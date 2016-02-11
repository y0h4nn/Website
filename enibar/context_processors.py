from .models import Note

def check_note(request):
    note = None
    if request.method in ["POST", "GET"] and request.user.is_active:
        note = Note.get_note(request.user)
    return {'user_note': note}
