from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth_app.models import User
from .models import Course, CourseMaterial


class CourseMaterialAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="adminpass123",
            role="admin"
        )

        self.employee_user = User.objects.create_user(
            email="employee@example.com",
            password="employeepass123",
            role="employee"
        )

        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.employee_token = str(RefreshToken.for_user(self.employee_user).access_token)

        self.course = Course.objects.create(
            title="Course 1",
            description="Test course",
            status="draft"
        )

    def test_admin_can_upload_pdf_to_course(self):
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"%PDF-1.4 test content",
            content_type="application/pdf"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            f"/api/courses/{self.course.id}/materials/",
            {"file": pdf_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseMaterial.objects.count(), 1)
        self.assertEqual(response.data["file_type"], "pdf")
        self.assertEqual(response.data["filename"], "test.pdf")

    def test_admin_can_upload_audio_to_course(self):
        audio_file = SimpleUploadedFile(
            "audio.mp3",
            b"fake audio bytes",
            content_type="audio/mpeg"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            f"/api/courses/{self.course.id}/materials/",
            {"file": audio_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseMaterial.objects.count(), 1)
        self.assertEqual(response.data["file_type"], "audio")
        self.assertEqual(response.data["filename"], "audio.mp3")

    def test_admin_cannot_upload_invalid_file_type(self):
        txt_file = SimpleUploadedFile(
            "notes.txt",
            b"plain text",
            content_type="text/plain"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            f"/api/courses/{self.course.id}/materials/",
            {"file": txt_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(CourseMaterial.objects.count(), 0)

    def test_admin_cannot_upload_file_above_10mb(self):
        big_file = SimpleUploadedFile(
            "big.pdf",
            b"a" * (10 * 1024 * 1024 + 1),
            content_type="application/pdf"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            f"/api/courses/{self.course.id}/materials/",
            {"file": big_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(CourseMaterial.objects.count(), 0)

    def test_admin_can_list_course_materials(self):
        CourseMaterial.objects.create(
            course=self.course,
            file=SimpleUploadedFile(
                "test.pdf",
                b"%PDF-1.4 test content",
                content_type="application/pdf"
            ),
            file_type="pdf",
            filename="test.pdf"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(f"/api/courses/{self.course.id}/materials/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_employee_cannot_upload_course_material(self):
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"%PDF-1.4 test content",
            content_type="application/pdf"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.employee_token}")
        response = self.client.post(
            f"/api/courses/{self.course.id}/materials/",
            {"file": pdf_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_list_unassigned_course_materials(self):
        CourseMaterial.objects.create(
            course=self.course,
            file=SimpleUploadedFile(
                "test.pdf",
                b"%PDF-1.4 test content",
                content_type="application/pdf"
            ),
            file_type="pdf",
            filename="test.pdf"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.employee_token}")
        response = self.client.get(f"/api/courses/{self.course.id}/materials/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_upload_course_material(self):
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"%PDF-1.4 test content",
            content_type="application/pdf"
        )

        response = self.client.post(
            f"/api/courses/{self.course.id}/materials/",
            {"file": pdf_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_list_course_materials(self):
        response = self.client.get(f"/api/courses/{self.course.id}/materials/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_to_nonexistent_course_returns_404(self):
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"%PDF-1.4 test content",
            content_type="application/pdf"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            "/api/courses/9999/materials/",
            {"file": pdf_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_materials_for_nonexistent_course_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/courses/9999/materials/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)