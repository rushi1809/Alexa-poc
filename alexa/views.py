import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)

def build_alexa_response(message):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": message
            },
            "shouldEndSession": True
        }
    }


@csrf_exempt
def alexa_webhook(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=405
        )

    try:
        payload = json.loads(request.body.decode("utf-8"))
        logger.info("Alexa Payload: %s", payload)
    except Exception:
        return JsonResponse(
            build_alexa_response(
                "Invalid request received."
            )
        )

    request_data = payload.get("request", {})
    request_type = request_data.get("type")

    # Alexa: Open Skill
    if request_type == "LaunchRequest":
        return JsonResponse(
            build_alexa_response(
                "Welcome to Alexa POC."
            )
        )

    # Alexa: Intent
    if request_type == "IntentRequest":
        intent_name = (
            request_data.get("intent", {})
            .get("name")
        )
        logger.info("Alexa Intent Received: %s", intent_name)
        if intent_name == "HelloWorldIntent":
            return JsonResponse(
                build_alexa_response(
                    "Hello from Django Alexa POC."
                )
            )

        return JsonResponse(
            build_alexa_response(
                f"Intent {intent_name} is not supported."
            )
        )

    return JsonResponse(
        build_alexa_response(
            "Unable to process your request."
        )
    )