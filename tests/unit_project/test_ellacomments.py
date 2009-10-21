# -*- coding: utf-8 -*-
from djangosanetesting import DatabaseTestCase

from django import template
from django.contrib.sites.models import Site

from threadedcomments.models import ThreadedComment

from unit_project.test_core import create_basic_categories, create_and_place_a_publishable
from unit_project import template_loader

def create_comment(obj, ct):
        c = ThreadedComment.objects.create(
            comment='',
            content_type=ct,
            object_pk=obj.pk,
            site=Site.objects.get_current(),
        )
        return c

class TestTemplateTags(DatabaseTestCase):
    def setUp(self):
        super(TestTemplateTags, self).setUp()
        create_basic_categories(self)
        create_and_place_a_publishable(self)

    def test_comment_count_for_article_is_picked_up_through_article(self):
        create_comment(self.publishable, self.publishable.content_type)
        t = template.Template('''{% load ellacomments_tags %}{% get_comment_count for obj as var_name%}{{ var_name }}''')
        self.assert_equals('1', t.render(template.Context({'obj': self.publishable})))

    def test_comment_count_for_article_is_picked_up_through_publishable(self):
        create_comment(self.publishable, self.publishable.content_type)
        t = template.Template('''{% load ellacomments_tags %}{% get_comment_count for obj as var_name%}{{ var_name }}''')
        self.assert_equals('1', t.render(template.Context({'obj': self.only_publishable})))
        
    def test_comment_list_for_article_is_picked_up_through_article(self):
        create_comment(self.publishable, self.publishable.content_type)
        t = template.Template('''{% load ellacomments_tags %}{% get_comment_list for obj as var_name%}{{ var_name|length }}''')
        self.assert_equals('1', t.render(template.Context({'obj': self.publishable})))

    def test_comment_list_for_article_is_picked_up_through_publishable(self):
        create_comment(self.publishable, self.publishable.content_type)
        t = template.Template('''{% load ellacomments_tags %}{% get_comment_list for obj as var_name%}{{ var_name|length }}''')
        self.assert_equals('1', t.render(template.Context({'obj': self.only_publishable})))
        
