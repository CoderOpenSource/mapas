from django.contrib import admin

# Register your models here.
from .models import CustomUser, Cliente, Taller, Tecnico
admin.site.register(CustomUser)
admin.site.register(Cliente)
admin.site.register(Taller)
admin.site.register(Tecnico)
