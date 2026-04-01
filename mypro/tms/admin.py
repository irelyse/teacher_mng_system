from django.contrib import admin
from .models import Teacher, Users

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("tname", "display_subjects", "qualification", "contact", "status")

    def display_subjects(self, obj):
        return ", ".join([s.name for s in obj.subjects.all()])
    display_subjects.short_description = 'Subjects'

admin.site.register(Teacher, TeacherAdmin)

class UsersAdmin(admin.ModelAdmin):
    list_display = ("names", "username", "password")

admin.site.register(Users, UsersAdmin)
