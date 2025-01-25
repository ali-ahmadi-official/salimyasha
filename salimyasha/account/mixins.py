from django.http import Http404
from django.shortcuts import redirect

class NotAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user is None or not hasattr(request.user, 'user_type'):
            raise Http404("Page not found")
        if request.user.is_authenticated and request.user.user_type is None:
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)

class DoctorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.doctor != request.user:
            return Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)
    
class AccountTrueRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.doctorprofile.account_verification != True:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

class FreeRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status != 'آزاد':
            return Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)

class SelfProfileMixin:
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)
    
class SelfUserMixin:
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile != request.user:
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)

class SelfClinicMixin:
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.doctor != request.user:
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)