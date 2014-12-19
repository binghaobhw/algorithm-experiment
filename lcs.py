#!/usr/bin/env python
# coding: utf-8
import random
import sys

from timer import Timer, timing


sys.setrecursionlimit(5000)
EMPTY_STRING = u''
timer_recursive = Timer()
timer_dynamic = Timer()
CHAR_CANDIDATES = [u'A', u'B', u'C', u'D']


def real_recursively_find_lcs(x, y):
    if not x or not y:
        return EMPTY_STRING
    if x[-1] == y[-1]:
        return EMPTY_STRING.join([real_recursively_find_lcs(x[:-1], y[:-1]), x[-1]])
    else:
        return max(real_recursively_find_lcs(x[:-1], y),
                   real_recursively_find_lcs(x, y[:-1]), key=lambda s: len(s))


@timing(timer_recursive)
def recursively_find_lcs(x, y):
    return real_recursively_find_lcs(x, y)


def create_zero_matrix(raw_num, column_num):
    return [[0 for j in range(column_num)] for i in range(raw_num)]


def lcs_len(x, y):
    raw_num = len(x)
    column_num = len(y)
    lcs_len_ = create_zero_matrix(raw_num+1, column_num+1)
    @timing(timer_dynamic)
    def fill_lcs_len():
        for i in range(raw_num):
            for j in range(column_num):
                if x[i] == y[j]:
                    lcs_len_[i][j] = lcs_len_[i-1][j-1] + 1
                else:
                    lcs_len_[i][j] = max(lcs_len_[i][j-1], lcs_len_[i-1][j])
    fill_lcs_len()
    return lcs_len_


def back_track(lcs_len_, x, y, i, j):
    if i == -1 or j == -1:
        return EMPTY_STRING
    elif x[i] == y[j]:
        return EMPTY_STRING.join([back_track(lcs_len_, x, y, i-1, j-1), x[i]])
    else:
        if lcs_len_[i][j-1] > lcs_len_[i-1][j]:
            return back_track(lcs_len_, x, y, i, j-1)
        else:
            return back_track(lcs_len_, x, y, i-1, j)


def dynamically_find_lcs(x, y):
    if not x or not y:
        return EMPTY_STRING
    lcs_len_ = lcs_len(x, y)
    return back_track(lcs_len_, x, y, len(x)-1, len(y)-1)


def three_sequence_lcs_len(x, y, z):
    num_x = len(x)
    num_y = len(y)
    num_z = len(z)
    lcs_len_ = [[[0 for k in range(num_z+1)] for j in range(num_y+1)] for i in range(num_x+1)]

    def fill_lcs_len():
        for i in range(num_x):
            for j in range(num_y):
                for k in range(num_z):
                    if x[i] == y[j] == z[k]:
                        lcs_len_[i][j][k] = lcs_len_[i-1][j-1][k-1] + 1
                    else:
                        lcs_len_[i][j][k] = max(lcs_len_[i-1][j][k],
                                                lcs_len_[i][j-1][k],
                                                lcs_len_[i][j][k-1])
    fill_lcs_len()
    return lcs_len_


def three_sequence_back_track(lcs_len_, x, y, z, i, j, k):
    if i == -1 or j == -1 or k == -1:
        return EMPTY_STRING
    elif x[i] == y[j] == z[k]:
        return three_sequence_back_track(lcs_len_, x, y, z, i-1, j-1, k-1) + x[i]
    else:
        max_ = max([lcs_len_[i][j][k-1], lcs_len_[i][j-1][k], lcs_len_[i-1][j][k]])
        if lcs_len_[i][j][k-1] == max_:
            return three_sequence_back_track(lcs_len_, x, y, z, i, j, k-1)
        elif lcs_len_[i][j-1][k] == max_:
            return three_sequence_back_track(lcs_len_, x, y, z, i, j-1, k)
        else:
            return three_sequence_back_track(lcs_len_, x, y, z, i-1, j, k)


def three_sequence_dynamically_find_lcs(x, y, z):
    if (not x and not y) or (not x and not z) or (not x and not z):
        return EMPTY_STRING
    lcs_len_ = three_sequence_lcs_len(x, y, z)
    return three_sequence_back_track(lcs_len_, x, y, z, len(x) - 1, len(y) - 1, len(z) - 1)


def random_str(str_len):
    return EMPTY_STRING.join(random.choice(CHAR_CANDIDATES) for j in range(str_len))


def experiment_one():
    str_len = 20
    pair_num = 20
    print 'str_len: {}, pair_num: {}'.format(str_len, pair_num)
    timer_recursive.reset()
    timer_dynamic.reset()
    for i in range(pair_num):
        x = random_str(str_len)
        y = random_str(str_len)
        recursively_find_lcs(x, y)
        dynamically_find_lcs(x, y)
    print '{:.3f} {:.3f}'.format(timer_recursive.time_, timer_dynamic.time_)


def experiment_two():
    str_len_list = range(10, 21, 2)
    pair_num = 20
    for str_len in str_len_list:
        timer_recursive.reset()
        timer_dynamic.reset()
        for i in range(pair_num):
            x = random_str(str_len)
            y = random_str(str_len)
            recursively_find_lcs(x, y)
            dynamically_find_lcs(x, y)
        print '{} {:.3f} {:.3f}'.format(str_len, timer_recursive.time_, timer_dynamic.time_)
        # print '{} {:.3f}'.format(str_len, timer_dynamic.time_)


def main(args):
    if args[0] == '1':
        experiment_one()
    elif args[0] == '2':
        experiment_two()


if __name__ == '__main__':
    main(sys.argv[1:])

