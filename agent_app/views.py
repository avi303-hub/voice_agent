from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import VoiceQuery
from .serializers import VoiceQuerySerializer
from google.cloud import speech
import openai
import requests
from django.core.files.storage import default_storage
from django.shortcuts import render

@csrf_exempt  
def ask_ai(request):
    if request.method == "POST":
        return JsonResponse({"message": "API is working!"})
    return JsonResponse({"error": "Invalid request"}, status=400)

class VoiceAgentView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)
        
        file_path = default_storage.save(audio_file.name, audio_file)
        text_query = self.speech_to_text(file_path)
        response_text = self.get_ai_response(text_query)
        audio_url = self.text_to_speech(response_text)
        
        voice_query = VoiceQuery.objects.create(query=text_query, response=response_text, audio_file=audio_url)
        return Response(VoiceQuerySerializer(voice_query).data)
    
    def speech_to_text(self, file_path):
        client = speech.SpeechClient()
        with open(file_path, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, language_code="en-US")
        response = client.recognize(config=config, audio=audio)
        return response.results[0].alternatives[0].transcript if response.results else ""
    
    def get_ai_response(self, text_query):
        openai.api_key = "YOUR_OPENAI_API_KEY"
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text_query}])
        return response["choices"][0]["message"]["content"]
    
    def text_to_speech(self, response_text):
        elevenlabs_api_key = "YOUR_ELEVENLABS_API_KEY"
        response = requests.post("https://api.elevenlabs.io/v1/text-to-speech", json={"text": response_text}, headers={"Authorization": f"Bearer {elevenlabs_api_key}"})
        audio_url = "media/audio/response.mp3"
        with open(audio_url, "wb") as f:
            f.write(response.content)
        return audio_url

def home(request):
    return render(request, "index.html")
