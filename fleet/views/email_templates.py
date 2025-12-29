from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from ..models import EmailTemplate
from ..forms import EmailTemplateForm

class EmailTemplateListView(ListView):
    model = EmailTemplate
    template_name = "email/template_list.html"
    context_object_name = "templates"


class EmailTemplateCreateView(CreateView):
    model = EmailTemplate
    form_class = EmailTemplateForm
    template_name = "email/template_form.html"
    success_url = reverse_lazy("emailtemplate_list")


class EmailTemplateUpdateView(UpdateView):
    model = EmailTemplate
    form_class = EmailTemplateForm
    template_name = "email/template_form.html"
    success_url = reverse_lazy("email/template_list")
