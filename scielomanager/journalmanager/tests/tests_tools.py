# coding: utf-8
from django.test import TestCase
from .modelfactories import IssueFactory


class PaginationTest(TestCase):
    def _makeOne(self, *args, **kwargs):
        from scielomanager.tools import get_paginated
        return get_paginated(*args, **kwargs)

    def test_total_number_of_items(self):
        items_list = [chr(i) for i in range(97, 123)]
        page_num = 1
        items_per_page = 5

        pag = self._makeOne(items_list, page_num, items_per_page=items_per_page)
        self.assertEqual(pag.paginator.count, 26)

    def test_total_number_of_items_per_page(self):
        items_list = [chr(i) for i in range(97, 123)]
        page_num = 1
        items_per_page = 5

        pag = self._makeOne(items_list, page_num, items_per_page=items_per_page)
        self.assertEqual(len(pag.object_list), 5)

    def test_total_number_of_pages(self):
        items_list = [chr(i) for i in range(97, 123)]
        page_num = 1
        items_per_page = 5

        pag = self._makeOne(items_list, page_num, items_per_page=items_per_page)
        self.assertEqual(pag.paginator.num_pages, 6)

    def test_get_iterator_by_object_list(self):
        items_list = [chr(i) for i in range(97, 123)]
        page_num = 1
        items_per_page = 5

        pag = self._makeOne(items_list, page_num, items_per_page=items_per_page)
        self.assertTrue(hasattr(pag, 'object_list'))

    def test_non_existing_page_must_retrieve_the_last_page(self):
        items_list = [chr(i) for i in range(97, 123)]
        page_num = 10  # there are only 6 pages
        items_per_page = 5

        pag = self._makeOne(items_list, page_num, items_per_page=items_per_page)
        self.assertEqual(pag.number, pag.paginator.num_pages)

    def test_non_int_but_coercible_page_parameter(self):
        items_list = [chr(i) for i in range(97, 123)]
        page_num = '1'
        items_per_page = 5

        pag = self._makeOne(items_list, page_num, items_per_page=items_per_page)
        self.assertEqual(pag.paginator.count, 26)

    def test_non_int_but_uncoercible_page_parameter_must_raise_TypeError(self):
        items_list = [chr(i) for i in range(97, 123)]
        page_num = 'foo'
        items_per_page = 5

        self.assertRaises(TypeError,
                          self._makeOne,
                          items_list,
                          page_num,
                          items_per_page=items_per_page)


class HasChangedTest(TestCase):

    def _makeOne(self, *args, **kwargs):
        from scielomanager.tools import has_changed
        return has_changed(*args, **kwargs)

    def test_has_changed_must_return_false_when_field_doesnt_change(self):
        issue = IssueFactory.create()

        self.assertFalse(self._makeOne(issue, 'total_documents'))

    def test_has_changed_must_return_false_when_field_is_changed(self):
        issue = IssueFactory.create(total_documents=10)

        self.assertFalse(self._makeOne(issue, 'total_documents'))

    def test_has_changed_must_return_none_when_instance_doesnt_exist_in_database(self):
        issue = IssueFactory.create(pk=None)
        self._makeOne(issue, 'volume')

    def test_has_changed_must_return_except_when_field_doesnt_exist(self):
        from django.core.exceptions import FieldError
        issue = IssueFactory.create()

        self.assertRaises(FieldError, lambda: self._makeOne(issue, 'fake_field'))
