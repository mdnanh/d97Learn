# course/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from result.models import TakenCourse
from accounts.models import Student

@receiver(post_save, sender=Course)
def auto_enroll_students_to_course(sender, instance, created, **kwargs):
    """
    Signal này sẽ tự động chạy mỗi khi một Khóa học được lưu.
    Nếu khóa học vừa được TẠO MỚI, nó sẽ tự động ghi danh
    tất cả các sinh viên có cùng Level.
    """
    # Chỉ chạy khi một khóa học vừa được TẠO MỚI (created=True)
    # và khóa học đó có chỉ định một Level cụ thể.
    if created and instance.level:
        # 1. Lấy Level của khóa học mới
        course_level = instance.level
        
        # 2. Tìm tất cả các sinh viên có cùng Level
        students_to_enroll = Student.objects.filter(level=course_level)
        
        # 3. Tạo các bản ghi TakenCourse hàng loạt
        taken_courses_to_create = []
        for student in students_to_enroll:
            # Tạo một đối tượng TakenCourse trong bộ nhớ
            taken_course = TakenCourse(student=student, course=instance)
            taken_courses_to_create.append(taken_course)
        
        # Dùng bulk_create để tạo tất cả các bản ghi chỉ bằng 1 câu lệnh SQL,
        # rất hiệu quả. ignore_conflicts=True để tránh lỗi nếu bản ghi đã tồn tại.
        TakenCourse.objects.bulk_create(taken_courses_to_create, ignore_conflicts=True)
        
        print(f"Đã tự động ghi danh {len(students_to_enroll)} sinh viên vào khóa học '{instance.title}'.")