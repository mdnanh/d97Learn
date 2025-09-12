from django.contrib import admin
from .models import User, Student, Parent


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "get_full_name",
        "username",
        "email",
        "is_active",
        "is_student",
        "is_lecturer",
        "is_parent",
        "is_staff",
        "get_student_classes",
        "get_level",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_lecturer",
        "is_parent",
        "is_staff",
    ]

    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"

    @admin.display(description='Trạm')
    def get_student_classes(self, obj):
        if hasattr(obj, 'student'):
            # Dùng get_classes_display() để lấy tên hiển thị thay vì giá trị ('tsgnscn')
            return obj.student.get_classes_display() 
        return "N/A" # Hoặc None
    @admin.display(description='Level')
    def get_level(self, obj):
        if hasattr(obj, 'student'):
            # Dùng get_level_display() để lấy tên hiển thị thay vì giá trị ('Bachelor')
            return obj.student.get_level_display() 
        return "N/A" # Hoặc None

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Parent)
