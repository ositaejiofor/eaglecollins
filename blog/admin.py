from django.contrib import admin
from .models import Blog, Category, Comment
from .models import Product, Service


# Registering Blog model



admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(Service)
