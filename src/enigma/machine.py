from .rotor import Rotor, ALPHABET
from .reflector import Reflector
from .plugboard import Plugboard


class Enigma:
    def __init__(self, rotors, reflector: Reflector, plugboard: Plugboard = None,
                 positions: str = "AAA", rings=None):
        if len(rotors) != 3:
            raise ValueError("This Enigma uses exactly 3 rotors")
        if len(positions) != 3:
            raise ValueError("Need exactly 3 starting positions")
        self.rotors = [self._build_rotor(r) for r in rotors]
        self.reflector = reflector
        self.plugboard = plugboard or Plugboard()
        for rotor, pos in zip(self.rotors, positions):
            rotor.set_position(pos)
        if rings is not None:
            if len(rings) != 3:
                raise ValueError("Need exactly 3 ring settings")
            for rotor, ring in zip(self.rotors, rings):
                rotor.set_ring(ring)

    @staticmethod
    def _build_rotor(spec) -> Rotor:
        if isinstance(spec, Rotor):
            return Rotor(spec.wiring, spec.notch, spec.name)
        wiring, notch, name = spec
        return Rotor(wiring, notch, name)

    def _step_rotors(self) -> None:
        left, middle, right = self.rotors
        if middle.at_notch():
            middle.step()
            left.step()
        elif right.at_notch():
            middle.step()
        right.step()

    def encrypt_letter(self, letter: str) -> str:
        if not letter.isalpha():
            return letter
        self._step_rotors()
        c = ALPHABET.index(letter.upper())
        c = self.plugboard.swap(c)
        for rotor in reversed(self.rotors):
            c = rotor.forward(c)
        c = self.reflector.reflect(c)
        for rotor in self.rotors:
            c = rotor.backward(c)
        c = self.plugboard.swap(c)
        return ALPHABET[c]

    def encrypt(self, text: str) -> str:
        return "".join(self.encrypt_letter(ch) for ch in text if ch.isalpha())

    def process(self, text: str) -> str:
        out = []
        for ch in text:
            if ch.isalpha():
                out.append(self.encrypt_letter(ch))
            else:
                out.append(ch)
        return "".join(out)
