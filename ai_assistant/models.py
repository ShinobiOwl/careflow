from django.db import models
from django.contrib.auth.models import User


class AIConversation(models.Model):
    CATEGORY_CHOICES = (
        ('symptom_check', 'Symptom Check'),
        ('drug_interaction', 'Drug Interaction'),
        ('general_health', 'General Health'),
        ('lab_interpretation', 'Lab Report Interpretation'),
        ('clinical_note', 'Clinical Note Assistance'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default='general_health')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title or self.category} - {self.user.username}"

    class Meta:
        ordering = ['-updated_at']


class AIMessage(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )

    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    tokens_used = models.PositiveIntegerField(default=0)
    response_time_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."

    class Meta:
        ordering = ['created_at']