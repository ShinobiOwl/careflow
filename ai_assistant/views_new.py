import requests
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import AIConversation, AIMessage
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from datetime import date

def get_careflow_context():
    """
    Gathers a summary of the current system state to provide context to the AI.
    """
    try:
        doctors = Doctor.objects.filter(is_active=True)
        doctor_list = [f"{d.full_name} ({d.specialization}) - Status: {d.get_status_display()}" for d in doctors]
        
        patient_count = Patient.objects.filter(is_active=True).count()
        today_appts = Appointment.objects.filter(appointment_date=date.today()).count()
        
        context = "\n\n--- CURRENT CAREFLOW SYSTEM DATA ---\n"
        context += f"Total Active Patients: {patient_count}\n"
        context += f"Appointments Today: {today_appts}\n"
        context += "Active Doctors:\n"
        if doctor_list:
            context += "\n".join(doctor_list)
        else:
            context += "No active doctors found."
        context += "\n----------------------------------\n"
        return context
    except Exception as e:
        return f"\n(Error gathering system context: {str(e)})\n"


@login_required
def ai_dashboard(request):
    conversations = AIConversation.objects.filter(user=request.user)
    context = {
        'conversations': conversations,
    }
    return render(request, 'ai_assistant/dashboard.html', context)
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
            return redirect('ai_dashboard')

        # Create or get conversation
        if not conversation:
            conversation = AIConversation.objects.create(
                user=request.user,
                category=category,
                title=user_message[:80],
            )

        # Save user message
        AIMessage.objects.create(
            conversation=conversation,
            role='user',
            content=user_message,
        )

        # Call Flask/Ollama API
        system_prompt = (
            "You are CareFlow AI, a medical assistant for hospital staff. "
            "Help with symptom analysis, drug interactions, clinical notes, and general medical queries. "
            "Always remind users that you are an AI assistant and not a replacement for professional medical judgment. "
            "Be concise, professional, and evidence-based in your responses."
        )
        
        # Inject real-time system data
        system_prompt += get_careflow_context()
        system_prompt += "\nUse the provided SYSTEM DATA to answer questions about doctors, patients, and appointments. If the information is not in the data, state that you don't have access to that specific real-time information."

        # Build message history for context
        chat_history = [{"role": "system", "content": system_prompt}]
        recent_msgs = conversation.messages.order_by('created_at')[:20]
        for msg in recent_msgs:
            chat_history.append({"role": msg.role, "content": msg.content})

        start_time = time.time()
        try:
            response = requests.post(
                f"{settings.FLASK_AI_URL}/api/chat",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "messages": chat_history,
                    "stream": False,
                },
                timeout=120,
            )
            elapsed = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                data = response.json()
                assistant_content = data.get('message', {}).get('content', 'No response received.')
                tokens = data.get('eval_count', 0)
            elif response.status_code == 502:
                assistant_content = "Error: The AI bridge is running, but it cannot reach the Ollama service. Please ensure Ollama is running."
                tokens = 0
            else:
                assistant_content = f"Error: AI service returned status {response.status_code}. Please try again."
                tokens = 0
        except requests.exceptions.ConnectionError:
            assistant_content = "Error: Cannot connect to the AI bridge service. Please ensure the Flask AI container is running."
            tokens = 0
            elapsed = 0
        except requests.exceptions.Timeout:
            assistant_content = "Error: AI service timed out. Please try a shorter query."
            tokens = 0
            elapsed = 0

        # Save assistant message
        AIMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=assistant_content,
            tokens_used=tokens,
            response_time_ms=elapsed,
        )

        return redirect('ai_chat', pk=conversation.pk)

    context = {
        'conversation': conversation,
        'messages_list': messages_list,
        'conversations': AIConversation.objects.filter(user=request.user)[:10],
    }
    return render(request, 'ai_assistant/chat.html', context)
