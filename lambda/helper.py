import paho.mqtt.publish as publish
import json

HOST = 'test.mosquitto.org' # Public MQTT broker
PORT = 1883 # Standart port

"""
This class is used to react appropriately to the intents. The MQTT messages are sent to the MQTT broker here.
"""


def handle_confirmation_intent(handler_input):
    session_attributes = handler_input.attributes_manager.session_attributes
    locale = handler_input.request_envelope.request.locale
    
    if session_attributes.get('confirmation_pending'):
        
        # Reset flag
        session_attributes['confirmation_pending'] = False
        
        if session_attributes.get('intent') in ['DriveForwardIntent', 'DriveBackwardIntent']:
            
            # Get distance value for DriveForwardIntent and DriveForwardIntent from the session attributes
            
            payload = {
                "distance" : session_attributes.get('distance')
            }
            
            # Differentiate between forward and backward
            
            if session_attributes.get('intent') == 'DriveForwardIntent':
                topic = 'mav/forward'
                
                if locale.startswith("de"):
                    direction = 'vorwärts'
                elif locale.startswith("en"):
                    direction = 'forward'
                else:
                    direction = 'forward'
            else:
                topic = 'mav/backward'
                
                if locale.startswith("de"):
                    direction = 'rückwärts'
                elif locale.startswith("en"):
                    direction = 'backward'
                else:
                    direction = 'backward'
            
            # Send message to the MQTT broker
            result = send_mqtt_message_catch_errors(topic, json.dumps(payload))
            
            if result != True:
                return result
            else:
                # Generate the voice output for alexa with the appropriate language.
                
                if locale.startswith("de"):
                    return f"Okay ich fahre {session_attributes.get('distance')} {session_attributes.get('unit')} {direction}"
                elif locale.startswith("en"):
                    return f"Okay I drive {session_attributes.get('distance')} {session_attributes.get('unit')} {direction}"
                else:
                    return f"Okay I drive {session_attributes.get('distance')} {session_attributes.get('unit')} {direction}"
                
        elif session_attributes.get('intent') in ['DriveLeftIntent', 'DriveRightIntent']:
            
            # Get angle value for DriveLeftIntent and DriveRightIntent attributes
            
            payload = {
                "angle" : session_attributes.get('angle')
            }
            
            # Get the direction
            
            if session_attributes.get('intent') == 'DriveLeftIntent':
                topic = 'mav/turn_left'
                
                if locale.startswith("de"):
                    direction = 'links'
                elif locale.startswith("en"):
                    direction = 'left'
                else:
                    direction = 'left'
            else:
                topic = 'mav/turn_right'
                
                if locale.startswith("de"):
                    direction = 'rechts'
                elif locale.startswith("en"):
                    direction = 'right'
                else:
                    direction = 'right'
            
            # Send message to the MQTT broker
            
            result = send_mqtt_message_catch_errors(topic, json.dumps(payload))
            
            if result != True:
                return result
            else:
                
                # Generate voice output
                
                locale = handler_input.request_envelope.request.locale
                if locale.startswith("de"):
                    return f"Okay ich fahre {session_attributes.get('angle')} {session_attributes.get('unit')} {direction}."
                elif locale.startswith("en"):
                    return f"Okay I will turn by {session_attributes.get('angle')} {session_attributes.get('unit')} {direction} now."
                else:
                    return f"Okay I will turn by {session_attributes.get('angle')} {session_attributes.get('unit')} {direction} now."
                
    else:
        # If the intent is triggered but there is nothing to confirm, inform the user that there is nothing to confirm.
        
        locale = handler_input.request_envelope.request.locale
        
        if locale.startswith("de"):
            speak_output = "Es gibt nichts zu bestätigen."
        elif locale.startswith("en"):
            speak_output = "There is nothing to confirm."
        else:
            speak_output = "There is nothing to confirm."
            
        return speak_output

def handle_stop_driving_intent(handler_input):
    """
    Handler which is used to stop the MAV robot if requested by the user. No confirmation needed!
    """
    
    result = send_mqtt_message_catch_errors('mav/stop_mav', None)
    
    if result != True:
        return result
    else:
        locale = handler_input.request_envelope.request.locale
        
        if locale.startswith("de"):
            return str("Der MAV stoppt nun mit dem Fahren.")
        elif locale.startswith("en"):
            return str("The MAV stops driving now")
        else:
            return str("The MAV stops driving now")
    

def send_mqtt_message_catch_errors(topic, payload):
    """
    Method which is used to send/publish the MQTT message to the broker. 
    """
    
    try:
        publish.single(topic, payload=payload, hostname=HOST, port=PORT)
        return True
        
    except Exception as ex:
        locale = handler_input.request_envelope.request.locale
        
        if locale.startswith("de"):
            speak_output = f"Es gab einen Fehler beim Senden der Nachricht mit MQTT. Der Fehler lautet: {ex}"
        elif locale.startswith("en"):
            speak_output = f"There was an error sending the message with MQTT. The error is: {ex}"
        else:
            speak_output = f"There was an error sending the message with MQTT. The error is: {ex}"
            
        return speak_output

