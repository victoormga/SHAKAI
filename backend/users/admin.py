from django.contrib import admin
from .models import User, Profile

# Registra el modelo User y Profile en el panel de administración
admin.site.register(User)
admin.site.register(Profile)