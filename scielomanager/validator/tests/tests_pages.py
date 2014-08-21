# coding:utf-8
from os import path
import unittest
import mocker
from PIL import Image
import StringIO

from django.core.urlresolvers import reverse
from django_webtest import WebTest
from django.conf import settings
from django_factory_boy import auth
from django.core.files.uploadedfile import InMemoryUploadedFile

from waffle import Flag

from articletrack.tests import doubles


def _get_test_xml_abspath(filename):
    folder_path = settings.PROJECT_PATH
    folder_path = settings.PROJECT_PATH.split('/')
    folder_path.extend(['articletrack', 'tests', 'xml_tests_files', filename])
    return '/'.join(folder_path)


def get_temporary_text_file():
    io = StringIO.StringIO()
    io.write('foo')
    text_file = InMemoryUploadedFile(io, field_name='file', name='foo.txt', content_type='text', size=io.len, charset='utf8')
    text_file.seek(0)
    return text_file

def get_temporary_image_file():
    io = StringIO.StringIO()
    size = (200,200)
    color = (255,0,0,0)
    image = Image.new("RGBA", size, color)
    image.save(io, format='PNG')
    image_file = InMemoryUploadedFile(io, field_name='file', name='foo.png', content_type='png', size=io.len, charset=None)
    image_file.seek(0)
    return image_file

def get_temporary_xml_file(xml_abs_path):
    fp = open(xml_abs_path)
    io = StringIO.StringIO(fp.read())
    fp.close()
    xml_file = InMemoryUploadedFile(io, field_name='file', name='foo.xml', content_type='text/xml', size=io.len, charset='utf8')
    xml_file.seek(0)
    return xml_file


class ValidatorTests(WebTest, mocker.MockerTestCase):

    def _addWaffleFlag(self):
        Flag.objects.create(name='packtools_validator', everyone=True)

    def _mocker_replace_stylechecker(self, with_annotations=False):
        XML = self.mocker.replace('packtools.stylechecker.XML')
        XML(mocker.ANY)
        if with_annotations:
            self.mocker.result(doubles.StylecheckerAnnotationsDouble(mocker.ANY))
        else:
            self.mocker.result(doubles.StylecheckerDouble(mocker.ANY))
        self.mocker.replay()

    def test_status_code_stylechecker_without_waffle_flag(self):
        response = self.app.get(
            reverse('validator.packtools.stylechecker',),
            expect_errors=True
        )
        self.assertEqual(response.status_code, 404)

    def test_status_code_stylechecker_with_waffle_flag(self):
        self._addWaffleFlag()
        response = self.app.get(
            reverse('validator.packtools.stylechecker',),
        )
        self.assertEqual(response.status_code, 200)

    def test_access_unauthenticated_user(self):
        self._addWaffleFlag()
        response = self.app.get(
            reverse('validator.packtools.stylechecker',),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validator/packtools.html')

    def test_access_authenticated_user(self):
        self._addWaffleFlag()
        self.user = auth.UserF(is_active=True)
        response = self.app.get(
            reverse('validator.packtools.stylechecker',),
            user=self.user
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validator/packtools.html')

    def test_link_is_present_at_homepage(self):
        self._addWaffleFlag()
        response = self.app.get(
            reverse('index',),
        )
        # response redirecto to login
        self.assertEqual(response.status_code, 302)
        response = response.follow()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        expected_url = reverse('validator.packtools.stylechecker',)
        response.mustcontain('href="%s"' % expected_url)

    def test_submit_empty_form_is_not_valid(self):
        # with
        self._addWaffleFlag()
        page = self.app.get(
            reverse('validator.packtools.stylechecker',),
        )
        form = page.forms['stylechecker']
        # when
        response = form.submit()
        # then
        self.assertTemplateUsed(response, 'validator/packtools.html')
        self.assertFalse(response.context['form'].is_valid())
        form_errors = response.context['form'].errors
        expected_errors = {
            '__all__': [u'if trying to validate via URL, please submit a valid URL']
        }
        self.assertEqual(form_errors, expected_errors)
        self.assertFalse(hasattr(response.context, 'results'))

    def test_submite_invalid_url_then_form_is_not_valid(self):
        # with
        self._addWaffleFlag()
        page = self.app.get(
            reverse('validator.packtools.stylechecker',),
        )
        form = page.forms['stylechecker']
        form['type'] = 'url'
        form['url'] = 'file:///abc.123'
        # when
        response = form.submit()
        # then
        self.assertTemplateUsed(response, 'validator/packtools.html')
        self.assertFalse(response.context['form'].is_valid())
        form_errors = response.context['form'].errors
        expected_errors = {
            'url': [u'Enter a valid URL.'],
            '__all__': [u'if trying to validate via URL, please submit a valid URL']
        }
        self.assertEqual(form_errors, expected_errors)
        self.assertFalse(hasattr(response.context, 'results'))

    def test_submit_valid_url_then_form_is_valid(self):
        """
        Submitting a valid url, will not raise a validation error of the form.
        """
        # with
        self._addWaffleFlag()
        self._mocker_replace_stylechecker()
        # when
        page = self.app.get(
            reverse('validator.packtools.stylechecker',),
        )
        form = page.forms['stylechecker']
        form['type'] = 'url'
        form['url'] = 'http://example.com/foo/bar/valid.xml'
        response = form.submit()
        # then
        self.assertTemplateUsed(response, 'validator/packtools.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].is_valid())
        expected_results = {
            'validation_errors': {'error_lines': '', 'results': []},
            'annotations': None,
            'can_be_analyzed': (True, None)
        }
        self.assertEqual(response.context['results'], expected_results)

    def test_submit_text_file_then_form_not_valid(self):
        # with
        self._addWaffleFlag()
        test_file = get_temporary_text_file()
        # when
        response = self.client.post(
            reverse('validator.packtools.stylechecker',),
            {
                'type': 'file',
                'file': test_file
            }
        )
        # then
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {
            '__all__': [u'if trying to validate a File, please upload a valid XML file'],
            'file': [u'This type of file is not allowed! Please select another file.']
        }
        self.assertEqual(form.errors, expected_errors)

    def test_submit_image_file_then_form_not_valid(self):
        # with
        self._addWaffleFlag()
        test_file = get_temporary_image_file()
        # when
        response = self.client.post(
            reverse('validator.packtools.stylechecker',),
            {
                'type': 'file',
                'file': test_file
            }
        )
        # then
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {
            '__all__': [u'if trying to validate a File, please upload a valid XML file'],
            'file': [u'This type of file is not allowed! Please select another file.']
        }
        self.assertEqual(form.errors, expected_errors)

    def test_submit_valid_xml_file_then_form_not_valid(self):
        # with
        self._addWaffleFlag()
        self._mocker_replace_stylechecker(with_annotations=True)
        test_file_path = _get_test_xml_abspath('with_style_errors.xml')
        test_file = get_temporary_xml_file(test_file_path)
        # when
        response = self.client.post(
            reverse('validator.packtools.stylechecker',),
            {
                'type': 'file',
                'file': test_file
            }
        )
        # then
        form = response.context['form']
        results = response.context['results']

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['form'].is_valid())
        self.assertEqual((True, None), results['can_be_analyzed'])
        self.assertIsNotNone(results['validation_errors'])
        self.assertIsNotNone(results['annotations'])
        self.assertTrue(len(results['validation_errors']['results']) > 0)

        self.assertTemplateUsed('validator/packtools.html')
