from threading import local
local_thread = local()


def get_latest_request():
    """Gets the request that was last stored in the local thread.
    Note: when testing the receivers.py, because the postsave and postdelete receivers use this method,
    they will retrieve the request that was last stored in this local thread (unless it is wiped somehow)."""
    return getattr(local_thread, "request", None)


def _reset_current_request():
    setattr(local_thread, 'request', None)


class AuditLogMiddleware:
    """Responsible for making each new request available to the audit logger."""

    def __init__(self, get_response):
        """Only called at server startup."""
        self.get_response = get_response  # One-time configuration and initialization required by Django

    def __call__(self, request):
        """Called for each request"""
        _reset_current_request()
        local_thread.request = request
        # Code to be executed for each request before the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/reponse after the view is called.
        return response
