from django.test import TestCase
from django import forms
from django.template import Template, Context


class StampRegularFieldTests(TestCase):

    def test_field_is_printed(self):
        out = Template(
                "{% load formstamps %}"
                "{% stamp_regular_field field %}"
            ).render(Context({
                'field': forms.CharField()
            }))

        self.assertIn('django.forms.fields.CharField object at', out)

    def test_label_bound_to_field(self):
        class TestForm(forms.Form):
            name = forms.CharField()
        tform = TestForm()

        out = Template(
                "{% load formstamps %}"
                "{% stamp_regular_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<label for="id_name">', out)

    def test_error_class_appears_on_errors(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_regular_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('error', out)

    def test_error_messages_are_displayed(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_regular_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<li>This field is required.</li>', out)

    def test_error_messages_are_displayed_inside_errorlist_class(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_regular_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<ul class="errorlist">', out)

    def test_required_fields_have_reqfield_class(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_regular_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<span class="req-field">', out)


class StampInlineFormsetFieldTests(TestCase):

    def test_field_is_printed(self):
        out = Template(
                "{% load formstamps %}"
                "{% stamp_inlineformset_field field %}"
            ).render(Context({
                'field': forms.CharField()
            }))

        self.assertIn('django.forms.fields.CharField object at', out)

    def test_label_bound_to_field(self):
        class TestForm(forms.Form):
            name = forms.CharField()
        tform = TestForm()

        out = Template(
                "{% load formstamps %}"
                "{% stamp_inlineformset_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<label for="id_name">', out)

    def test_error_class_appears_on_errors(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_inlineformset_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('error', out)

    def test_error_messages_are_displayed(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_inlineformset_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<li>This field is required.</li>', out)

    def test_error_messages_are_displayed_inside_errorlist_class(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_inlineformset_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<ul class="errorlist">', out)

    def test_required_fields_have_reqfield_class(self):
        class TestForm(forms.Form):
            name = forms.CharField(required=True)
        tform = TestForm({})

        out = Template(
                "{% load formstamps %}"
                "{% stamp_inlineformset_field field %}"
            ).render(Context({
                'field': tform['name']
            }))

        self.assertIn('<span class="req-field">', out)

