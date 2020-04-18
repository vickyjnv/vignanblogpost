from .models import Com
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
	ListView,
	CreateView,
)
from django.contrib import messages
from django.shortcuts import render
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
		name = form.cleaned_data.get('name')
		messages.success(self.request, f'Group {name} Created!')
		form.instance.user = self.request.user
		return super().form_valid(form)

def error_404_view(request, exception):
	return render(request,'error.html')

