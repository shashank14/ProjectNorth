from django.conf.urls import url
from .views import login_view,logout_view,register_view

urlpatterns = [
url(r'^$',login_view,name='login'),
url(r'^login/$',login_view,name='login'),
url(r'^logout/$',logout_view,name='logout'),
url(r'^signup/$',register_view,name='signup')
]
