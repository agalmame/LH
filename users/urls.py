from django.urls import path
from . import views

"""urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]"""
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('conge/addVacation', views.CreateVacation, name='addvacation'),
    path('conge/listvacation/', views.ListVacation.as_view(), name='listvacation'),
    path('conge/<int:pk>/congedetail', views.DetailVacation.as_view(), name='congedetail'),
    path('conge/<int:pk>/congemodifier', views.UpdateVacation.as_view(), name='congemodifier'),
    path('conge/<int:pk>/congesupprimer', views.DeleteVacation.as_view(), name='congesupprimer'),
    path('conge/lesdemande', views.SubordinateListView.as_view(), name='lesdemande'),
    path('conge/<int:pk>/congereagire', views.ReactVacationView.as_view(), name='congereagire'),
    path('conge/<int:pk>/attestation', views.AttestationView.as_view(), name='attestation')
]
