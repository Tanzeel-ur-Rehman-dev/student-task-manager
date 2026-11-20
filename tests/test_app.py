import os
import tempfile
import unittest
from app import app

class StudentTaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        import app as app_module
        self.original_db = app_module.DB_PATH
        app_module.DB_PATH = app_module.Path(self.temp_db.name)
        app_module.init_db()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        import app as app_module
        app_module.DB_PATH = self.original_db
        os.unlink(self.temp_db.name)

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My Task Manager", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_add_task(self):
        response = self.client.post("/add", data={
            "title": "Finish lab report", "subject": "Software Engineering",
            "due_date": "2026-12-01", "priority": "High"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Finish lab report", response.data)

if __name__ == "__main__":
    unittest.main()
