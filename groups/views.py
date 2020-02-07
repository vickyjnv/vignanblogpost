from .models import Com
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
	ListView,
	CreateView,
)
# Create your views here.

class GroupListView(ListView):
	model = Com
	template_name = 'groups/groups.html'
	context_object_name = 'group'
	ordering = ['-name']



class GroupCreateView(LoginRequiredMixin, CreateView):
	model = Com
	fields = ['name','discripton']
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
