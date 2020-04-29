"""urls.py tests"""
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.auth import views as auth_views
from ..views import (
    index, legals,
    register_view, login_view,
    search, results, detail,
    userpage, new_name, new_email,
    watchlist, load_favorite,
)

class TestUrls(SimpleTestCase):
    """test on urls.py with SimpleTestCase class"""

    def test_index_url_is_resolved(self):
        """test index_url"""
        url = reverse('foodSearch:index')
        self.assertEqual(resolve(url).func, index)

    def test_legals_url_is_resolved(self):
        """test legals_url"""
        url = reverse('foodSearch:legals')
        self.assertEqual(resolve(url).func, legals)

    def test_register_view_url_is_resolved(self):
        """test register_view"""
        url = reverse('foodSearch:register')
        self.assertEqual(resolve(url).func, register_view)

    def test_login_url_is_resolved(self):
        """test login_url"""
        url = reverse('foodSearch:login')
        self.assertEqual(resolve(url).func, login_view)

    def test_userpage_url_is_resolved(self):
        """test userpage_url"""
        url = reverse('foodSearch:userpage')
        self.assertEqual(resolve(url).func, userpage)

    def test_watchlist_url_is_resolved(self):
        """test watchlist_url"""
        url = reverse('foodSearch:watchlist')
        self.assertEqual(resolve(url).func, watchlist)

    def test_search_url_is_resolved(self):
        """test search_url"""
        url = reverse('foodSearch:search')
        self.assertEqual(resolve(url).func, search)

    def test_results_url_is_resolved(self):
        """test results_url"""
        url = reverse('foodSearch:results', args=[00000])
        self.assertEqual(resolve(url).func, results)

    def test_detail_url_is_resolved(self):
        """test detail_url"""
        url = reverse('foodSearch:detail', args=[00000])
        self.assertEqual(resolve(url).func, detail)

    def test_load_favorite_url_is_resolved(self):
        """test load_favorite"""
        url = reverse('foodSearch:load_favorite')
        self.assertEqual(resolve(url).func, load_favorite)

    def test_new_name_is_resolved(self):
        """test new_name"""
        url = reverse('foodSearch:new_name')
        self.assertEqual(resolve(url).func, new_name)

    def test_new_email_is_resolved(self):
        """test new_email"""
        url = reverse('foodSearch:new_email')
        self.assertEqual(resolve(url).func, new_email)

    def test_password_reset_is_resolved(self):
        """test password_reset"""
        url = reverse('foodSearch:password_reset')
        view = resolve(url)
        self.assertEqual(view.func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_is_resolved(self):
        """test password_reset_done"""
        url = reverse('foodSearch:password_reset_done')
        view = resolve(url)
        self.assertEqual(view.func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_is_resolved(self):
        """test password_reset_confirm"""
        view = resolve('/reset/{uidb64}/{token}/')
        self.assertEqual(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_is_resolved(self):
        """test password_reset_complete"""
        url = reverse('foodSearch:password_reset_complete')
        view = resolve(url)
        self.assertEqual(view.func.view_class, auth_views.PasswordResetCompleteView)
