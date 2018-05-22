import random
import string
from unittest import TestCase

from commun.model.refente import Refente
from commun.model.bobine_fille import BobineFille
from commun.model.bobine_fille_selected import BobineFilleSelected

from commun.utils.filter_matthis import get_bobine_fille_combinaisons_for_refente


length = 700
grammage = 30
code = 0


def get_code():
    global code
    code += 1
    return code


def build_bobine(laize, poses, color):
    return BobineFille(code=get_code(), laize=laize, poses=poses, color=color, length=length, gr=grammage)


def build_bobines(all_laize_and_poses, color="Blanc"):

    return [
        build_bobine(laize, poses, color)
        for (laize, poses) in all_laize_and_poses
    ]


def build_selected_bobines(all_laize_and_pose, color="Blanc"):
    return [
        BobineFilleSelected(build_bobine(laize, [pose], color), pose=pose)
        for (laize, pose) in all_laize_and_pose
    ]


def build_refente(*laizes):
    # Complète avec des None pour avoir 7 valeurs
    laizes = list(laizes) + [None for _ in range(0, 7 - len(laizes))]
    return Refente(code=get_code(), laize1=laizes[0], laize2=laizes[1], laize3=laizes[2],
                   laize4=laizes[3], laize5=laizes[4], laize6=laizes[5], laize7=laizes[6])


class TestFilterMatthis(TestCase):
    def test_filter(self):
        bobines = build_bobines([
            (130, [1]),
            (150, [1, 2]),
            (150, [1, 1, 1, 3]),
            (150, [0]),
        ])
        selected_bobines = build_selected_bobines([
            (130, 1),
            (150, 1),
        ])
        refente = build_refente(130, 150, 150, 150, 130, 150)

        res = get_bobine_fille_combinaisons_for_refente(refente, bobines, selected_bobines, max_solutions=None)
        self.assertEqual(len(res), 11)
