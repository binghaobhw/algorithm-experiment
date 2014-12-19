#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase
from lcs import recursively_find_lcs, dynamically_find_lcs, \
    three_sequence_dynamically_find_lcs, random_str


class TestFindLcs(TestCase):
    def setUp(self):
        self.a = u'wangbinghao'
        self.b = u'chenhuanle'
        self.expected = u'nha'

    def test_recursively_find_lcs(self):
        result = recursively_find_lcs(self.a, self.b)
        self.assertTrue(result == self.expected)

    def test_dynamically_find_lcs(self):
        result = dynamically_find_lcs(self.a, self.b)
        self.assertTrue(result == self.expected)


class TestThreeSequenceFindLcs(TestCase):
    def setUp(self):
        self.x = 'ab'
        self.y = 'efabdg'
        self.z = 'abefdg'
        self.expected = 'ab'

    def test_three_sequence_dynamically_find_lcs(self):
        result = three_sequence_dynamically_find_lcs(self.x, self.y, self.z)
        self.assertTrue(result == self.expected)


class TestRandomStr(TestCase):
    str_len = 100
    def test_random_str(self):
        result = random_str(self.str_len)
        self.assertTrue(len(result) == self.str_len)
