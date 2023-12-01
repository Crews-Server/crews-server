# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient, APITestCase
# from rest_framework import status
# from django.urls import reverse
# from datetime import datetime, timedelta

# from table.models import User, Apply, Post, Crew, Evaluation


# class EvaluationTests(APITestCase):
#     def setUp(self):
#         # Create API client
#         self.client = APIClient()

#         # Get the user model
#         User = get_user_model()

#         # Create an administrator user
#         self.admin_user = User.objects.create_user(
#             email="admin@sogang.ac.kr",
#             name="Admin",
#             password="adminpassword",
#             sogang_mail="adminmail@sogang.ac.kr",
#             student_number="20220002",
#             first_major="Computer Science",
#         )
#         self.admin_user.is_staff = True
#         self.admin_user.save()

#         # Create test user
#         self.user = User.objects.create_user(
#             email="test@sogang.ac.kr",
#             name="Test User",
#             password="testpassword",
#             sogang_mail="testmail@sogang.ac.kr",
#             student_number="20220001",
#             first_major="Computer Science",
#         )

#         # Create test crew
#         crew = Crew.objects.create(
#             crew_name="Test Crew", description="Test Crew Description"
#         )

#         # Set up dates for the post
#         current_time = datetime.now()
#         self.post = Post.objects.create(
#             title="Test Post",
#             content="Test Post Content",
#             crew_id=crew.id,
#             apply_start_date=current_time,
#             apply_end_date=current_time + timedelta(days=7),
#             document_result_date=current_time + timedelta(days=14),
#         )

#         # Create an application
#         self.apply = Apply.objects.create(user=self.user, post=self.post)

#         # Create an evaluation
#         self.evaluation = Evaluation.objects.create(
#             user=self.user, apply=self.apply, score=5, comment="Test Comment"
#         )

#         # Login as admin
#         # self.client.login(email="admin@sogang.ac.kr", password="adminpassword")
#         login_successful = self.client.login(username="admin", password="adminpassword")
#         if not login_successful:
#             raise ValueError("Admin login failed in test setup")

#     def test_get_applied_user_list(self):
#         url = reverse("get-applied-user-list") + f"?post_id={self.post.id}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_document_pass_count(self):
#         url = reverse("first-round-pass-count", args=[self.post.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_user_evaluation(self):
#         url = reverse("user-evaluation", args=[self.user.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_document_pass_post(self):
#         url = reverse("document-pass-post")
#         data = {"post_id": self.post.id, "applicant_id": self.user.id}
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_final_pass_post(self):
#         url = reverse("final-pass-post")
#         data = {"post_id": self.post.id, "applicant_id": self.user.id}
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_application_details(self):
#         url = reverse("application-details", args=[self.apply.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_admin_evaluation_status(self):
#         url = reverse("admin-evaluation-status", args=[self.user.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_evaluation(self):
#         url = reverse("update-evaluation", args=[self.evaluation.id])
#         data = {"score": 10, "comment": "Updated comment"}
#         response = self.client.patch(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
