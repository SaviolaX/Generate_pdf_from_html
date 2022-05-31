from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic import (
    ListView, View, DetailView, DeleteView, UpdateView)
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import DocumentCreateForm
from .models import Document, DocumentStatusChoises
from .services import render_to_pdf


class Index(LoginRequiredMixin, View):
    """Return index html page"""
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request):
        return render(request, 'main/index.html')


class DocumentsView(LoginRequiredMixin, ListView):
    """Return a list of all agreemant forms"""
    model = Document
    template_name = 'main/all_forms.html'
    context_object_name = 'documents'
    login_url = 'login'
    redirect_field_name = 'login'

    def get_queryset(self) -> list:
        documents = self.model.objects.all().select_related('car')
        return documents


class DocumentPageView(LoginRequiredMixin, DetailView):
    """Return a single agreemant form page"""
    model = Document
    template_name = 'main/form_page.html'
    context_object_name = 'document'
    login_url = 'login'
    redirect_field_name = 'login'


class ViewPDF(LoginRequiredMixin, View):
    """Generate PDF file in browser without autodownloading"""
    login_url = 'login'
    redirect_field_name = 'login'

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        context = {'document': document}
        pdf = render_to_pdf('main/pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class DocumentCreateView(LoginRequiredMixin, FormView):
    """Create a new document"""
    template_name = 'main/create_form.html'
    form_class = DocumentCreateForm
    success_url = reverse_lazy('list_documents')
    login_url = 'login'
    redirect_field_name = 'login'

    def form_valid(self, form):
        """Validate data and save one"""
        form.save()
        return super().form_valid(form)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete object from db"""
    model = Document
    template_name = 'main/delete_form.html'
    context_object_name = 'document'
    success_url = reverse_lazy('list_documents')
    login_url = 'login'
    redirect_field_name = 'login'


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    """Update object"""
    model = Document
    template_name = 'main/update_form.html'
    context_object_name = 'document'
    form_class = DocumentCreateForm
    login_url = 'login'
    redirect_field_name = 'login'

    def get_success_url(self):
        """URL to redirect after update"""
        return reverse_lazy('document_page', kwargs={'pk': self.object.id})


@login_required(login_url='login')
def finish_document(request, pk):
    """Change document status"""
    document = get_object_or_404(Document, pk=pk)
    document.status = DocumentStatusChoises.FINISHED
    document.save()
    return redirect('list_documents')
