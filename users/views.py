from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, DetailView
from .models import VacationModel, Employee
from .form import VacationCreateForm, ReactVacationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from datetime import datetime


# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'


def CreateVacation(request):
    form = VacationCreateForm(request.POST or None)
    error_message = ""
    if form.is_valid():
        dateD = request.POST.get("dateDebut")
        dateF = request.POST.get("dateFin")
        fmt = '%m/%d/%Y'
        dd = datetime.strptime(str(dateD), fmt)
        df = datetime.strptime(str(dateF), fmt)
        dateDiff = (df - dd).days
        q = Employee.objects.get(id=request.user.id)
        if dateDiff < q.calculconge:
            if dateDiff > 0:
                instance = form.save(commit=False)
                instance.employee = request.user
                instance.save()
                return redirect('listvacation')
            else:
                error_message = "La date de fin doit etre la superieur"

        else:
            error_message = "Votre demande depasse votre droit ({} jour)".format(str(q.calculconge))
    context = {
        "form": form,
        "error_message": error_message,
    }
    return render(request, 'conge.html', context)


class ListVacation(LoginRequiredMixin, ListView):
    model = VacationModel
    template_name = 'congelist.html'
    login_url = 'login'

    def get_queryset(self):
        qs = VacationModel.objects.filter(employee=self.request.user)
        return qs


class DetailVacation(LoginRequiredMixin, DetailView):
    model = VacationModel
    template_name = 'congedetail.html'
    login_url = 'login'


class UpdateVacation(LoginRequiredMixin, UpdateView):
    model = VacationModel
    template_name = 'congemodifier.html'
    fields = ['dateDebut', 'dateFin', 'nature']
    login_url = 'login'
    success_url = '/conge/listvacation'

    def form_valid(self, form):
        dateD = self.request.POST.get("dateDebut")
        dateF = self.request.POST.get("dateFin")
        fmt = '%Y-%m-%d'
        dd = datetime.strptime(str(dateD), fmt)
        df = datetime.strptime(str(dateF), fmt)
        dateDiff = (df - dd).days
        q = Employee.objects.get(id=self.request.user.id)
        if dateDiff < q.calculconge:
            if dateDiff > 0:
                instance = form.save(commit=False)
                instance.employee = self.request.user
                instance.save()
                return super(UpdateVacation, self).form_valid(form)
            else:
                content = "La date de fin doit etre la superieur"
        else:
            content = "Votre demande depasse votre droit ({} jour)".format(str(q.calculconge))
        context = {
            "content": content,
            "form": form
        }
        return render(self.request, 'congemodifier.html', context)




class DeleteVacation(LoginRequiredMixin, DeleteView):
    model = VacationModel
    template_name = 'congesupprimer.html'
    login_url = 'login'
    success_url = reverse_lazy('home')


class SubordinateListView(LoginRequiredMixin, ListView):
    model = VacationModel
    template_name = 'Lesdemande.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = []
        emp = Employee.objects.filter(Q(chef1=self.request.user) | Q(chef2=self.request.user))
        if emp.exists():
            for e in emp:
                queryset += VacationModel.objects.filter(employee=e.pk).filter(valide__iexact='EN COURS')
            return queryset


class ReactVacationView(LoginRequiredMixin, UpdateView):
    form_class = ReactVacationForm
    model = VacationModel
    template_name = 'congereagire.html'
    login_url = 'login'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.par = self.request.user.first_name + ' ' + self.request.user.last_name
        return super(ReactVacationView, self).form_valid(form)


class AttestationView(LoginRequiredMixin, DetailView):
    model = VacationModel
    login_url = 'login'
    template_name = 'attestation.html'
