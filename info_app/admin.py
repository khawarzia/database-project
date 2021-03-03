from django.contrib import admin
from .models import department,sections_offered,course,result

admin.site.register(department)
admin.site.register(sections_offered)
admin.site.register(course)
admin.site.register(result)