from predictionmarkets.util import in_base


def test_in_base():
    for base in range(2, 11):
        digits = "".join(str(d) for d in range(base))
        for n in [1, 2, 3, 5, 10, 20, 30, 50, 100]:
            assert int("".join(in_base(n, digits)), base) == n
