import random
import string
from unittest import TestCase

from commun.utils.filter import (
  filter_bobines_papier_for_contrainte,
)

from commun.model.bobine_mere import BobineMere
from commun.model.contraintes import Contrainte


AVAILABLE_LAIZE = [130, 140, 150, 160, 173, 180, 190, 210, 240, 300, 320]
AVAILABLE_LENGTH = [500, 700]
AVAILABLE_COLOR = ['Orange', 'Blanc', 'Ivoire', 'Jaune', 'Ecru', 'Noir',
                   'Prune', 'Rouge', 'Vert', 'Marron', 'Ecru Enduit']
AVAILABLE_GRAMMAGE = [30, 32, 35, 40, 48]


def random_code(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_laize():
    return random.choice(AVAILABLE_LAIZE)


def random_length():
    return random.choice(AVAILABLE_LENGTH)


def random_color():
    return random.choice(AVAILABLE_COLOR)


def random_grammage():
    return random.choice(AVAILABLE_GRAMMAGE)


def fake_bobine_mere(code=None, laize=None, length=None, color=None, gr=None):
    if code is None:
        code = random_code()
    if laize is None:
        laize = random_laize()
    if length is None:
        length = random_length()
    if color is None:
        color = random_color()
    if gr is None:
        gr = random_grammage()

    return BobineMere(code=code, laize=laize, lenght=length, color=color, gr=gr)


class TestFilter(TestCase):

    def test_filter_bobines_papier_for_contrainte__no_contrainte(self):
        bobines = [fake_bobine_mere(), fake_bobine_mere(), fake_bobine_mere(), fake_bobine_mere()]
        contrainte = Contrainte()
        filtered_bobines = filter_bobines_papier_for_contrainte(bobines, contrainte)
        self.assertEqual(filtered_bobines, [])

    def test_filter_bobines_papier_for_contrainte__bobine_papier_contrainte(self):
        bobine_mere_1 = fake_bobine_mere()
        bobines = [fake_bobine_mere(), fake_bobine_mere(), bobine_mere_1, fake_bobine_mere()]
        contrainte = Contrainte(bobine_papier=bobine_mere_1)
        filtered_bobines = filter_bobines_papier_for_contrainte(bobines, contrainte)
        self.assertEqual(filtered_bobines, [bobine_mere_1])
