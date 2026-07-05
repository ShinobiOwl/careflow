import requests
import time
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import AIConversation, AIMessage
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment


def get_db_context(user_message):
    """Fetches live data from MySQL to feed to the AI brain"""
    today = timezone.now().date()
    msg_lower = user_message.lower()
    
    total_patients = Patient.objects.filter(is_active=True).count()
    doctors = Doctor.objects.filter(is_active=True)
    total_doctors = doctors.count()
    available_doctors = doctors.filter(status='available').count()
    on_duty_doctors = doctors.filter(status='on_duty').count()
    on_leave_doctors = doctors.filter(status='on_leave').count()
    
    today_appts = Appointment.objects.filter(appointment_date=today).count()
    pending_appts = Appointment.objects.filter(status='scheduled').count()
    
    # Base context
    context = f"""
    HOSPITAL DATA:
    Date: {today}
    Patients: {total_patients}
    Doctors: {total_doctors} (Available: {available_doctors}, On-Duty: {on_duty_doctors}, On-Leave: {on_leave_doctors})
    Today's Appts: {today_appts}
    Pending Appts: {pending_appts}
    """
    
    # ONLY provide detailed lists if explicitly requested to save tokens/time
    if any(word in msg_lower for word in ['list', 'who', 'which', 'names']):
        if 'doctor' in msg_lower or 'available' in msg_lower:
            doctor_list = [f"{d.full_name}: {d.get_status_display()}" for d in doctors]
            if doctor_list:
                context += "\nDOCTOR LIST:\n" + "\n".join(doctor_list)
        
        if 'appointment' in msg_lower or 'schedule' in msg_lower:
            appts = Appointment.objects.filter(appointment_date=today).select_related('patient', 'doctor').order_by('appointment_time')[:10]
            if appts:
                context += "\nSCHEDULE:\n" + "\n".join([f"{a.appointment_time.strftime('%H:%M')} - {a.patient.full_name} ({a.doctor.short_name})" for a in appts])
            
    return context

@login_required
def ai_dashboard(request):
    conversations = AIConversation.objects.filter(user=request.user)
    return render(request, 'ai_assistant/dashboard.html', {'conversations': conversations})


@login_required
def ai_chat(request, pk=None):
    conversation = None
    messages_list = []

    if pk:
        conversation = get_object_or_404(AIConversation, pk=pk, user=request.user)
        messages_list = conversation.messages.all()

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        category = request.POST.get('category', 'general_health')

        if not user_message:
            messages.error(request, 'Please enter a message.')
            return redirect('ai_chat')

        if not conversation:
            conversation = AIConversation.objects.create(
                user=request.user,
                category=category,
                title=user_message[:80],
            )

        AIMessage.objects.create(conversation=conversation, role='user', content=user_message)

        db_context = get_db_context(user_message)
        
        system_prompt = (
            "You are the CareFlow System Interface. Your sole purpose is to provide accurate information "
            "based on the PROVIDED DATA below. \n\n"
            "RULES:\n"
            "1. Use the PROVIDED DATA to answer questions about doctors, patients, and appointments.\n"
            "2. If the answer is in the PROVIDED DATA, you MUST use it. Do NOT say you don't have access to real-time information.\n"
            "3. If the answer is NOT in the PROVIDED DATA, simply state that the information is not currently available.\n"
            "4. Be concise and professional.\n"
            "5. Always mention that you are an AI assistant and not a replacement for professional medical judgment.\n\n"
            "PROVIDED DATA:\n"
            f"{db_context}"
        )

        chat_history = [{"role": "system", "content": system_prompt}]
        recent_msgs = conversation.messages.order_by('created_at')[:20]
        for msg in recent_msgs:
            chat_history.append({"role": msg.role, "content": msg.content})

        start_time = time.time()
        try:
            response = requests.post(
                f"{settings.FLASK_AI_URL}/api/chat",
                json={"model": settings.OLLAMA_MODEL, "messages": chat_history, "stream": False},
                timeout=300,
            )
            elapsed = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                data = response.json()
                assistant_content = data.get('message', {}).get('content', 'No response received.')
                tokens = data.get('eval_count', 0)
            else:
                assistant_content = f"Error: AI service returned status {response.status_code}."
                tokens = 0
        except Exception:
            assistant_content = "Cannot reach AI service. Is Ollama running?"
            tokens = 0
            elapsed = 0

        AIMessage.objects.create(
            conversation=conversation, role='assistant',
            content=assistant_content, tokens_used=tokens, response_time_ms=elapsed
        )

        return redirect('ai_chat', pk=conversation.pk)

    context = {
        'conversation': conversation,
        'messages_list': messages_list,
        'conversations': AIConversation.objects.filter(user=request.user)[:10],
    }
    return render(request, 'ai_assistant/chat.html', context)



@login_required
def ai_new_chat(request):
    return redirect('ai_chat')


@login_required
def ai_delete_conversation(request, pk):
    conversation = get_object_or_404(AIConversation, pk=pk, user=request.user)
    conversation.delete()
    messages.success(request, 'Conversation deleted.')
    return redirect('ai_dashboard')


@login_required
@require_POST
def ai_delete_all_conversations(request):
    AIConversation.objects.filter(user=request.user).delete()
    messages.success(request, 'All conversations deleted successfully.')
    return redirect('ai_dashboard')

def ai_chat_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        category = data.get('category', 'general_health')

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        conversation = None
        if conversation_id:
            conversation = AIConversation.objects.filter(pk=conversation_id, user=request.user).first()

        if not conversation:
            conversation = AIConversation.objects.create(user=request.user, category=category, title=user_message[:80])

        AIMessage.objects.create(conversation=conversation, role='user', content=user_message)

        db_context = get_db_context(user_message)
        system_prompt = (
            "You are the CareFlow System Interface. Your sole purpose is to provide accurate information "
            "based on the PROVIDED DATA below. \n\n"
            "RULES:\n"
            "1. Use the PROVIDED DATA to answer questions about doctors, patients, and appointments.\n"
            "2. If the answer is in the PROVIDED DATA, you MUST use it. Do NOT say you don't have access to real-time information.\n"
            "3. If the answer is NOT in the PROVIDED DATA, simply state that the information is not currently available.\n"
            "4. Be concise and professional.\n"
            "5. Always mention that you are an AI assistant and not a replacement for professional medical judgment.\n\n"
            "PROVIDED DATA:\n"
            f"{db_context}"
        )

        chat_history = [{"role": "system", "content": system_prompt}]
        for msg in conversation.messages.order_by('created_at')[:20]:
            chat_history.append({"role": msg.role, "content": msg.content})

        start_time = time.time()
        try:
            response = requests.post(
                f"{settings.FLASK_AI_URL}/api/chat",
                json={"model": settings.OLLAMA_MODEL, "messages": chat_history, "stream": False},
                timeout=300,
            )
            elapsed = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                resp_data = response.json()
                assistant_content = resp_data.get('message', {}).get('content', 'No response.')
                tokens = resp_data.get('eval_count', 0)
            else:
                assistant_content = "AI service error. Try again."
                tokens = 0
        except Exception:
            assistant_content = "Cannot reach AI service."
            tokens = 0
            elapsed = 0

        AIMessage.objects.create(
            conversation=conversation, role='assistant',
            content=assistant_content, tokens_used=tokens, response_time_ms=elapsed
        )

        return JsonResponse({
            'conversation_id': conversation.pk,
            'message': assistant_content,
            'tokens': tokens,
            'response_time_ms': elapsed,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
