from django.http import Http404

class DoctorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.user_type != 'دکتر' or user.doctorprofile.account_verification != True:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)