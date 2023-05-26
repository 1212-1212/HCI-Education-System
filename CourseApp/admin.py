from django.contrib import admin
from .models import *


class LearnerAdmin(admin.ModelAdmin):
    list_display = ["user_name", "email", "birth_date"]
    list_filter = ["birth_date", "first_name", "last_name"]
    search_fields = ["id", "birth_date", "first_name", "last_name"]
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


class InstructorAdmin(admin.ModelAdmin):
    list_display = ["user_name", "email", "birth_date"]
    list_filter = ["birth_date", "first_name", "last_name", "degree"]
    search_fields = ["birth_date", "first_name", "last_name", "degree"]
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    list_filter = ["name", "instructors", "users"]
    search_fields = ["instructors", "users"]
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.instructors

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.instructors


class LessonAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.course.instructors

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.course.instructors

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.course.instructors


class EnrollmentAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.course.instructors

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.course.instructors

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.course.instructors


class ChoiceAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.question.course.instructors

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.question.course.instructors

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or obj and request.user in obj.question.course.instructors

class PostAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
