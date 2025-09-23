from django.apps import AppConfig


class CourseConfig(AppConfig):
    name = "course"
    def ready(self):
        # Dòng này sẽ import và đăng ký các signal của em
        import course.signals