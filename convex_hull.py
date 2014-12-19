#!/usr/bin/env python
# coding: utf-8
import random
from timer import timing, Timer

SCOPE = range(101)

COUNTER_CLOCKWISE = 1
COLLINEAR = 0
CLOCKWISE = -1

POSITIVE_X, FIRST, POSITIVE_Y, SECOND, NEGATIVE_X, THIRD, NEGATIVE_Y, FORTH = range(8)

brute_force_timer = Timer()
graham_scan_timer = Timer()
divide_and_conquer_timer = Timer()


def random_points(point_num):
    points = []
    for i in range(point_num):
        x = random.choice(SCOPE)
        y = random.choice(SCOPE)
        while (x, y) in points:
            x = random.choice(SCOPE)
            y = random.choice(SCOPE)
        points.append((x, y))
    return points


def in_triangle(target, a, b, c):
    # a, b, c collinear
    if position_with_line(a, b, c) == 0:
        # target, a, b, c collinear
        if position_with_line(target, a, b) == 0:
            sorted_points = sorted([target, a, b, c])
            # If target is not either min or max
            if target != sorted_points[0] and target != sorted_points[-1]:
                return True
            return False
        return False
    return position_with_line(target, a, b)*position_with_line(c, a, b) >= 0 and \
        position_with_line(target, a, c)*position_with_line(b, a, c) >= 0 and \
        position_with_line(target, b, c)*position_with_line(a, b, c) >= 0


def position_with_line(point, a, b):
    """Return the position with given line on which point a and b locate.

    :param point:
    :param a:
    :param b:
    """
    x, y = point[0], point[1]
    a_x, a_y = a[0], a[1]
    b_x, b_y = b[0], b[1]
    x_diff = a_x - b_x
    y_diff = b_y - a_y
    return y_diff * x + x_diff * y + a_y*b_x - a_x*b_y


@timing(brute_force_timer)
def brute_force_find_convex_hull(original_points):
    points = set(original_points)
    remove_points = set()
    for a in points:
        if a in remove_points:
            continue
        for b in points:
            if b in {a} or b in remove_points:
                continue
            for c in points:
                if c in {a, b} or c in remove_points:
                    continue
                for d in points:
                    if d in {a, b, c} or d in remove_points:
                        continue
                    if in_triangle(d, a, b, c):
                        remove_points.add(d)
    points.difference_update(remove_points)
    point_max_x = max(points)
    point_min_x = min(points)
    points_above = set()
    points_below = set()
    for point in points:
        z = orientation(point_min_x, point_max_x, point)
        if z == COUNTER_CLOCKWISE:
            points_above.add(point)
        elif z == CLOCKWISE:
            points_below.add(point)
    sorted_points_above = sorted(points_above, reverse=True)
    sorted_points_below = sorted(points_below)
    convex_hull = [point_min_x]
    convex_hull.extend(sorted_points_below)
    convex_hull.append(point_max_x)
    convex_hull.extend(sorted_points_above)
    return convex_hull


def length(point):
    return point[0] ** 2 + point[1] ** 2


def polar_angle_compare(a, b):
    orientation_ = orientation((0, 0), a, b)
    if orientation_ == COLLINEAR:
        return length(a) - length(b)
    elif orientation_ == CLOCKWISE:
        return 1
    else:
        return -1


def polar_angle_counter_clockwise_sort(points, base_point):
    return sorted(points, cmp=polar_angle_compare, key=lambda p: (p[0] - base_point[0], p[1] - base_point[1]))


def orientation(a, b, c):
    """Determine the orientation of points a, b, c.

    Use z-coordinate of the cross product of (b_x-a_x, b_y-a_y, 0) and
    (c_x-a_x, c_y-a_y, 0) to determine.

    :param a:
    :param b:
    :param c:
    :return:
    """
    a_x, a_y = a
    b_x, b_y = b
    c_x, c_y = c
    z = (b_x - a_x) * (c_y - a_y) - (b_y - a_y) * (c_x - a_x)
    if z == 0:
        return COLLINEAR
    elif z < 0:
        return CLOCKWISE
    else:
        return COUNTER_CLOCKWISE


def counter_clockwise(a, b, c):
    orientation_ = orientation(a, b, c)
    return True if orientation_ == COUNTER_CLOCKWISE else False


@timing(graham_scan_timer)
def graham_scan(points):
    if len(points) < 3:
        return points
    point_set = set(points)
    convex_hull = []
    point_min_y = min(points, key=lambda p: (p[1], p[0]))
    sorted_points = polar_angle_counter_clockwise_sort(
        point_set - {point_min_y}, point_min_y)
    convex_hull.append(point_min_y)
    convex_hull.append(sorted_points[0])
    convex_hull.append(sorted_points[1])
    for i in range(2, len(sorted_points)):
        while len(convex_hull) >= 2 and not counter_clockwise(
                convex_hull[-2], convex_hull[-1], sorted_points[i]):
            convex_hull.pop()
        convex_hull.append(sorted_points[i])
    return convex_hull


def merge(left_convex_hull, right_convex_hull):
    points = list(left_convex_hull)
    points.extend(right_convex_hull)
    return graham_scan(points)


@timing(divide_and_conquer_timer)
def divide_and_conquer_find_convex_hull(points):
    return real_divide_and_conquer(sorted(points))


def real_divide_and_conquer(points):
    n = len(points)
    if n < 3:
        return points
    left_points, right_points = points[:n/2], points[n/2:]
    left_convex_hull = real_divide_and_conquer(left_points)
    right_convex_hull = real_divide_and_conquer(right_points)
    return merge(left_convex_hull, right_convex_hull)


def experiment():
    for point_num in range(1000, 10001, 1000):
        points = random_points(point_num)

        brute_force_timer.reset()
        graham_scan_timer.reset()
        divide_and_conquer_timer.reset()

        a = brute_force_find_convex_hull(points)
        b = graham_scan(points)
        c = divide_and_conquer_find_convex_hull(points)

        # assert set(a) == set(b) == set(c)

        print '{} {:.3f} {:.3f} {:.3f}'.format(point_num, brute_force_timer.time_,
                                               graham_scan_timer.time_, divide_and_conquer_timer.time_)


if __name__ == '__main__':
    experiment()