def handle_drive_forward_intent(handler_input):
    """
    Handler which is used to process the DriveForwardIntent. Confirmation is required.
    """
    
    slots = handler_input.request_envelope.request.intent.slots
    
    # If a distance value is provided, use it and convert/parse it to meter. If no distance value is provided drive 1 meter forward.
    if slots["distance"].value:
        distance_slot_value, unit_value = parse_value_unit(str(slots["distance"].value), str(slots["unit"].value))
    else:
        distance_slot_value, unit_value = 1.0, 'meter'
        
        
    session_attributes = handler_input.attributes_manager.session_attributes
    session_attributes["intent"] = "DriveForwardIntent"
    session_attributes["distance"] = distance_slot_value
    session_attributes["unit"] = unit_value
    session_attributes["confirmation_pending"] = True
    
    locale = handler_input.request_envelope.request.locale
        
    if locale.startswith("de"):
        speak_output = f"Soll ich wirklich {distance_slot_value} {unit_value} vorwärts fahren?"
    elif locale.startswith("en"):
        speak_output = f"Should I really drive {distance_slot_value} {unit_value} forward?"
    else:
        speak_output = f"Should I really drive {distance_slot_value} {unit_value} forward?"
    
    return speak_output


def handle_drive_backward_intent(handler_input):
    """
    Handler which is used to process the DriveBackwardIntent. Confirmation is required.
    """
    
    slots = handler_input.request_envelope.request.intent.slots
    
    # If a distance value is provided, use it and convert/parse it to meter. If no distance value is provided drive 1 meter backward.
    if slots["distance"].value:
        distance_slot_value, unit_value = parse_value_unit(str(slots["distance"].value), str(slots["unit"].value))
    else:
        distance_slot_value, unit_value = 1.0, 'meter'
        
        
    session_attributes = handler_input.attributes_manager.session_attributes
    session_attributes["intent"] = "DriveBackwardIntent"
    session_attributes["distance"] = distance_slot_value
    session_attributes["unit"] = unit_value
    session_attributes["confirmation_pending"] = True
    
    locale = handler_input.request_envelope.request.locale
        
    if locale.startswith("de"):
        speak_output = f"Soll ich wirklich {distance_slot_value} {unit_value} rückwärts fahren?"
    elif locale.startswith("en"):
        speak_output = f"Should I really drive {distance_slot_value} {unit_value} backward?"
    else:
        speak_output = f"Should I really drive {distance_slot_value} {unit_value} backward?"
    
    return speak_output


def handle_drive_left_intent(handler_input):
    """
    Handler which is used to process the DriveLeftIntent. Confirmation is required.
    """
    
    slots = handler_input.request_envelope.request.intent.slots
    locale = handler_input.request_envelope.request.locale
    
    # If a angle value is provided, use it and convert/parse it to degree. If no angle value is provided drive 90 degrees to the left.
    if slots["angle"].value:
        angle_slot_value, unit_value = parse_value_unit(str(slots["angle"].value), str(slots["unit"].value))
    else:
        if locale.startswith("de"):
            angle_slot_value, unit_value = 90.0, 'grad'
        elif locale.startswith("en"):
            angle_slot_value, unit_value = 90.0, 'degree'
        else:
            angle_slot_value, unit_value = 90.0, 'degree'
        
        
    session_attributes = handler_input.attributes_manager.session_attributes
    session_attributes["intent"] = "DriveLeftIntent"
    session_attributes["angle"] = angle_slot_value
    session_attributes["unit"] = unit_value
    session_attributes["confirmation_pending"] = True
        
    if locale.startswith("de"):
        speak_output = f"Soll ich wirklich {angle_slot_value} {unit_value} nach links fahren?"
    elif locale.startswith("en"):
        speak_output = f"Should I really turn {angle_slot_value} {unit_value} to the left?"
    else:
        speak_output = f"Should I really turn {angle_slot_value} {unit_value} to the left?"
        
    return speak_output


def handle_drive_right_intent(handler_input):
    """
    Handler which is used to process the DriveRightIntent. Confirmation is required.
    """
    slots = handler_input.request_envelope.request.intent.slots
    locale = handler_input.request_envelope.request.locale
    
    # If a angle value is provided, use it and convert/parse it to degree. If no angle value is provided drive 90 degrees to the right.
    if slots["angle"].value:
        angle_slot_value, unit_value = parse_value_unit(str(slots["angle"].value), str(slots["unit"].value))
    else:
        if locale.startswith("de"):
            angle_slot_value, unit_value = 90.0, 'grad'
        elif locale.startswith("en"):
            angle_slot_value, unit_value = 90.0, 'degrees'
        else:
            angle_slot_value, unit_value = 90.0, 'degrees'
        
        
    session_attributes = handler_input.attributes_manager.session_attributes
    session_attributes["intent"] = "DriveRightIntent"
    session_attributes["angle"] = angle_slot_value
    session_attributes["unit"] = unit_value
    session_attributes["confirmation_pending"] = True
        
    if locale.startswith("de"):
        speak_output = f"Soll ich wirklich {angle_slot_value} {unit_value} nach rechts fahren?"
    elif locale.startswith("en"):
        speak_output = f"Should I really turn {angle_slot_value} {unit_value} to the right?"
    else:
        speak_output = f"Should I really turn {angle_slot_value} {unit_value} to the right?"
    
    return speak_output

def parse_value_unit(value, unit):
    """
    This method is used by the IntentHandlers to convert the value of a valid unit of measurement to meter (distance) or degree (angle).
    """
    
    if unit in ['meter', 'Meter']:
        return float(value), 'meter'
        
    elif unit in ['zentimeter', 'Zentimeter', 'centimeter']:
        return float(float(value) / 100), 'meter'
    
    elif unit in ['grad', 'Grad']:
        return float(value), 'grad'
        
    elif unit in ['degree', 'degrees']:
        return float(value), 'degree'
        
    else:
        return float(value), 'NoUnit'