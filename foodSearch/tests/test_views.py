#!/usr/bin/env python
"""Test on views.py"""

from django.test import TestCase
from django.urls import reverse
from django.test import TransactionTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from  django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver

from ..models import Favorite, Product

class GeneralPagesTestCase(TestCase):
    """
    Tests on generals pages as index or legals
    not depending on database or user action
    """

    def test_index_page(self):
        """test index view"""
        # you must add a name to index view: `name="index"`
        response = self.client.get(reverse('foodSearch:index'))
        self.assertEqual(response.status_code, 200)

    def test_legals_page(self):
        """test legal view"""
        response = self.client.get(reverse('foodSearch:legals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/legals.html')


class RegisterPageTestCase(StaticLiveServerTestCase):
    """
    Tests on views depending on authentification of user
    using a StaticLiveServerTestCase class
    """

    @classmethod
    def setUpClass(cls):
        """setup tests"""
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """teardown tests"""
        cls.selenium.quit()
        super().tearDownClass()

    def test_register(self):
        """tests on register view"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_css_selector("#connect").click()
        signin_modal = self.selenium.find_element_by_css_selector("#modalLogIn")
        self.assertTrue(signin_modal.is_displayed())
        self.selenium.find_element_by_css_selector("#registration").click()
        signup_modal = self.selenium.find_element_by_css_selector("#modalRegister")
        self.assertTrue(signup_modal.is_displayed())

        username_input = self.selenium.find_element_by_css_selector("#signUp-username")
        username_input.send_keys('usertest')
        email_input = self.selenium.find_element_by_css_selector("#signUp-email")
        email_input.send_keys('usertest@test.com')
        password_input = self.selenium.find_element_by_css_selector("#signUp-password1")
        password_input.send_keys('mot2passe5ecret')
        password_input = self.selenium.find_element_by_css_selector("#signUp-password2")
        password_input.send_keys('mot2passe5ecret')
        self.selenium.find_element_by_css_selector("#signUp-btn").click()

        self.assertEqual(User.objects.filter(username="usertest").exists(), True)
        self.assertEqual(User.objects.filter(username="usertest").count(), 1)
        self.assertEqual(User.objects.get(username="usertest").is_authenticated, True)

    def test_login(self):
        """tests on login view"""
        User.objects.create(username="Test",
                            email="userinDB@test.com",
                            password="mot2passe5ecret")
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_css_selector("#connect").click()
        signin_modal = self.selenium.find_element_by_css_selector("#modalLogIn")
        self.assertTrue(signin_modal.is_displayed())
        username_input = self.selenium.find_element_by_css_selector("#login-username")
        username_input.send_keys('Test')
        password_input = self.selenium.find_element_by_css_selector("#login-password")
        password_input.send_keys('mot2passe5ecret')
        self.selenium.find_element_by_css_selector("#signin-Submit").click()

        self.assertEqual(User.objects.filter(username="Test").exists(), True)
        self.assertEqual(User.objects.filter(username="Test").count(), 1)
        self.assertEqual(User.objects.get(username="Test").is_authenticated, True)

class RegisterClientTestCase(TransactionTestCase):

    def setUp(self):
        """setup tests"""
        self.user1 = User.objects.create_user(
        'registerTestUser', 'test@test.com', 'testpassword')

    def test_register_succes(self):
        data = {'username':'NewUserTest', 'email':'testnewUser@test.com','password1':'t3stpassword','password2':'t3stpassword'}
        response = self.client.post(reverse('foodSearch:register'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.filter(username='NewUserTest').exists(), True)
        self.assertEqual(User.objects.get(username='NewUserTest').is_authenticated, True)
        self.client.logout()

    def test_register_fails_password_not_confrimed(self):
        data = {'username':'NewUserTest', 'email':'testnewUser@test.com','password1':'t3stpassword','password2':'testpassword'}
        response = self.client.post(reverse('foodSearch:register'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.filter(username='NewUserTest').exists(), False)

    def test_register_fails_password_too_short(self):
        data = {'username':'NewUserTest', 'email':'testnewUser@test.com','password1':'test','password2':'test'}
        response = self.client.post(reverse('foodSearch:register'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.filter(username='NewUserTest').exists(), False)

    def test_register_fails_username_already_in_DB(self):
        data = {'username':'registerTestUser', 'email':'registerTestUser@test.com','password1':'t3stpassword','password2':'t3stpassword'}
        response = self.client.post(reverse('foodSearch:register'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.filter(username='registerTestUser').exists(), True)
        self.assertEqual(User.objects.filter(email='registerTestUser@test.com').exists(), False)

    def test_register_fails_email_already_in_DB(self):
        data = {'username':'brandnewuser', 'email':'test@test.com','password1':'t3stpassword','password2':'t3stpassword'}
        response = self.client.post(reverse('foodSearch:register'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(User.objects.filter(username='brandnewuser').exists(), False)


class ProceedResearchTestCase(TestCase):
    """
    Tests on views depending on user actions not related to saving or deleting favorites
    """

    def setUp(self):
        """setup tests"""
        self.user = User.objects.create_user(
            username='Test', email='Test@…', password='password')
        self.query = "Product"
        self.prod = Product.objects.create(id=31,
                                           name="Fàke product for db",
                                           formatted_name="FAKE PRODUCT FOR DB",
                                           brands="brand fake",
                                           formatted_brands="BRAND FAKE",
                                           reference='1',
                                           nutrition_grade_fr="A")
        self.prod2 = Product.objects.create(id=32,
                                            name="Second fake prôduct",
                                            formatted_name="SECOND FAKE PRODUCT",
                                            brands="the wrong one",
                                            formatted_brands="THE WRONG ONE",
                                            reference='2',
                                            nutrition_grade_fr="E")

    def test_search_get(self):
        """test search view"""
        response = self.client.get(reverse('foodSearch:search'), {'query': self.query})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/search.html')
        self.assertEqual(self.prod in response.context['found_products'], True)

    def test_results_get(self):
        """test result view"""
        response = self.client.get(reverse('foodSearch:results', args=[self.prod2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/results.html')
        self.assertEqual({self.prod: "unsaved"} in response.context['result'], True)

    def test_detail_get(self):
        """test detail view"""
        response = self.client.get(reverse('foodSearch:detail', args=[self.prod.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/detail.html')
        self.assertEqual(response.context['product'], self.prod)

class UserProfileTestCase(TransactionTestCase):

    def setUp(self):
        """setup tests"""
        self.user = User.objects.create_user(
            username='Test', email='test@test.com', password='testpassword')

    def test_userpage_get(self):
        """test userpage view in get method"""
        self.client.login(username='Test', password='testpassword')
        response = self.client.get(reverse('foodSearch:userpage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(username="Test").is_authenticated, True)
        self.assertTemplateUsed(response, 'foodSearch/userpage.html')
        self.assertEqual(response.context['user'].username, self.user.username)
        self.assertEqual(response.context['user'].email, self.user.email)
        self.client.logout()

    def test_new_name(self):
        """test change nameview"""
        id = self.user.id
        username = self.user.username
        self.client.login(username=self.user.username, password='testpassword')
        data = {'username':'NewName'}
        response = self.client.post(reverse('foodSearch:new_name'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(User.objects.filter(username="NewName").exists(), True)
        self.assertEquals(User.objects.filter(username="NewName").count(), 1)
        self.assertEquals(User.objects.get(id=id).username, 'NewName')
        self.client.logout()

    def test_new_name_already_in_DB(self):
        """test change nameview with integrity error, name already in DB"""
        User.objects.create_user(
            username='userinDB', email='Test@…', password='password')
        id = self.user.id
        username = self.user.username
        self.client.login(username=self.user.username, password='testpassword')
        data = {'username':'userinDB'}
        response = self.client.post(reverse('foodSearch:new_name'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(User.objects.get(id=id).username, username)
        self.assertTrue(User.objects.get(username='userinDB').id != id)
        self.client.logout()

    def test_new_email(self):
        """test change nameview"""
        id = self.user.id
        username = self.user.username
        self.client.login(username=self.user.username, password='testpassword')
        data = {'email':'New@email.test'}
        response = self.client.post(reverse('foodSearch:new_email'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(User.objects.get(id=id).email, 'New@email.test')
        self.client.logout()

    def test_new_email_already_in_DB(self):
        """test change nameview with integrity error, name already in DB"""
        User.objects.create_user(
            username='userinDB', email='emailalreadyindb@test.com', password='password')
        id = self.user.id
        email = self.user.email
        self.client.login(username=self.user.username, password='testpassword')
        data = {'email':'emailalreadyindb@test.com'}
        response = self.client.post(reverse('foodSearch:new_email'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(User.objects.get(id=id).email, email)
        self.client.logout()


class ManageFavoritesTestCase(TransactionTestCase):
    """
    Tests on views managing saving or deleting favorites
    """

    def setUp(self):
        """setup tests"""
        self.user1 = User.objects.create_user(
            username='Test', email='Test@…', password='password')
        self.user2 = User.objects.create_user(
            username='Test2', email='Test@…', password='password')
        self.product1 = Product.objects.create(name="Fàke product for db",
                                               formatted_name="FAKE PRODUCT FOR DB",
                                               brands="good4U",
                                               formatted_brands="GOOD4U",
                                               reference='fakeref1',
                                               nutrition_grade_fr="A")
        self.product2 = Product.objects.create(name="Second fake prôduct",
                                               formatted_name="SECOND FAKE PRODUCT",
                                               brands="bad4U",
                                               formatted_brands="BAD4U",
                                               reference='fakeref2',
                                               nutrition_grade_fr="E")
        self.favorite = Favorite.objects.create(user=self.user1,
                                                substitute=self.product1,
                                                initial_search_product=self.product2)


    def test_watchlist_empty(self):
        """tests watchlist view when empty"""
        self.client.login(username='Test2', password='password')
        response = self.client.get(reverse('foodSearch:watchlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/watchlist.html')
        self.assertEqual(response.context['page'], 1)
        self.assertEqual(response.context['title'], 'Mes aliments')
        self.assertEqual(response.context['watchlistpage'].exists(), False)
        self.assertEqual(response.context['paginate'], False)
        self.client.logout()

    def test_watchlist_content(self):
        """tests watchlist view when with content"""
        self.client.login(username='Test', password='password')
        response = self.client.get(reverse('foodSearch:watchlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/watchlist.html')
        self.assertEqual(response.context['page'], 1)
        self.assertEqual(response.context['title'], 'Mes aliments')
        self.assertEqual(response.context['watchlistpage'].exists(), True)
        self.assertEqual(self.favorite in response.context['watchlistpage'], True)
        self.assertEqual(response.context['paginate'], False)
        self.client.logout()

    def test_save_favorite(self):
        """tests loadfavorite view when saving favorite"""
        self.client.login(username='Test2', password='password')
        data = {'user': self.user2.id,
                'substitute':self.product1.id,
                'favorite': "unsaved",
                'product':self.product2.id}
        response = self.client.post(reverse('foodSearch:load_favorite'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        fav = Favorite.objects.filter(user=self.user2, substitute=self.product1)
        self.assertEqual(fav.exists(), True)
        self.client.logout()

    def test_unsave_favorite(self):
        """tests loadfavorite view when deleting favorite"""
        self.client.login(username='Test', password='password')
        data = {'user': self.user1.id,
                'substitute':self.product1.id,
                'favorite': "saved",
                'product':self.product2.id}
        response = self.client.post(reverse('foodSearch:load_favorite'),
                                    data=data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        fav = Favorite.objects.filter(user=self.user1, substitute=self.product1)
        self.assertEqual(fav.exists(), False)
        self.client.logout()
