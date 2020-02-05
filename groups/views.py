from django.shortcuts import render
from .models import Com
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
	ListView,
	CreateView,
)
# Create your views here.

def group(request):
	context = {
		'group' : Com.objects.all()
	}
	return render(request, "groups/groups.html", context)


class GroupListView(ListView):
	model = Com
	template_name = 'groups/groups.html'
	context_object_name = 'group'
	ordering = ['-name']



class GroupCreateView(LoginRequiredMixin, CreateView):
	model = Com
	fields = ['name']
