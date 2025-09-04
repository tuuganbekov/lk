import time
import uuid
from loguru import logger


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"[LOG] REQUEST {request.method} {request.path}")
        trace_id = str(uuid.uuid4())
        request.trace_id = trace_id
        response = self.get_response(request)
        response['TraceId'] = trace_id
        logger.info(f"[LOG] RESPONSE {response.status_code}")
        return response
