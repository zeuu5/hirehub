import re
from .models import DamageReport, ChatMessage
from django.utils import timezone

class DamageAssessmentChatbot:
    def __init__(self):
        self.conversation_state = "greeting"
        self.current_report = None
        self.conversation_states = {}  # For tracking multiple conversations

    def respond(self, message, user=None, session_key=None):
        message = message.lower().strip()
        
        # Get or initialize conversation state
        if session_key not in self.conversation_states:
            self.conversation_states[session_key] = {
                'state': 'greeting',
                'report_data': {}
            }
        state = self.conversation_states[session_key]

        # State machine logic
        if state['state'] == 'greeting':
            return self.handle_greeting(state)
            
        elif state['state'] == 'damage_type':
            return self.handle_damage_type(message, state)
            
        elif state['state'] == 'damage_description':
            return self.handle_description(message, state)
            
        elif state['state'] == 'severity':
            return self.handle_severity(message, state, user, session_key)
            
        return {
            "text": "I'm sorry, I didn't understand that. Could you rephrase?",
            "status": "success"
        }

    def handle_greeting(self, state):
        state['state'] = 'damage_type'
        return {
            "text": "Welcome to Damage Assessment! What type of damage are you experiencing?\n\n"
                    "Please choose from: plumbing, electrical, structural, appliance, or other.",
            "status": "success"
        }

    def handle_damage_type(self, message, state):
        damage_types = ['plumbing', 'electrical', 'structural', 'appliance', 'other']
        detected = next((t for t in damage_types if t in message.lower()), None)
        
        if detected:
            state['report_data']['damage_type'] = detected
            state['state'] = 'damage_description'
            return {
                "text": f"Understood, {detected} issue. Please describe the damage in detail.",
                "status": "success"
            }
        return {
            "text": "I didn't recognize that damage type. Please choose from: plumbing, electrical, structural, appliance, or other.",
            "status": "success"
        }

    def handle_description(self, message, state):
        if len(message) < 10:
            return {
                "text": "Please provide a more detailed description of the damage.",
                "status": "success"
            }
        
        state['report_data']['description'] = message
        state['state'] = 'severity'
        return {
            "text": "Thank you. How would you rate the severity?\n\n"
                    "Options: low (minor issue), medium (needs attention), high (serious problem), emergency (needs immediate action)",
            "status": "success"
        }

    def handle_severity(self, message, state, user, session_key):
        severities = ['low', 'medium', 'high', 'emergency']
        detected = next((s for s in severities if s in message.lower()), None)
        
        if detected:
            state['report_data']['severity'] = detected
            state['state'] = 'complete'
            
            # Create damage report
            report = DamageReport.objects.create(
                user=user if user and user.is_authenticated else None,
                damage_type=state['report_data']['damage_type'],
                description=state['report_data']['description'],
                status='new'
            )
            
            # Get recommendation
            recommendation = self.get_recommendation(
                state['report_data']['damage_type'],
                state['report_data']['severity']
            )
            
            # Clear conversation state
            self.conversation_states.pop(session_key, None)
            
            return {
                "text": f"Report created! {recommendation}\n\n"
                        "A service professional will review your case shortly. "
                        "You can check the status anytime by asking 'status update'.",
                "status": "success",
                "damage_report_id": report.id
            }
        return {
            "text": "Please specify severity: low, medium, high, or emergency.",
            "status": "success"
        }

    def get_recommendation(self, damage_type, severity):
        recommendations = {
            'plumbing': {
                'low': "For minor plumbing issues, try tightening connections or using a plunger.",
                'medium': "Schedule a plumber for pipe repairs within the next few days.",
                'high': "Contact a licensed plumber immediately for significant leaks.",
                'emergency': "CALL AN EMERGENCY PLUMBER NOW! Shut off main water if necessary."
            },
            'electrical': {
                'low': "For minor electrical issues, check if the circuit breaker has tripped.",
                'medium': "Have an electrician inspect the wiring soon.",
                'high': "Stop using the affected circuit and call an electrician immediately.",
                'emergency': "EVACUATE IF SAFETY RISK! Call emergency electrician immediately!"
            }
            # Add other damage types...
        }
        return recommendations.get(damage_type, {}).get(severity, 
            "Contact a qualified professional to assess the damage.")

    def save_message(self, user, session_key, message, response, is_bot):
        ChatMessage.objects.create(
            user=user if user and user.is_authenticated else None,
            session_key=session_key,
            message=message,
            response=response,
            is_bot=is_bot,
            intent=self.detect_intent(message)
        )
    
    def detect_intent(self, message):
        message = message.lower()
        if any(word in message for word in ['thank', 'thanks', 'appreciate']):
            return 'gratitude'
        elif any(word in message for word in ['hi', 'hello', 'hey']):
            return 'greeting'
        return 'unknown'