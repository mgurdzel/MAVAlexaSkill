# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from helper import handle_drive_forward_intent, handle_drive_backward_intent, handle_confirmation_intent, handle_drive_left_intent, handle_drive_right_intent, handle_stop_driving_intent

from ask_sdk_model import Response


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)



class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch.
    Gives welcome command in appropriate language for the user."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        locale = handler_input.request_envelope.request.locale
        
        if locale.startswith("de"):
            speak_output = "Hallo, willkommen beim MAV-Controller. Bitte gebe einen Befehl in welche Richtung ich fahren soll."
        elif locale.startswith("en"):
            speak_output = "Hello, welcome to the MAV controller. Please give a command in which direction I should drive."
        else:
            speak_output = "Hello, welcome to the MAV controller. Please give a command in which direction I should drive."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        locale = handler_input.request_envelope.request.locale
        
        if locale.startswith("de"):
            speak_output = "Hallo, willkommen beim MAV-Controller. Wie kann ich dir helfen?."
        elif locale.startswith("en"):
            speak_output = "Hello, welcome to the MAV controller. Please give a command in which direction I should drive."
        else:
            speak_output = "Hello, welcome to the MAV controller. Please give a command in which direction I should drive."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent.
    Is able to stop the confirmation of a move command which was previously called."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["confirmation_pending"] = False
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent.
    Is called if the skill has not understood the command."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        
        locale = handler_input.request_envelope.request.locale
        
        if locale.startswith("de"):
            speech = "Hmm, ich bin mir nicht sicher. Du kannst Hallo oder Hilfe sagen. Was möchtest du tun?"
            reprompt = "Ich habe es nicht verstanden. Wie kann ich dir helfen?"
        elif locale.startswith("en"):
            speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
            reprompt = "I didn't catch that. What can I help you with?"
        else:
            speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
            reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        
        locale = handler_input.request_envelope.request.locale
        
        if locale.startswith("de"):
            speak_output = "Entschuldigung, ich hatte Probleme zu verstehen was du gesagt hast. Bitte versuche es erneut."
        elif locale.startswith("en"):
            speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        else:
            speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ConfirmationIntentHandler(AbstractRequestHandler):
    
    """Handler for Confirmation Intent.
    Is required to finally execute the movement command."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ConfirmationIntent")(handler_input)

    def handle(self, handler_input):
        
        speak_output = handle_confirmation_intent(handler_input)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class DriveForwardIntentHandler(AbstractRequestHandler):
    """Handler for Drive Forward Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DriveForwardIntent")(handler_input)

    def handle(self, handler_input):
        
        speak_output = handle_drive_forward_intent(handler_input)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DriveBackwardsIntentHandler(AbstractRequestHandler):
    
    """Handler for Drive Backward Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DriveBackwardsIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = handle_drive_backward_intent(handler_input)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DriveLeftIntentHandler(AbstractRequestHandler):
    
    """Handler for Drive Left Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DriveLeftIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = handle_drive_left_intent(handler_input)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DriveRightIntentHandler(AbstractRequestHandler):
    
    """Handler for Drive Right Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DriveRightIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = handle_drive_right_intent(handler_input)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class StopDrivingIntentHandler(AbstractRequestHandler):
    
    """Handler for Stop Driving Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StopDrivingIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = handle_stop_driving_intent(handler_input)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(ConfirmationIntentHandler())
sb.add_request_handler(DriveForwardIntentHandler())
sb.add_request_handler(DriveBackwardsIntentHandler())
sb.add_request_handler(DriveLeftIntentHandler())
sb.add_request_handler(DriveRightIntentHandler())
sb.add_request_handler(StopDrivingIntentHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

lambda_handler = sb.lambda_handler()