ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Rotor:
    def __init__(self, wiring: str, notch: str, name: str = ""):
        if len(wiring) != 26 or set(wiring) != set(ALPHABET):
            raise ValueError(f"Invalid wiring for rotor {name}")
        self.name = name
        self.wiring = wiring
        self.notch = notch
        self.position = 0
        self.ring_setting = 0

    def set_position(self, letter: str) -> None:
        self.position = ALPHABET.index(letter.upper())

    def set_ring(self, letter_or_index) -> None:
        if isinstance(letter_or_index, str):
            self.ring_setting = ALPHABET.index(letter_or_index.upper())
        else:
            self.ring_setting = letter_or_index

    def at_notch(self) -> bool:
        return ALPHABET[self.position] == self.notch

    def step(self) -> None:
        self.position = (self.position + 1) % 26

    def forward(self, c: int) -> int:
        shifted = (c + self.position - self.ring_setting) % 26
        mapped = ALPHABET.index(self.wiring[shifted])
        return (mapped - self.position + self.ring_setting) % 26

    def backward(self, c: int) -> int:
        shifted = (c + self.position - self.ring_setting) % 26
        mapped = self.wiring.index(ALPHABET[shifted])
        return (mapped - self.position + self.ring_setting) % 26


# Historical Enigma I rotor wirings
ROTOR_I = ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", "I")
ROTOR_II = ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", "II")
ROTOR_III = ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", "III")
ROTOR_IV = ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J", "IV")
ROTOR_V = ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z", "V")
