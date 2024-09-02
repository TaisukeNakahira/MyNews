from django.contrib import admin
from .models import Articles, Favorites

# Register your models here.
admin.site.register(Articles)
admin.site.register(Favorites)
