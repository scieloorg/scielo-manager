from django.contrib.auth import logout
from maintenancewindow import models


class MaintenanceMiddleware(object):

    def process_request(self, request):

        on_maintenance = models.Event.on_maintenance()

        if on_maintenance and not request.user.is_staff:
            logout(request)

        return None
