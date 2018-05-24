from commun.model.bobine_fille_selected import BobineFilleSelected


# Determine s'il existe des combinaisons valides de bobines pour une refente.
# S'arrete de chercher après avoir trouvé `max_solutions`.
def get_bobine_fille_combinaisons_for_refente(refente, bobines_fille, bobines_fille_selected=None, max_solutions=1):
    if bobines_fille_selected is None:
        bobines_fille_selected = []
    # Prépare une liste avec les solutions
    combinaisons = Combinaisons()
    # Convertit la refente en RefenteBuffer
    initial_refente_buffer = RefenteBuffer(refente.laizes)
    # Récupère toutes les combinaisons possible de refente après avoir appliqué
    # les bobines filles sélectionnées
    refentes = initial_refente_buffer.get_combinaisons(bobines_fille_selected)
    # Groupe les bobines qui fonctionnent entre elles
    clusters = _group_bobines_fille(bobines_fille, bobines_fille_selected)
    # Test chacun des groupes et refente
    for refente in refentes:
        if refente.is_full():
            continue
        for cluster in clusters:
            # Convertit les BobineFille du groupe en BobineFilleSelected
            bobines_poses = [
                bobine_fille_selected
                for bobine_fille in cluster
                for bobine_fille_selected in [
                    BobineFilleSelected(bobine_fille, pose)
                    for pose in bobine_fille.poses
                ]
            ]
            # Group les BobineFilleSelected par laize
            bobine_poses_by_laize = {}
            for bobine_pose in bobines_poses:
                laize = bobine_pose.laize
                if not bobine_poses_by_laize.get(laize):
                    bobine_poses_by_laize[laize] = []
                bobine_poses_by_laize[laize].append(bobine_pose)
            # Test si il existe une combinaison valid dans ce groupe
            res = _is_valid_refente_for_bobines_pose(refente, bobine_poses_by_laize, max_solutions)
            # Si on trouve des combinaisons, on les ajoute au tableau des solutions
            # et on s'arrete dès qu'on en a assez.
            if res:
                for combi in res:
                    if max_solutions is not None and len(combinaisons.all()) >= max_solutions:
                        return combinaisons
                    combinaisons.add(combi)
    # Retourne toutes les combinaisons qu'on a trouvées
    return combinaisons.all(max_solutions)


# Représente une refente sur laquelle on peut appliquer des poses.
class RefenteBuffer:
    def __init__(self, laizes):
        # Copy les laizes de la refente pour pouvoir travailler dessus
        self.laizes = laizes[:]
        # Définit l'index de la première laize non-occupée
        self.index = self.get_first_free_laize_index()

    # Retourne l'index de la première laize qui n'est pas None.
    # Démarre à `start_index`.
    def get_first_free_laize_index(self, start_index=0):
        for i in range(start_index, len(self.laizes)):
            if self.laizes[i] is not None:
                return i
        return None

    # Vérifie si une bobine peut être appliquée sur la refente à un certain index
    def can_apply(self, bobine_selected, index):
        if self.laizes[index] is None:
            return False
        laize, size = self.get_current_laize(index)
        pose = 1 if bobine_selected.pose == 0 else bobine_selected.pose
        return laize == bobine_selected.laize and size >= pose

    # Génère toutes les combinaisons de refente en placant les bobine filles
    # dans les endroits disponible
    def get_combinaisons(self, bobines_selected):
        if not bobines_selected:
            return [self]
        refentes = []
        bobine_selected = bobines_selected[0]
        for i in range(len(self.laizes)):
            r = self.copy()
            if r.can_apply(bobine_selected, i):
                for laize_index in range(i, i + bobine_selected.pose):
                    r.laizes[laize_index] = None
                if len(bobines_selected) > 1:
                    for combi in r.get_combinaisons(bobines_selected[1:]):
                        combi.index = combi.get_first_free_laize_index()
                        refentes.append(combi)
                else:
                    r.index = r.get_first_free_laize_index()
                    refentes.append(r)
        return refentes

    # Retourne un tuple (laize, laize_size) définissant la laize courante (ou à partir d'un
    # certain index) ainsi que le nombre de laize de cette taille qui suivent.
    def get_current_laize(self, index=None):
        if index is None:
            index = self.index
        index = self.get_first_free_laize_index(index)
        if index is None:
            return None, None
        current_laize = self.laizes[index]
        counter = 1
        for laize in self.laizes[index + 1:]:
            if laize != current_laize:
                break
            counter += 1
        return current_laize, counter

    # Retourne la taille réelle d'une pose.
    @staticmethod
    def _get_real_pose(bobine_pose):
        return 1 if bobine_pose.pose == 0 else bobine_pose.pose

    # Applique une BobineFilleSelected sur la refente.
    def apply(self, bobine_pose):
        self.move_index(RefenteBuffer._get_real_pose(bobine_pose), 1)

    # Enlève une BobineFilleSelected de la refente.
    def restore(self, bobine_pose):
        self.move_index(RefenteBuffer._get_real_pose(bobine_pose), -1)

    def move_index(self, size, direction):
        counter = 0
        while counter < size:
            self.index += direction
            if self.index >= len(self.laizes) and direction > 0:
                self.index = len(self.laizes)
                break
            if self.index <= 0 and direction < 0:
                self.index = 0
                break
            if self.laizes[self.index] is not None:
                counter += 1

    # Indique si la refente est complète.
    def is_full(self):
        return self.index is None or self.get_first_free_laize_index(self.index) is None

    def copy(self):
        return RefenteBuffer(self.laizes[:])

    def __repr__(self):
        return 'RefenteBuffer({})[{}]'.format(', '.join([str(l) for l in self.laizes]), self.index)


