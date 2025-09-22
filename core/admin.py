# core/admin.py
from django.contrib import admin
from django.utils.html import format_html # Import công cụ để tạo HTML an toàn
from modeltranslation.admin import TranslationAdmin
from .models import NewsAndEvents


@admin.register(NewsAndEvents) # Cách đăng ký hiện đại và gọn gàng hơn
class NewsAndEventsAdmin(TranslationAdmin):
    # 1. Tùy chỉnh các cột hiển thị trên trang danh sách
    list_display = ('title', 'posted_as', 'upload_time', 'display_attachment_link')
    
    # 2. Thêm bộ lọc ở thanh bên phải
    list_filter = ('posted_as', 'upload_time')
    
    # 3. Thêm một ô tìm kiếm
    search_fields = ('title', 'summary')
    
    # 4. Tạo một phương thức tùy chỉnh để hiển thị link tải file
    def display_attachment_link(self, obj):
        # Kiểm tra xem tin tức này có file đính kèm không
        if obj.attachment:
            # Tạo một thẻ <a> HTML trỏ đến URL của file
            return format_html('<a href="{0}" target="_blank">Tải về</a>', obj.attachment.url)
        # Nếu không có file, hiển thị một dấu gạch ngang
        return "—"
    
    # Đặt tên cho cột mới trong giao diện admin
    display_attachment_link.short_description = "File đính kèm"

# Dòng admin.site.register(...) cũ không cần nữa vì đã có @admin.register