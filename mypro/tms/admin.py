from django.contrib import admin
from .models import Teacher, Users, Subject

admin.site.site_header = "Teacher Management System Admin"
admin.site.site_title = "TMS Admin Portal"
admin.site.index_title = "Welcome to the TMS Portal"

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("tname", "display_subjects", "qualification", "contact", "status")

    def display_subjects(self, obj):
        return ", ".join([s.name for s in obj.subjects.all()])
    display_subjects.short_description = 'Subjects'

admin.site.register(Teacher, TeacherAdmin)

class UsersAdmin(admin.ModelAdmin):
    list_display = ("names", "username", "password")

admin.site.register(Users, UsersAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(Subject, SubjectAdmin)

