from django.contrib import admin
from .models import CommunityCentre

# Register your models here.
@admin.register(CommunityCentre)
class CommunityCentreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}