# Représente une combinaison de BobineFilleSelected
# Cette classe est majoritairement utilisé pour dé-dupliquer les solutions
class Combinaisons:
    def __init__(self):
        self.list = []
        self.seen = set()

    def add(self, combi):
        h = hash(combi)
        if h in self.seen:
            return
        self.seen.add(h)
        self.list.append(combi)

    def all(self, limit=None):
        if limit is None:
            return self.list
        return self.list[0:limit]


# Sépare une liste de bobine en groupe de bobines qui ont les mêmes contraintes
# Si une liste de `bobines_contrainte` est spécifié, retourne uniquement le
# groupe de bobines qui satisfait ces `bobines_contrainte`.
def _group_bobines_fille(bobines_fille, bobines_contrainte):
    # Si il existe des bobines contraintes, super simple, on crée juste un seul groupe de
    # bobines qui fonctionnent avec la première bobine contrainte
    if bobines_contrainte:
        contrainte = bobines_contrainte[0]
        valid_bobines = [b for b in bobines_fille if
                         is_valid_bobine_fille_for_bobine_fille(b, contrainte)]
        return [valid_bobines]
    # Si il n'y a pas de bobines contraintes, on répartit les bobines par groupes qui fonctionnent
    # entre eux.
    clusters = []
    # Parcours les bobines
    for bobine in bobines_fille:
        is_added = False
        # Parcours les groupes
        for cluster in clusters:
            # On prend première bobine du groupe comme contrainte
            contrainte = cluster[0]
            # Si la bobine fonctionne avec la contrainte, on l'ajoute au groupe
            if is_valid_bobine_fille_for_bobine_fille(bobine, contrainte):
                cluster.append(bobine)
                is_added = True
                break
        # Si la bobine ne marche avec aucun groupe, on en crée un nouveau
        if not is_added:
            clusters.append([bobine])
    return clusters


# Méthode récursive qui détermine si il existe des combinaisons de BobineFilleSelected qui
# fonctionnent pour une RefenteBuffer.
# S'arrete de chercher après avoir trouvé `max_solutions`.
def _is_valid_refente_for_bobines_pose(refente_buffer, bobines_poses_by_laize, max_solutions):
    # Si la refente est complète, c'est gagné
    if refente_buffer.is_full():
        return []
    # Prépare une liste avec les solutions
    combinaisons = Combinaisons()
    # Récupère la laize courante ainsi que le nombre de place disponible pour cette laize
    laize, laize_size = refente_buffer.get_current_laize()
    # Récupère les bobines-pose avec la bonne laize
    bobines_poses = bobines_poses_by_laize.get(laize, [])
    # Parcours les BobineFilleSelected par index
    for bobine_pose_index in range(len(bobines_poses)):
        bobine_pose = bobines_poses[bobine_pose_index]
        pose = bobine_pose.pose
        # Check d'abord si la pose n'est pas trop grande
        if pose > laize_size:
            continue
        # Applique la BobineFilleSelected sur RefenteBuffer
        refente_buffer.apply(bobine_pose)
        # Enlève la BobineFilleSelected de la liste si la pose n'est pas 0
        if pose > 0:
            bobines_poses.pop(bobine_pose_index)
        # Appel récursif!
        res = _is_valid_refente_for_bobines_pose(refente_buffer, bobines_poses_by_laize, max_solutions)
        # Replace la BobineFilleSelected dans la liste si la pose n'est pas 0
        if pose > 0:
            bobines_poses.insert(bobine_pose_index, bobine_pose)
        # Restore RefenteBuffer
        refente_buffer.restore(bobine_pose)
        # Si on a trouvé des combinaisons, on ajoute la bobine courante à la fin de chacunes.
        if res is not None:
            if len(res) == 0:
                combinaisons.add((bobine_pose,))
            for combi in res:
                new_combi = tuple(sorted(combi + (bobine_pose,)))
                combinaisons.add(new_combi)
            if max_solutions is not None and len(combinaisons.all()) >= max_solutions:
                return combinaisons.all(max_solutions)
    # Retourne les combinaisons
    return None if not combinaisons else combinaisons.all()


# Compare si deux bobines filles sont compatible (copiée de filter.py)
def is_valid_bobine_fille_for_bobine_fille(bobine_fille, bobine_fille_contrainte):
    if not bobine_fille_contrainte:
        return True
    if bobine_fille.color != bobine_fille_contrainte.color:
        return False
    if bobine_fille.gr != bobine_fille_contrainte.gr:
        return False
    if bobine_fille.length != bobine_fille_contrainte.length:
        return False
    return True
