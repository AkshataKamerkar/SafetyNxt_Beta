from django.contrib import admin
from .models import Contact,Route

# Register your models
admin.site.register(Contact)


class RouteInfo(admin.ModelAdmin):
    pass

admin.site.register(Route,RouteInfo)
