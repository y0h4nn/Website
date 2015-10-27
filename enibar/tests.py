from django.test import TestCase, Client
from .models import Note
from decimal import Decimal


class TestEnibarImport(TestCase):
    def setUp(self):
        self.client = Client()
        super().setUp()

    def test_note_import_404(self):
        response = self.client.options("/enibar/note/", "{}")
        self.assertEqual(response.status_code, 404)
        response = self.client.put("/enibar/note", "pouet")
        self.assertEqual(response.status_code, 404)

    def test_import_note_put(self):
        response = self.client.put("/enibar/note", '{"id": 1, "nickname": "coucou", "mail": "test@test.fr", "note": 52.2}')
        self.assertEqual(response.status_code, 200)
        note = Note.objects.get(foreign_id=1)
        self.assertEqual(note.foreign_id, 1)
        self.assertEqual(note.nickname, "coucou")
        self.assertEqual(note.mail, "test@test.fr")
        self.assertEqual(note.note, Decimal("52.2"))
        response = self.client.put("/enibar/note", '{"id": 1, "nickname": "coucou", "mail": "test@test.fr", "note": 50.2}')
        self.assertEqual(response.status_code, 200)
        note = Note.objects.get(foreign_id=1)
        self.assertEqual(note.foreign_id, 1)
        self.assertEqual(note.nickname, "coucou")
        self.assertEqual(note.mail, "test@test.fr")
        self.assertEqual(note.note, Decimal("50.2"))

    def test_import_note_delete(self):
        Note.objects.create(foreign_id=2, nickname="toto", mail="coucou@test.fr", note=Decimal("10"))
        response = self.client.delete("/enibar/note", '{"id": 2}')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(foreign_id=2)

