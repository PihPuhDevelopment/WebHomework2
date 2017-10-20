from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.printparams),
    url(r'^', views.default)
]