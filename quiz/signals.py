from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Quiz, Question

# @receiver(pre_delete, sender=Quiz) # Cách này cũng được nhưng m2m_changed an toàn hơn
# def delete_questions_on_quiz_delete(sender, instance, **kwargs):
#     """
#     Trước khi một Quiz bị xóa, hãy xóa tất cả các Question liên quan đến nó.
#     CẢNH BÁO: Điều này sẽ xóa vĩnh viễn Question, ngay cả khi nó đang được dùng
#     trong một Quiz khác.
#     """
#     for question in instance.question_set.all():
#         question.delete()

@receiver(m2m_changed, sender=Question.quiz.through)
def question_removed_from_quiz(sender, instance, action, pk_set, **kwargs):
    """
    Một giải pháp AN TOÀN HƠN và TỐT HƠN:
    Khi một câu hỏi bị gỡ khỏi TẤT CẢ các bài quiz mà nó thuộc về,
    hãy xóa vĩnh viễn câu hỏi đó.
    """
    if action == "post_remove" or action == "post_clear":
        # pk_set chứa ID của các bài quiz vừa bị gỡ khỏi câu hỏi
        # instance ở đây là đối tượng Question
        
        # Kiểm tra xem câu hỏi này còn thuộc về bài quiz nào khác không
        if instance.quiz.count() == 0:
            # Nếu không còn thuộc về bài quiz nào, nó đã trở thành "mồ côi"
            # Bây giờ chúng ta có thể xóa nó một cách an toàn
            instance.delete()