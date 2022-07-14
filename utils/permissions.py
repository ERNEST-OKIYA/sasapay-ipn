from rest_framework import permissions
from ipware import get_client_ip

class WhitelistPermission(permissions.BasePermission):
    """
    Global permission check for whitelisted IPs.
    """

    def has_permission(self, request, view):
        client_ip, is_routable = get_client_ip(request)

        pass
