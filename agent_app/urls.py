from django.urls import path
from .views import home, VoiceAgentView, ask_ai

urlpatterns = [
    path('', home, name='home'),
    path('api/ask/', ask_ai, name='ask_ai'),  # Added ask_ai URL
    path('api/voice-agent/', VoiceAgentView.as_view(), name='voice_agent'),
]
