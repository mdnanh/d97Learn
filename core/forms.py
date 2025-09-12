from django import forms
from .models import NewsAndEvents, Session, Semester, SEMESTER
from django.utils.translation import gettext_lazy as _

# news and events
class NewsAndEventsForm(forms.ModelForm):
    class Meta:
        model = NewsAndEvents
        fields = (
            "title",
            "summary",
            "posted_as",
        )
        labels = {
                "title": _("Title"),
                "summary": _("Summary"),
                "posted_as": _("Post as"),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        self.fields["posted_as"].widget.attrs.update({"class": "form-control"})


class SessionForm(forms.ModelForm):
    next_session_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "date",
            }
        ),
        required=True,
        label= _("Next Session Begins"),
    )

    class Meta:
        model = Session
        fields = ["session", "is_current_session", "next_session_begins"]
        labels = {
            "session": _("Session"),
            "is_current_session": _("Is Current Session?"),
            "next_session_begins": _("Next Session Begins"),
        }

class SemesterForm(forms.ModelForm):
    semester = forms.CharField(
        widget=forms.Select(
            choices=SEMESTER,
            attrs={
                "class": "browser-default custom-select",
            },
        ),
        label= _("Semester"),
    )
    is_current_semester = forms.CharField(
        widget=forms.Select(
            choices=((True, "Yes"), (False, "No")),
            attrs={
                "class": "browser-default custom-select",
            },
        ),
        label= _("is current semester?"),
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "browser-default custom-select",
            }
        ),
        required=True,
        label= _("Session"),
    )

    next_semester_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
        required=True,
        label= _("Next Semester Begins"),
    )

    class Meta:
        model = Semester
        fields = ["semester", "is_current_semester", "session", "next_semester_begins"]
        labels = {
            "semester": _("Semester"),
            "is_current_semester": _("Is Current Semester?"),
            "session": _("Session"),
            "next_semester_begins": _("Next Semester Begins"),
        }
