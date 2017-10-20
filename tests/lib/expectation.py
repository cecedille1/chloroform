# -*- coding: utf-8 -*-


def should_match_expectation(actual, expected):
    actual = iter(actual.split())
    expected = iter(expected.split())

    for act, exp in zip(actual, expected):
        any_position = exp.find('ANY')
        if any_position == -1:
            assert act == exp, '%s == %s' % (act, exp)
        elif exp == 'ANY':
            pass
        else:
            assert act.startswith(exp[:any_position]), '%s.startswith(%s)' % (act, exp[:any_position])
            assert act.endswith(exp[any_position + 3:]), '%s.endswith(%s)' % (act, exp[any_position + 3:])

    remain_actual =list(actual)
    assert not remain_actual
    remain_expected =list(expected)
    assert not remain_expected


def should_not_match_expectation(actual, expected):
    try:
        should_match_expectation(actual, expected)
    except AssertionError:
        pass
    else:
        raise AssertionError('{!r} match {!r}'.format(actual, expected))


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        should_match_expectation('abc', 'ANY')
        should_match_expectation('abc def', 'ANY ANY')
        should_match_expectation('abc def', 'abc def')
        should_match_expectation('abc def ghi', 'abc def ANY')
        should_match_expectation('abc def ghi', 'abc ANY ghi')
        should_match_expectation('abc def ghi', 'ANY def ghi')
        should_match_expectation('abc def ghi', 'ANY def ANY')
        should_match_expectation('abc defghi', 'ANY defANY')
        should_match_expectation('abc defghi', 'ANY ANYghi')
        should_match_expectation('abc defghi', 'ANY deANYi')

        should_not_match_expectation('abc def ghi', 'abc def jkl')
        should_not_match_expectation('abc def ghi', 'abc def ANY ANY')
        should_not_match_expectation('abc def ghi', 'ANY abc ANY')
        should_not_match_expectation('abc def ghi', 'ANY ANY def ghi')
        should_not_match_expectation('abc def ', 'abc def ANY')
    else:
        should_match_expectation(sys.argv[1], sys.argv[2])
