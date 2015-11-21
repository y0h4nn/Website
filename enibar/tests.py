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

    def test_note_put_403(self):
        response = self.client.put("/enibar/note", '{"id": 1, "nickname": "coucou", "mail": "test@test.fr", "note": 52.2}')
        self.assertEqual(response.status_code, 403)

    def test_note_delete_403(self):
        response = self.client.delete("/enibar/note", '{"id": 2}')
        self.assertEqual(response.status_code, 403)

    def test_import_note_put(self):
        response = self.client.put("/enibar/note", '{"token": "changeme", "id": 1, "nickname": "coucou", "mail": "test@test.fr", "note": 52.2}')
        self.assertEqual(response.status_code, 200)
        note = Note.objects.get(foreign_id=1)
        self.assertEqual(note.foreign_id, 1)
        self.assertEqual(note.nickname, "coucou")
        self.assertEqual(note.mail, "test@test.fr")
        self.assertEqual(note.note, Decimal("52.2"))
        response = self.client.put("/enibar/note", '{"token": "changeme", "id": 1, "nickname": "coucou", "mail": "test@test.fr", "note": 50.2}')
        self.assertEqual(response.status_code, 200)
        note = Note.objects.get(foreign_id=1)
        self.assertEqual(note.foreign_id, 1)
        self.assertEqual(note.nickname, "coucou")
        self.assertEqual(note.mail, "test@test.fr")
        self.assertEqual(note.note, Decimal("50.2"))

    def test_import_note_delete(self):
        Note.objects.create(foreign_id=2, nickname="toto", mail="coucou@test.fr", note=Decimal("10"))
        response = self.client.delete("/enibar/note", '{"token": "changeme", "id": 2}')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(foreign_id=2)

    def test_get_note(self):
        Note.objects.create(foreign_id=2, nickname="toto", mail="coucou@test.fr", note=Decimal("10"))
        Note.objects.create(foreign_id=3, nickname="toto2", mail="cou@test.com", note=Decimal("11"))

        response = self.client.get("/enibar/note")
        self.assertEqual(response.json(), [{'note': '10.00', 'nickname': 'toto', 'foreign_id': 2, 'mail': 'coucou@test.fr'}, {'note': '11.00', 'nickname': 'toto2', 'foreign_id': 3, 'mail': 'cou@test.com'}])
        response = self.client.get("/enibar/note", {"foreign_id": 2})
        self.assertEqual(response.json(), [{'mail': 'coucou@test.fr', 'note': '10.00', 'nickname': 'toto', 'foreign_id': 2}])
        response = self.client.get("/enibar/note", {"pouet": 2})
        self.assertEqual(response.status_code, 404)

