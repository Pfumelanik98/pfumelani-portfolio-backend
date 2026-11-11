from django.test import TestCase, override_settings


class HomeRedirectTests(TestCase):
    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_home_redirects_to_api_root(self):
        response = self.client.get("/")

        self.assertRedirects(response, "/api/v1/")

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_admin_login_page_loads(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)

    def test_admin_stylesheet_is_available(self):
        response = self.client.get("/static/admin/css/base.css")

        self.assertEqual(response.status_code, 200)
