import random
import string
from unittest import TestCase

from commun.utils.filter import filter_bobines_papier_for_contrainte,\
    is_valid_refente_for_bobines_fille,\
    is_valid_bobine_fille_for_bobines_fille

from commun.model.bobine_mere import BobineMere
from commun.model.refente import Refente
from commun.model.bobine_fille import BobineFille
from commun.model.bobine_fille_selected import BobineFilleSelected
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


def fake_bobine_fille(code=None, laize=None, poses=None, color=None):
    if code is None:
        code = random_code()
    if poses is None:
        poses = [0]
    if color is None:
        color = random_color()
    return BobineFille(code=code, laize=laize, poses=poses, color=color)


class TestFilter(TestCase):

    def test_filter_bobines_papier_for_contrainte__no_contrainte(self):
        bobines = [fake_bobine_mere(), fake_bobine_mere(), fake_bobine_mere(), fake_bobine_mere()]
        contrainte = Contrainte()
        filtered_bobines = filter_bobines_papier_for_contrainte(bobines, contrainte)
        self.assertEqual(filtered_bobines, bobines)

    def test_filter_bobines_papier_for_contrainte__bobine_papier_contrainte(self):
        bobine_mere_1 = fake_bobine_mere()
        bobines = [fake_bobine_mere(), fake_bobine_mere(), bobine_mere_1, fake_bobine_mere()]
        contrainte = Contrainte(bobine_papier=bobine_mere_1)
        filtered_bobines = filter_bobines_papier_for_contrainte(bobines, contrainte)
        self.assertEqual(filtered_bobines, [bobine_mere_1])

    def test_is_valid_bobine_fille_for_bobines_fille__remove_pose_in_poses(self):
        bobine_0 = fake_bobine_fille(laize=150, poses=[2, 1])
        bobine_selected = BobineFilleSelected(bobine=bobine_0, pose=2)
        bobines = [bobine_selected]
        is_valid_bobine_fille_for_bobines_fille(bobine_fille=bobine_selected, bobines_fille=bobines)
        self.assertEqual(bobine_0.poses, [1])

    def test_is_valid_refente_for_bobines_fille__multi_the_same_pose_compatible(self):
        bobine_0 = fake_bobine_fille(laize=150, poses=[2])
        bobines_selected = [BobineFilleSelected(bobine=bobine_0, pose=2)]
        bobine_1 = fake_bobine_fille(laize=150, poses=[1, 1, 4])
        bobines = [bobine_1]
        refente = Refente(laize1=150, laize2=150, laize3=150, laize4=150)
        is_valid = is_valid_refente_for_bobines_fille(refente=refente,
                                                      bobines_fille=bobines,
                                                      bobines_fille_selected=bobines_selected)
        self.assertEqual(is_valid, True)

    def test_is_valid_refente_for_bobines_fille__multi_the_same_pose_not_compatible(self):
        bobine_0 = fake_bobine_fille(laize=150, poses=[1])
        bobines_selected = [BobineFilleSelected(bobine=bobine_0, pose=1)]
        bobine_1 = fake_bobine_fille(laize=150, poses=[1, 1, 4])
        bobines = [bobine_1]
        refente = Refente(laize1=150, laize2=150, laize3=150, laize4=150)
        is_valid = is_valid_refente_for_bobines_fille(refente=refente,
                                                      bobines_fille=bobines,
                                                      bobines_fille_selected=bobines_selected)
        self.assertEqual(is_valid, False)

    def test_is_valid_refente_for_bobines_fille__different_color(self):
        bobine_0 = fake_bobine_fille(laize=150, color="Jaune")
        bobine_1 = fake_bobine_fille(laize=140, color="Noir")
        bobine_2 = fake_bobine_fille(laize=130, color="Jaune")
        bobine_3 = fake_bobine_fille(laize=180, color="Jaune")
        bobines = [bobine_0, bobine_1, bobine_2, bobine_3]
        refente = Refente(laize1=150, laize2=140, laize3=130, laize4=180)
        is_valid = is_valid_refente_for_bobines_fille(refente=refente,
                                                      bobines_fille=bobines,
                                                      bobines_fille_selected=None)
        self.assertEqual(is_valid, False)
