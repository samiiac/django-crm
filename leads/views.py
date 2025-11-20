from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, AssignAgentForm,LeadCategoryUpdateForm
from .models import Lead, Category
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LeadForm
from agents.mixins import OrganizerandLoginRequiredMixin




class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


def landing_page(request):
    return render(request, "landing.html")


class LandingView(generic.TemplateView):
    template_name = "landing.html"


def lead_list(request):
    lead = Lead.objects.all()
    context = {"lead_list": lead}
    return render(request, "lead_list.html", context=context)


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "lead_list.html"

    context_object_name = "lead_list"

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()

        if user.is_agent:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, agent__isnull=False
            )
            queryset = queryset.filter(agent__user=user)
            # leads assigned to and on same org as agent
        elif user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, agent__isnull=False
            )
            # leads on the same organization as the organizer ie loggedin user
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, agent__isnull=True
            )
            context.update({"unassigned_leads": queryset})
        return context


def lead_detail(request, pk):
    lead_detail = Lead.objects.get(id=pk)
    context = {"lead_detail": lead_detail}
    return render(request, "lead_detail.html", context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "lead_detail.html"

    context_object_name = "lead_detail"

    def get_queryset(self):
        user = self.request.user

        queryset = Lead.objects.all()

        if user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        elif user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset


def lead_create(request):

    if request.method == "POST":

        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    else:
        context = {"form": LeadForm()}
        return render(request, "lead_create.html", context)


class LeadCreateView(OrganizerandLoginRequiredMixin, generic.CreateView):
    template_name = "lead_create.html"

    form_class = LeadForm

    def get_success_url(self):
        return reverse("leads-list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="Lead created",
            message="Lead has been created.You can check it out.",
            from_email="django@crm.com",
            recipient_list=["test@test.com"],
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form_class = LeadForm(instance=lead)
    context = {"lead": lead, "form": form}

    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    else:
        return render(request, "lead_update.html", context)


class LeadUpdateView(OrganizerandLoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadForm

    def get_success_url(self, *args, **kwargs):

        return reverse("leads-detail", kwargs={"pk": self.object.id})

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)


class LeadDeleteView(OrganizerandLoginRequiredMixin, generic.DeleteView):
    template_name = "lead_delete.html"

    def get_success_url(self):
        return reverse("leads-list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)


class AssignAgentView(OrganizerandLoginRequiredMixin, generic.FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return reverse("leads-list")

    def form_valid(self, form):
        lead = Lead.objects.get(id=self.kwargs["pk"])
        agent = form.cleaned_data["agent"]
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)

        context.update(
            {"unassigned_leads": queryset.filter(category__isnull=True).count()}
        )
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset
    
    
class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"
    
    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset
    
    
class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user = user)

        return queryset
    
    
    def get_success_url(self):
        return reverse("leads-detail",kwargs={"pk" : self.get_object().id})
    
    
    
    
    
