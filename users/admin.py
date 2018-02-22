from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .form import CustomUserChangeForm, CustomUserCreationForm
from .models import Employee, VacationModel, VacationEdit
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime
user = get_user_model()

# Register your models here.


def metre_a_jour(modeladmin, request, queryset):
    current_year = datetime.datetime.now()
    for item in queryset:
        if VacationEdit.objects.filter(user=item, edited_year=current_year.year).exists():
            continue
        item.calculconge = item.calculconge + item.nombreConge
        VacationEdit.objects.create(user=item, edited_year=current_year.year)
        item.save()

metre_a_jour.short_description = "Metre a jour les Conges"


class CustomUserAdmin(UserAdmin):
    actions = [metre_a_jour]
    model = Employee
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = ((None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'matricule', 'cnss', 'service', 'post', 'chef1', 'chef2', 'nombreConge', 'type')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'last_login', 'is_superuser',)}))


admin.site.register(user, CustomUserAdmin)
admin.site.register(VacationModel)
