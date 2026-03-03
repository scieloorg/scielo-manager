from django.contrib.auth import logout
from maintenancewindow import models


class MaintenanceMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        if self.get_response is None:
            return None
        return self.get_response(request)

    def process_request(self, request):

        on_maintenance = models.Event.on_maintenance()

        if on_maintenance and not request.user.is_staff:
            logout(request)

        return None
