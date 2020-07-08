from django.contrib import admin
from django.urls import path,include
from share.views import HomeView, DisplayView, MyView, SearchView,RegisterView,IndexView,down_file


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',IndexView.as_view(),name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('s/<code>', DisplayView.as_view(), name='display'),
    path('my/', MyView.as_view(), name='my'),
    path('download/<code>',down_file,name='download'),
    path('search/', SearchView.as_view(), name='search'),
    path('',RegisterView.as_view(),name='register'),
    path('',include('django.contrib.auth.urls')),
]