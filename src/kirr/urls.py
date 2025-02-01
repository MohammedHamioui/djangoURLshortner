from django.contrib import admin
from django.urls import path, re_path

from shortener.views import kirr_redirect_view, URLRedirectView, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', HomeView.as_view()),
    #re_path(r'^a/(?P<shortcode>[\w-]{6,15})/$', kirr_redirect_view),
    re_path(r'^(?P<shortcode>[\w-]{6,15})/$', URLRedirectView.as_view(), name="shortcode"),
]