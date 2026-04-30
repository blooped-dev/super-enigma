from .rotor import ALPHABET


class Plugboard:
    def __init__(self, pairs=None):
        self.mapping = list(range(26))
        if pairs:
            self.set_pairs(pairs)

    def set_pairs(self, pairs) -> None:
        self.mapping = list(range(26))
        seen = set()
        for pair in pairs:
            if len(pair) != 2:
                raise ValueError(f"Plugboard pair must have 2 letters: {pair!r}")
            a, b = pair[0].upper(), pair[1].upper()
            if a == b:
                raise ValueError(f"Cannot wire letter to itself: {pair!r}")
            if a in seen or b in seen:
                raise ValueError(f"Letter used in more than one plug: {pair!r}")
            seen.add(a)
            seen.add(b)
            ai, bi = ALPHABET.index(a), ALPHABET.index(b)
            self.mapping[ai] = bi
            self.mapping[bi] = ai

    def swap(self, c: int) -> int:
        return self.mapping[c]
