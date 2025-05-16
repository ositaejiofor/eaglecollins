from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


# URL configuration for the blog app
urlpatterns = [
    path('', views.home, name='blog_home'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('category/<str:category>/', views.posts_by_category, name='posts_by_category'),
    path('about/', views.about, name='about'),
    path('products/', views.products_view, name='blog/products'),
    path('services/', views.services_view, name='blog/services'),
    path('services/', views.services_view, name='blog/multi-tech'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
