from pathlib import Path
import random
import typing as t

WORDS = [
    line.strip()
    for line in (Path(__file__).parent / "english-2048.txt").read_text().strip().split("\n")
]
N_WORDS = len(WORDS)
assert N_WORDS == 2**11
WORD_INDICES = {w: i for i, w in enumerate(WORDS)}

def int_to_words(n: int) -> t.Sequence[str]:
    if n < 0:
        raise ValueError("cannot convert negative number to words")
    result: t.List[str] = []
    while n > 0:
        n, digit = divmod(n, N_WORDS)
        result.append(WORDS[digit])
    return result

def words_to_int(words: t.Sequence[str]) -> int:
    result = 0
    for word in words[::-1]:
        result = N_WORDS*result + WORD_INDICES[word]
    return result

def random_words(n_words: int, rng: random.Random = random.Random()) -> t.Sequence[str]:
    return int_to_words(rng.randrange(N_WORDS**(n_words-1), N_WORDS**n_words))
