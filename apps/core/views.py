import time

from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

PROJECT_VERSION = "0.1.0"


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([AllowAny])
def system_status(request):
    components = {}
    overall_healthy = True

    # Database check
    try:
        start = time.monotonic()
        connection.ensure_connection()
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        components["database"] = {"status": "healthy", "latency_ms": latency_ms}
    except Exception as e:
        overall_healthy = False
        components["database"] = {"status": "unhealthy", "error": str(e)}

    # API info
    components["api"] = {"status": "healthy", "version": PROJECT_VERSION}

    data = {
        "status": "healthy" if overall_healthy else "unhealthy",
        "updated_at": timezone.now().isoformat(),
        "components": components,
    }

    http_status = (
        status.HTTP_200_OK if overall_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return Response(data, status=http_status)
