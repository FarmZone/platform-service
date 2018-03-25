from django.conf import settings
import re
from django.http import HttpResponse
import logging


logger = logging.getLogger(__name__)


class RBACMiddleware(object):
    """Django middle-ware class which provide check of role based
     access of various apps. Here we are using django groups as roles
     for the apps and hence we will have unique role for every app.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated() and not self.has_permission(request):
            response = HttpResponse("""<html>
                            <body>
                                <p style="text-style:bold; color:red">
                                    You have insufficient permission to access this page.
                                </p>
                            </body>
                        </html>
                        """, content_type="text/html")
        else:
            response = self.get_response(request)
        return response

    def has_permission(self, request):
        current_user = request.user
        #If the user is superuser and requested path starts with admin,
        #then the user should be allowed to access
        # if current_user.is_superuser and request.path.startswith('/admin'):
        #     return True
        # required_role = self.find_required_role(request)
        #current_user_roles = map(lambda x: x["name"].lower(), current_user.groups.values("name"))
        # if required_role:
        #     return required_role.lower() in current_user_roles
        return True

    # def find_required_role(self, request):
    #     uri = request.path
    #     for role in settings.ROLES:
    #         if re.search(role.url_structure, uri):
    #             return role.required_role
