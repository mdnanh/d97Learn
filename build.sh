#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Bắt đầu quá trình build..."

# Cài đặt các thư viện từ requirements.txt
pip install -r requirements.txt

# Thu thập tất cả các file tĩnh (CSS, JS) vào thư mục STATIC_ROOT
python manage.py collectstatic --no-input

# Áp dụng các thay đổi (migrations) vào database
python manage.py migrate

echo "Quá trình build đã hoàn tất!"