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

from . import doubles
import pkg_resources

PACKTOOLS_VERSION = pkg_resources.get_distribution('packtools').version


def _get_test_xml_abspath(filename):
    folder_path = settings.PROJECT_PATH
    folder_path = settings.PROJECT_PATH.split('/')
    folder_path.extend(['validator', 'tests', 'xml_tests_files', filename])
    return '/'.join(folder_path)


def get_temporary_text_file():
    io = StringIO.StringIO()
    io.write('foo')
    text_file = InMemoryUploadedFile(io, field_name='file', name='foo.txt', content_type='text', size=io.len, charset='utf8')
    text_file.seek(0)
    return text_file


def get_temporary_image_file():
    io = StringIO.StringIO()
    size = (200, 200)
    color = (255, 0, 0, 0)
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

    def test_access_unauthenticated_user(self):
        response = self.app.get(
            reverse('validator.packtools.stylechecker',),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validator/stylechecker.html')

    def test_access_authenticated_user(self):
        self.user = auth.UserF(is_active=True)
        response = self.app.get(
            reverse('validator.packtools.stylechecker',),
            user=self.user
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'validator/stylechecker.html')

    def test_link_is_present_at_homepage(self):
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
        page = self.app.get(
            reverse('validator.packtools.stylechecker',),
        )
        form = page.forms['xml_upload_form']
        # when
        response = form.submit()
        # then
        self.assertTemplateUsed(response, 'validator/stylechecker.html')
        self.assertFalse(response.context['form'].is_valid())
        form_errors = response.context['form'].errors
        expected_errors = {'file': [u'This field is required.']}
        self.assertEqual(form_errors, expected_errors)
        self.assertFalse(hasattr(response.context, 'results'))

    def test_submit_text_file_then_form_not_valid(self):
        """
        Submitting a text file will raise a from validation error
        """
        # with
        test_file = get_temporary_text_file()
        # when
        response = self.client.post(
            reverse('validator.packtools.stylechecker',),
            {
                'file': test_file
            }
        )
        # then
        form = response.context['form']
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {
            'file': [u'This type of file is not allowed! Please select another file.']
        }
        self.assertEqual(form.errors, expected_errors)

    def test_submit_image_file_then_form_not_valid(self):
        """
        Submitting a image file will raise a from validation error
        """
        # with
        test_file = get_temporary_image_file()
        # when
        response = self.client.post(
            reverse('validator.packtools.stylechecker',),
            {
                'file': test_file
            }
        )
        # then
        form = response.context['form']
        self.assertFalse(response.context['form'].is_valid())
        expected_errors = {'file': [u'This type of file is not allowed! Please select another file.']}
        self.assertEqual(form.errors, expected_errors)

    def test_submit_valid_xml_file_then_get_annotations_form_valid(self):
        """
        Submitting a xml file that generate annotations will let the form as valid,
        and xml validation will return annotations
        """
        # with

        stub_analyze_xml = doubles.make_stub_analyze_xml('valid')
        mock_utils = self.mocker.replace('validator.utils')
        mock_utils.analyze_xml
        self.mocker.result(stub_analyze_xml)

        self.mocker.replay()

        test_file_path = _get_test_xml_abspath('with_style_errors.xml')
        test_file = get_temporary_xml_file(test_file_path)

        # when
        response = self.client.post(
            reverse('validator.packtools.stylechecker',),
            {
                'file': test_file
            }
        )

        # then
        form = response.context['form']
        xml_exception = response.context['xml_exception']
        results = response.context['results']

        self.assertTrue(form.is_valid())
        self.assertTemplateUsed('validator/stylechecker.html')

        # the template cares about this keys
        self.assertEqual(results.keys(), ['validation_errors', 'meta', 'annotations'])
