from django.contrib import admin

from .models import Story, Project, Organization
from django.db import models


from tinymce.widgets import TinyMCE

  
class textEditorAdmin(admin.ModelAdmin):
   list_display = ["title"]
   formfield_overrides = {
   models.TextField: {'widget': TinyMCE()}
   }

admin.site.register(Story, textEditorAdmin)
admin.site.register(Project)
admin.site.register(Organization)