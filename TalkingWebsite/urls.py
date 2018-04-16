from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from . import views
from django.contrib import admin
# from django.urls import path
from django.views.generic import RedirectView


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^talkingtree/',  include('talkingtree.urls')),
]

urlpatterns += [
    url('', RedirectView.as_view(url='/talkingtree/')),
]
