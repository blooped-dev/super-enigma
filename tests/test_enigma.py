import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "src"))

from enigma import (
    Enigma,
    Plugboard,
    REFLECTOR_B,
    ROTOR_I,
    ROTOR_II,
    ROTOR_III,
)


def make_machine(positions="AAA", plugs=None, rings=None):
    return Enigma(
        rotors=[ROTOR_I, ROTOR_II, ROTOR_III],
        reflector=REFLECTOR_B,
        plugboard=Plugboard(plugs) if plugs else Plugboard(),
        positions=positions,
        rings=rings,
    )


class EnigmaTests(unittest.TestCase):
    def test_encrypt_is_reciprocal(self):
        original = "HELLOWORLD"
        cipher = make_machine().encrypt(original)
        plain = make_machine().encrypt(cipher)
        self.assertEqual(plain, original)

    def test_no_letter_maps_to_itself(self):
        machine = make_machine()
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            cipher = machine.encrypt_letter(letter)
            self.assertNotEqual(cipher, letter)

    def test_known_simple_output(self):
        # With rotors I/II/III, reflector B, position AAA, rings AAA, no plugs:
        # 'AAAAA' encrypts to 'BDZGO' - well-documented Enigma I result.
        machine = make_machine()
        self.assertEqual(machine.encrypt("AAAAA"), "BDZGO")

    def test_plugboard_round_trip(self):
        plugs = ["AB", "CD", "EF"]
        original = "TESTINGTHEPLUGBOARD"
        cipher = make_machine(plugs=plugs).encrypt(original)
        plain = make_machine(plugs=plugs).encrypt(cipher)
        self.assertEqual(plain, original)

    def test_ring_settings_round_trip(self):
        rings = ["B", "C", "D"]
        original = "RINGSETTINGSWORK"
        cipher = make_machine(positions="QER", rings=rings).encrypt(original)
        plain = make_machine(positions="QER", rings=rings).encrypt(cipher)
        self.assertEqual(plain, original)

    def test_double_stepping(self):
        # ROTOR_II notch is 'E', ROTOR_III notch is 'V'. Starting at "ADV":
        # press 1: right at notch V -> middle advances D->E, right V->W
        # press 2: middle at notch E -> double-step: middle E->F AND left A->B
        machine = make_machine(positions="ADV")
        machine.encrypt_letter("A")
        self.assertEqual(
            [machine.rotors[0].position, machine.rotors[1].position, machine.rotors[2].position],
            [0, 4, 22],
        )
        machine.encrypt_letter("A")
        self.assertEqual(
            [machine.rotors[0].position, machine.rotors[1].position, machine.rotors[2].position],
            [1, 5, 23],
        )

    def test_non_alpha_passthrough(self):
        machine = make_machine()
        result = machine.process("HELLO, WORLD!")
        self.assertEqual(len(result), len("HELLO, WORLD!"))
        self.assertIn(",", result)
        self.assertIn(" ", result)
        self.assertIn("!", result)


class PlugboardTests(unittest.TestCase):
    def test_swap_pair(self):
        pb = Plugboard(["AB"])
        self.assertEqual(pb.swap(0), 1)
        self.assertEqual(pb.swap(1), 0)
        self.assertEqual(pb.swap(2), 2)

    def test_letter_to_self_rejected(self):
        with self.assertRaises(ValueError):
            Plugboard(["AA"])

    def test_letter_used_twice_rejected(self):
        with self.assertRaises(ValueError):
            Plugboard(["AB", "AC"])


if __name__ == "__main__":
    unittest.main()
