from django.shortcuts import render, reverse
import random
from django.views import generic
from leads.models import Agent
from .forms import AgentModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganizerandLoginRequiredMixin

# Create your views here.


class AgentListView(OrganizerandLoginRequiredMixin,generic.ListView):
    template_name = "agents/list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    context_object_name = "agent_list"


class AgentCreateView(OrganizerandLoginRequiredMixin, generic.CreateView):
    template_name = "agents/create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agent-list")
    
    def form_valid(self, form):
        user = form.save(commit = False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0,1000)}")
        user.save()
        Agent.objects.create(user = user,organization = self.request.user.userprofile)
        
        return super(AgentCreateView,self).form_valid(form)
    


class AgentDetailView(OrganizerandLoginRequiredMixin,generic.DetailView):
    template_name = "agents/detail.html"
   

    context_object_name = "agent_detail"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentUpdateView(OrganizerandLoginRequiredMixin,generic.UpdateView):
    template_name = "agents/update.html"
    form_class = AgentModelForm
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self, *args, **kwargs):

        return reverse("agent-detail", kwargs={"pk": self.object.id})


class AgentDeleteView(OrganizerandLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/delete.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    
    def get_success_url(self):
        return reverse("agent-list")
