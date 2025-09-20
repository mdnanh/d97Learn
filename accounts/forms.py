from django import forms
from django.db import transaction
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth.forms import PasswordResetForm
from course.models import Program
from .models import User, Student, Parent, RELATION_SHIP, LEVEL, GENDERS, CLASSES
from django.utils.translation import gettext_lazy as _


class StaffAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("Username"),
        required=False,
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("First name"),
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("Last Name"),
    )

    gender = forms.CharField(
        max_length=20,
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
        label= _("Gender")
    )
    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
        label= _("Level"),
    )
    classes = forms.CharField(
        widget=forms.Select(
            choices=CLASSES,
            attrs={
                "class": "browser-default custom-select form-control",
            },
    ),
        label= _("Classes")
    )
    # address = forms.CharField(
    #     max_length=30,
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "text",
    #             "class": "form-control",
    #         }
    #     ),
    #     label= _("Address"),
    # )

    # phone = forms.CharField(
    #     max_length=30,
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "text",
    #             "class": "form-control",
    #         }
    #     ),
    #     label= _("Mobile No."),
    # )

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Email",
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label= _("Password"),
        required=False,
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label= _("Password Confirmation"),
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        # user.phone = self.cleaned_data.get("phone")
        # user.address = self.cleaned_data.get("address")
        user.email = self.cleaned_data.get("email")

        if commit:
            user.save()
            User.objects.create(
                user=user,
                level=self.cleaned_data.get("level"),
                program=self.cleaned_data.get("program"),
                classes=self.cleaned_data.get("classes"),
            )

        return user


class StudentAddForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("First name"),
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("Last name"),
    )

    gender = forms.CharField(
        max_length=20,
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
        label= _("Gender"),
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}), 
        required=True, label="Ngày/tháng/năm sinh")

    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
        label= _("Level"),
    )
    classes = forms.CharField(
        widget=forms.Select(
            choices=CLASSES,
            attrs={
                "class": "browser-default custom-select form-control",
            },
    ),
        label= _("Classes")
    )
    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label= _("Program"),
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label= _("Email Address"),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'level', 'classes']

    @transaction.atomic()
    def save(self, commit=True):
        # user = super().save(commit=False)
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        dob = self.cleaned_data.get("date_of_birth")
        email= self.cleaned_data.get("email")
        classes = self.cleaned_data.get("classes")
        level = self.cleaned_data.get("level")
        program = self.cleaned_data.get("program")
        # --- ÁP DỤNG QUY TẮC CỦA EM ---
        
        # 1. Tạo Tên đăng nhập từ Họ và Tên
        # Ví dụ: "Nguyễn Văn" + " " + "A" -> "Nguyễn Văn A"
        generated_username  = f"{last_name} {first_name}"
        
        # Tạo và ghi đè mật khẩu (dùng set_password để mã hóa)
        generated_password = dob.strftime('%d%m%Y')        
        # --- KẾT THÚC ÁP DỤNG QUY TẮC ---
        level_map = {
            'Sĩ quan': 'SQ',
            'Quân nhân chuyên nghiệp': 'CN',  
            'Chiến sĩ': 'CS',  
        }
        classes_map = {
            'TS-GN Sóng ngắn': 'TSGNSN',
            'TS-GN Sóng cực ngắn': 'TSGNSCN',
            'TS-GN ĐK&NTNB': 'TSGNĐK&NTNB',
            'Trạm Sửa chữa': 'TSC',
        }
        level_prefix = level_map.get(level, level.upper()) # Lấy từ map, nếu không có thì viết hoa

        # Ví dụ: 'tsgnscn' -> 'TSGNSCN'
        classes_prefix = classes_map.get(classes, classes.upper())

        # 2. Tìm số thứ tự tiếp theo
        # Tạo ra phần đầu của ID để tìm kiếm, ví dụ: "TSGNSCN_CN"
        id_prefix = f"{classes_prefix}_{level_prefix}"
        
        # Đếm xem đã có bao nhiêu sinh viên có ID bắt đầu bằng tiền tố này
        sequence_count = Student.objects.filter(id_number__startswith=id_prefix).count()
        
        # Số thứ tự mới sẽ là số lượng hiện tại + 1
        new_sequence = sequence_count + 1
        
        # 3. Tạo ID No. hoàn chỉnh
        # Dùng :02d để đảm bảo số thứ tự luôn có 2 chữ số (01, 02, ..., 10)
        generated_id_number = f"{id_prefix}_{new_sequence:02d}"
        if commit:
            # Dùng User.objects.create_user để tạo user và mã hóa mật khẩu
            user = User.objects.create_user(
                username=generated_username,
                password=generated_password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                is_student=True
            )
            # Tạo đối tượng Student liên quan
            Student.objects.create(
                student=user,
                level=level,
                id_number=generated_id_number,
                classes=classes,
                program=program
            )

        return user


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label= _("Email Address"),
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("First Name"),
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("Last Name"),
    )

    gender = forms.CharField(
        max_length=20,
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
        label= _("gender")
    )

    # phone = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "text",
    #             "class": "form-control",
    #         }
    #     ),
    #     label= _("Phone No."),
    # )
    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
        label= _("Level"),
    )
    classes = forms.CharField(
        widget=forms.Select(
            choices=CLASSES,
            attrs={
                "class": "browser-default custom-select form-control",
            },
    ),
        label= _("Classes")
    )
    # address = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "text",
    #             "class": "form-control",
    #         }
    #     ),
    #     label= _("Address / city"),
    # )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            # "phone",
            "level",
            "classes",
            # "address",
            "picture",
        ]

        labels = {
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "gender": _("Gender"),
            "email": _("Email Address"),
            # "phone": _("Phone No."),
            # "address": _("Address / city"),
            "level": _("Level"),
            "classes": _("Classes"),
            "picture": _("Profile Picture"),
        }


class ProgramUpdateForm(UserChangeForm):
    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label= _("Program"),
    )

    class Meta:
        model = Student
        fields = ["program"]
        labels = {
            "program": _("Program"),
        }

class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-mail address. "
            self.add_error("email", msg)
            return email


class ParentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("Username"),
    )
    # address = forms.CharField(
    #     max_length=30,
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "text",
    #             "class": "form-control",
    #         }
    #     ),
    #     label= _("Address"),
    # )

    # phone = forms.CharField(
    #     max_length=30,
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "text",
    #             "class": "form-control",
    #         }
    #     ),
    #     label= _("Mobile No."),
    # )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label= _("First name"),
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last name",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label= _("Email Address"),
    )

    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label= _("Student"),
    )

    relation_ship = forms.CharField(
        widget=forms.Select(
            choices=RELATION_SHIP,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password",
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password Confirmation",
    )

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        # user.address = self.cleaned_data.get("address")
        # user.phone = self.cleaned_data.get("phone")
        user.email = self.cleaned_data.get("email")
        user.save()
        parent = Parent.objects.create(
            user=user,
            student=self.cleaned_data.get("student"),
            relation_ship=self.cleaned_data.get("relation_ship"),
        )
        parent.save()
        return user
