from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os
from PIL import Image
from transformers import pipeline

# Initialize the image classification pipeline
classifier = pipeline("image-classification", model="Luwayy/disaster_images_model")

# Damage-to-service mapping
DAMAGE_SERVICES = {
    "water": ["Plumber", "Water Damage Specialist"],
    "fire": ["Fire Damage Restoration"],
    "human": ["General Contractor"],
    "crack": ["Mason", "Structural Engineer"],
    "structural": ["Structural Engineer"],
    "electrical": ["Electrician"],
    "mold": ["Mold Remediation Specialist"],
    "roof": ["Roofer"],
    "window": ["Glazier", "Window Specialist"]
}

def get_services(damage_type):
    damage_type = damage_type.lower()
    services = []

    for keyword, service_list in DAMAGE_SERVICES.items():
        if keyword in damage_type:
            services.extend(service_list)

    return list(set(services)) if services else ["General Contractor"]

def query_model(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        results = classifier(image)
        if results:
            top_result = results[0]
            return {
                "damage_type": top_result['label'],
                "confidence": top_result['score']
            }
        else:
            return {"error": "No damage detected."}
    except Exception as e:
        return {"error": str(e)}

def analyze_damage(request):
    if request.method == 'POST' and request.FILES.get('media'):
        media = request.FILES['media']

        # Validate image
        if not media.content_type.startswith('image/'):
            return JsonResponse({"error": "Only image files are allowed."}, status=400)

        try:
            # Save uploaded file
            file_path = f"media/{media.name}"
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in media.chunks():
                    destination.write(chunk)

            # Analyze image
            abs_path = default_storage.path(file_path)
            result = query_model(abs_path)

            if 'error' in result:
                return JsonResponse({
                    "error": "Damage analysis failed",
                    "details": result.get("error", "Unknown error")
                }, status=500)

            damage_type = result.get('damage_type', 'Unknown damage')
            services = get_services(damage_type)

            return JsonResponse({
                "damage_type": damage_type,
                "services": services,
                "confidence": result.get('confidence', 0),
                "image_url": default_storage.url(file_path)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)








# its for the chatbot 


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .chatbot_logic import DamageAssessmentChatbot
# import json

# chatbot = DamageAssessmentChatbot()

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .chatbot_logic import DamageAssessmentChatbot

# chatbot = DamageAssessmentChatbot()

# @csrf_exempt
# def chat_api(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_message = data.get('message', '')
            
#             if not user_message:
#                 return JsonResponse({'error': 'Empty message'}, status=400)
            
#             # Get or create session
#             session_key = request.session.session_key
#             if not session_key:
#                 request.session.create()
#                 session_key = request.session.session_key
            
#             # Get bot response
#             response = chatbot.respond(user_message)
            
#             return JsonResponse(response)
                
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             return JsonResponse({
#                 'error': str(e),
#                 'response': "I encountered an error processing your request."
#             }, status=500)
    
#     return JsonResponse({'error': 'Method not allowed'}, status=405)