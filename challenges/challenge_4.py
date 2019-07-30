def fib(num):
    """
    :param num: Position of the fibonacci sequence
    :return: An int
    :runtime: O(2^n)
    """
    if num == 0:
        return 0

    elif num == 1:
        return 1

    return fib(num - 1) + fib(num - 2)


def memoize(func):
    memo = {0: 0, 1: 1}

    def helper(x):
        if x not in memo:
            memo[x] = func(x)

        return memo[x]

    return helper



def fib_memo(num):
    """
    :param num:
    :return:
    """
    if num == 0:
        return 0

    elif num == 1:
        return 1

    return fib_memo(num - 1) + fib_memo(num - 2)


fib_memo = memoize(fib_memo())
print(fib_memo(500))
