from pathlib import Path
import random
import typing as t

WORDS = [
    line.strip()
    for line in (Path(__file__).parent / "english-2048.txt").read_text().split("\n")
]

T = t.TypeVar("T")


def in_base(n: int, digits: t.Sequence[T]) -> t.Sequence[T]:
    """Given a list of "digits" for expressing numbers, return a list of the digits.

        >>> in_base(12345, '0123456789')
        ['1', '2', '3', '4', '5']
        >>> int(''.join(in_base(12345, '01234')), 5)
        12345

    """
    base = len(digits)
    digits_low_to_high: t.List[int] = []
    while n > 0:
        n, digit = divmod(n, base)
        digits_low_to_high.append(digit)
    return [digits[i] for i in reversed(digits_low_to_high)]


def int_to_english_string(n: int, separator: str = "-") -> str:
    return separator.join(in_base(n, WORDS))


def random_words(n_words: int, separator: str = "-", rng: t.Optional[random.Random] = None) -> str:
    bound = len(WORDS) ** n_words
    n = rng.randrange(bound) if (rng is not None) else random.randrange(bound)
    return int_to_english_string(n)
