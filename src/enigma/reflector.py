from .rotor import ALPHABET


class Reflector:
    def __init__(self, wiring: str, name: str = ""):
        if len(wiring) != 26 or set(wiring) != set(ALPHABET):
            raise ValueError(f"Invalid wiring for reflector {name}")
        for i, ch in enumerate(wiring):
            j = ALPHABET.index(ch)
            if wiring[j] != ALPHABET[i]:
                raise ValueError(f"Reflector {name} wiring is not an involution")
        self.name = name
        self.wiring = wiring

    def reflect(self, c: int) -> int:
        return ALPHABET.index(self.wiring[c])


REFLECTOR_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT", "B")
REFLECTOR_C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL", "C")
