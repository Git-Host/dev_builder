from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from user_admin.forms import UserAdminAuthenticationForm
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
 
class UserAdmin(AdminSite):
    
    login_form = UserAdminAuthenticationForm
    
    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active
    
    @never_cache
    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        from user_admin.views import login
        context = {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        }
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        return login(request, **defaults)
    
    pass        

user_admin_site = UserAdmin(name='usersadmin')