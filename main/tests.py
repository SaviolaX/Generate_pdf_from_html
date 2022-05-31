from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Car, Document


class BaseTest(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123'
        )
        self.user_auth = {
            'username': 'will',
            'password': 'testpass123'
        }
        self.car = Car.objects.create(car_model='Mazda',
                                      car_number=1234,
                                      rent_cost_per_day=1.0)
        self.document1 = Document.objects.create(car=self.car,
                                                 first_name='Bob',
                                                 last_name='Ross',
                                                 company='TNK',
                                                 renting_date_from='1930-12-22',
                                                 renting_date_to='1930-12-23')
        self.login_url = reverse('login')


class IndexPageTests(BaseTest):

    def test_index_status_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_index_url_name_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_index_status_code_not_logged_in(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_index_url_name_code_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_homepage_contains_correct_html(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get('/')
        self.assertContains(response, 'Create PDF document')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')


class DocumentsViewTests(BaseTest):

    def test_list_documents_url_name_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(reverse('list_documents'))
        self.assertEqual(response.status_code, 200)

    def test_list_documents_url_name_code_not_logged_in(self):
        response = self.client.get(reverse('list_documents'))
        self.assertEqual(response.status_code, 302)

    def test_list_document_view(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(reverse('list_documents'))
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'Ross')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/all_forms.html')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')


class DocumentPageTests(BaseTest):

    def test_document_page_url_name_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(
            reverse('document_page', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_document_page_url_name_code_not_logged_in(self):
        response = self.client.get(
            reverse('document_page', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_document_detail_view(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(
            reverse('document_page', kwargs={'pk': self.document1.pk}))
        no_response = self.client.get('/document/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'Ross')
        self.assertContains(response, 'TNK')
        self.assertTemplateUsed(response, 'main/form_page.html')


class DocumentUpdatePageTests(BaseTest):

    def test_document_update_url_name_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(
            reverse('document_update', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_document_update_url_name_code_not_logged_in(self):
        response = self.client.get(
            reverse('document_update', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 302)


class DocumentDeletePageTests(BaseTest):

    def test_document_update_url_name_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(
            reverse('document_delete', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_document_update_url_name_code_not_logged_in(self):
        response = self.client.get(
            reverse('document_delete', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 302)


class DocumentCreatePageTests(BaseTest):

    def test_document_create_url_name_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(reverse('document_create'))
        self.assertEqual(response.status_code, 200)

    def test_document_create_url_name_code_not_logged_in(self):
        response = self.client.get(reverse('document_create'))
        self.assertEqual(response.status_code, 302)

    def test_document_creating(self):
        self.assertEqual(f'{self.document1.car.car_model}',
                         f'{self.car.car_model}')
        self.assertEqual(f'{self.document1.first_name}', 'Bob')
        self.assertEqual(f'{self.document1.last_name}', 'Ross')
        self.assertEqual(f'{self.document1.company}', 'TNK')
        self.assertEqual(f'{self.document1.renting_date_from}', '1930-12-22')
        self.assertEqual(f'{self.document1.renting_date_to}', '1930-12-23')


class ViewPDFPageTests(BaseTest):

    def test_document_pdf_url_name_code(self):
        self.client.post(self.login_url, self.user_auth)
        response = self.client.get(
            reverse('document_pdf', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_document_pdf_url_name_code_not_logged_in(self):
        response = self.client.get(
            reverse('document_pdf', kwargs={'pk': self.document1.pk}))
        self.assertEqual(response.status_code, 302)
