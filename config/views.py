# config/views.py
import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required

@login_required # Chỉ người dùng đã đăng nhập mới được xem/tải file
def protected_media_view(request, path):
    """
    Một view an toàn để phục vụ media files trên production,
    đọc file từ MEDIA_ROOT (trỏ đến Persistent Disk).
    """
    # Ghép đường dẫn an toàn
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Kiểm tra để đảm bảo người dùng không yêu cầu file ngoài thư mục MEDIA_ROOT
    if not os.path.normpath(file_path).startswith(os.path.normpath(settings.MEDIA_ROOT)):
        raise Http404("Permission denied")

    try:
        # Mở file ở chế độ đọc nhị phân ('rb') và trả về cho trình duyệt
        return FileResponse(open(file_path, 'rb'))
    except FileNotFoundError:
        # Nếu file không tồn tại trên disk, trả về lỗi 404
        raise Http404("File does not exist")