from django.contrib import admin
from .models import Course, Lesson

admin.site.register(Course)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "created_at")
    list_filter = ("course",)