from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout


class AuthMiddleware(MiddlewareMixin):

  def process_request(self, request):
    if request.path.startswith('/admin/'):
      return None
    else:
      if "access_token" in request.session:
        pass
      else:
        logout(request)
