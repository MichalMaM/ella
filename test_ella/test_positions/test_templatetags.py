# -*- coding: utf-8 -*-
from django.test import TestCase

from nose import tools

from django import template
from django.template import Context


from test_ella.test_core import create_basic_categories

from ella.core.models import Category
from ella.positions.models import Position
from ella.positions.templatetags.positions import (
                                                   _get_category_from_pars_var,
                                                   _parse_position_tag,
                                                   PositionNode,
                                                   )


class TestPositionParsing(TestCase):

    def setUp(self):
        super(TestPositionParsing, self).setUp()
        create_basic_categories(self)
        self.context = Context({'category': self.category})
        self.context_for_category_nested = Context({'category': self.category_nested})
        self.position = Position(
            category=self.category_nested,
            name='position-name',
            text='other text'
        )
        self.position.save()

    def test_getting_category_for_templatag_from_category_variable(self):
        tools.assert_equals(_get_category_from_pars_var(template.Variable('category'), self.context), self.category)

    def test_getting_category_for_templatag_from_category_tree_path_in_variable(self):
        context = Context({'category': '%s' % (self.category.tree_path)})
        tools.assert_equals(_get_category_from_pars_var(template.Variable('category'), context), self.category)

    def test_getting_category_for_templatag_from_category_tree_path(self):
        tools.assert_equals(_get_category_from_pars_var(template.Variable('"%s"' % (self.category.tree_path)), self.context), self.category)
        tools.assert_equals(_get_category_from_pars_var(template.Variable('"%s"' % (self.category_nested.tree_path)), self.context), self.category_nested)

    def test_parsing_position_tag(self):
        position_node = _parse_position_tag('position position-name for category'.split(), 'endposition')
        tools.assert_true(isinstance(position_node, PositionNode))
        tools.assert_true(isinstance(position_node.category, template.Variable))
        position_node = _parse_position_tag('position position-name for category nofallback'.split(), 'endposition')
        tools.assert_true(isinstance(position_node, PositionNode))
        tools.assert_true(isinstance(position_node.category, template.Variable))
        position_node = _parse_position_tag('position position-name for category using BOX_TYPE'.split(), 'endposition')
        tools.assert_true(isinstance(position_node, PositionNode))
        tools.assert_true(isinstance(position_node.category, template.Variable))
        position_node = _parse_position_tag('position position-name for category using BOX_TYPE nofallback'.split(), 'endposition')
        tools.assert_true(isinstance(position_node, PositionNode))
        tools.assert_true(isinstance(position_node.category, template.Variable))
        position_node = _parse_position_tag('position "position" for category'.split(), 'endposition')
        tools.assert_true(isinstance(position_node, PositionNode))
        tools.assert_true(isinstance(position_node.category, template.Variable))

    def test_position_templatetag_render_with_category_var(self):
        t = template.Template('{% load positions %}{% position position-name for category %}{% endposition %}')
        tools.assert_equals('other text', t.render(self.context_for_category_nested))

    def test_position_templatetag_render_with_category_tree_path(self):
        t = template.Template('{% load positions %}{% position position-name for "nested-category" %}{% endposition %}')
        tools.assert_equals('other text', t.render(self.context_for_category_nested))

    def test_empty_position_templatetag_render_with_category_var(self):
        t = template.Template('{% load positions %}{% position position-name for category %}{% endposition %}')
        tools.assert_equals('', t.render(self.context))

    def test_raise_position_templatetag_render_with_bad_category_tree_path(self):
        t = template.Template('{% load positions %}{% position position-name for "nested-categoryy" %}{% endposition %}')
        tools.assert_raises(Category.DoesNotExist, t.render, self.context_for_category_nested)

    def test_ifposition_templatetag_render_with_category_var(self):
        t = template.Template('{% load positions %}{% ifposition position-name for category %}ON{% else %}OUT{% endifposition %}')
        tools.assert_equals('ON', t.render(self.context_for_category_nested))

    def test_ifposition_templatetag_render_with_category_tree_path(self):
        t = template.Template('{% load positions %}{% ifposition position-name for "nested-category" %}ON{% else %}OUT{% endifposition %}')
        tools.assert_equals('ON', t.render(self.context_for_category_nested))

    def test_not_position_for_ifposition_templatetag_render_with_category_var(self):
        t = template.Template('{% load positions %}{% ifposition position-name for category %}ON{% else %}OUT{% endifposition %}')
        tools.assert_equals('OUT', t.render(self.context))

    def test_raise_ifposition_templatetag_render_with_bad_category_tree_path(self):
        t = template.Template('{% load positions %}{% ifposition position-name for "nested-categoryy" %}ON{% else %}OUT{% endifposition %}')
        tools.assert_raises(Category.DoesNotExist, t.render, self.context)
