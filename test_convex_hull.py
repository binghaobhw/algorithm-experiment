#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase
from convex_hull import random_points, in_triangle, \
    brute_force_find_convex_hull, \
    position_with_line, polar_angle_counter_clockwise_sort, graham_scan, \
    divide_and_conquer_find_convex_hull


class TestRandomPoints(TestCase):
    def test_random_points(self):
        result = random_points(10)
        print result
        self.assertTrue(len(result) == 10)


class TestPositionWithLine(TestCase):
    def setUp(self):
        self.param = [(2, 2), (0, 0), (3, 0)]

    def test_position_with_line(self):
        result = position_with_line(*self.param)
        self.assertTrue(result > 0)


class TestInTriangle(TestCase):
    def test_in_triangle(self):
        params = [[(99, 0), (91, 0), (100, 93), (97, 99)],
                  [(1, 2), (1, 1), (0, 0), (2, 0)],
                  [(1, 2), (1, 1), (2, 1), (3, 1)],
                  [(2, 0), (0, 0), (1, 0), (4, 0)],
                  [(0, 0), (1, 0), (2, 0), (4, 0)]]
        expected_results = [False, False, False, True, False]
        for param, expected in zip(params, expected_results):
            result = in_triangle(*param)
            self.assertTrue(result == expected)


class TestFindConvexHull(TestCase):
    def setUp(self):
        self.points = [[(10, 94), (89, 100), (15, 98), (98, 8), (2, 62), (94, 75), (93, 87), (12, 29), (8, 87), (34, 4)],
                       [(91, 0), (99, 0), (100, 22), (100, 93), (98, 98), (97, 99), (88, 100), (0, 100), (0, 1), (22, 0)]]
        self.expected = [[(2, 62), (12, 29), (34, 4), (98, 8), (94, 75), (93, 87), (89, 100), (15, 98), (10, 94), (8, 87)],
                         [(99, 0), (100, 22), (100, 93), (98, 98), (97, 99), (88, 100), (0, 100), (0, 1), (22, 0)]]

    def test_brute_force_find_convex_hull(self):
        for points, expected in zip(self.points, self.expected):
            result = brute_force_find_convex_hull(points)
            print 'result: {}\nexpected: {}'.format(result, expected)
            # self.assertTrue(set(result) == expected)

    def test_graham_scan(self):
        for points, expected in zip(self.points, self.expected):
            result = graham_scan(points)
            print 'result: {}\nexpected: {}'.format(result, expected)
            # self.assertTrue(set(result) == expected)

    def test_divide_and_conquer(self):
        for points, expected in zip(self.points, self.expected):
            result = divide_and_conquer_find_convex_hull(points)
            print 'result: {}\nexpected: {}'.format(result, expected)
            # self.assertTrue(set(result) == expected)



class TestPolarAngleCounterClockwiseSort(TestCase):
    def setUp(self):
        self.points = {(1, 0), (2, 0), (3, 0), (3, 1), (2, 2), (1, 1)}
        self.base_point = (0, 0)

    def test_polar_angle_counter_clockwise_sort(self):
        expected = [(1, 0), (2, 0), (3, 0), (3, 1), (1, 1), (2, 2)]
        result = polar_angle_counter_clockwise_sort(self.points, self.base_point)
        self.assertTrue(result == expected)
