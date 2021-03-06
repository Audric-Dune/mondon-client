from commun.model.bobine_fille_selected import BobineFilleSelected


def is_valid_refente_bobines_fille_bobines_fille_selected(refente, bobines_fille, bobines_fille_selected=None):
    if bobines_fille_selected is None:
        bobines_fille_selected = []
    initial_refente_buffer = RefenteBuffer(refente.laizes)
    refentes = initial_refente_buffer.get_combinaisons(bobines_fille_selected)
    if len(refentes) > 0 and refentes[0].is_full():
        return True
    return len(get_bobine_fille_combinaisons_for_refente(refente=refente,
                                                         bobines_fille=bobines_fille,
                                                         bobines_fille_selected=bobines_fille_selected,
                                                         max_solutions=1)) > 0


def is_valid_bobine_fille_and_pose_for_refente_bobines_filles_selected_with_bobines_filles(refente,
                                                                                           bobine_fille,
                                                                                           pose,
                                                                                           bobines_filles,
                                                                                           bobines_fille_selected=None):
    """
    On suppose que la bobine fille est dans bobine filles selected
    """
    new_bobine_fille_selected = BobineFilleSelected(bobine=bobine_fille, pose=pose)
    if bobines_fille_selected is None:
        bobines_fille_selected = []
    new_bobines_filles_selected = bobines_fille_selected + [new_bobine_fille_selected]
    new_bobines_filles = remove_bobine_fille_and_pose_in_bobines_filles(bobine_fille=bobine_fille,
                                                                        pose=pose,
                                                                        bobines_filles=bobines_filles)
    return is_valid_refente_bobines_fille_bobines_fille_selected(refente=refente,
                                                                 bobines_fille=new_bobines_filles,
                                                                 bobines_fille_selected=new_bobines_filles_selected)


def remove_bobine_fille_and_pose_in_bobines_filles(bobine_fille, pose, bobines_filles):
    if pose == 0:
        return bobines_filles
    new_bobines_filles = []
    for current_bobine in bobines_filles:
        if current_bobine.code == bobine_fille.code:
            new_poses = current_bobine.poses.copy().remove(pose)
            if new_poses:
                new_bobine = current_bobine.get_new_bobine_with_poses(poses=new_poses)
                new_bobines_filles.append(new_bobine)
        else:
            new_bobines_filles.append(current_bobine)
    return new_bobines_filles

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
                        # print("Combinaisons: ", combinaisons.all(max_solutions))
                        return combinaisons.all(max_solutions)
                    combinaisons.add(combi)
    # Retourne toutes les combinaisons qu'on a trouvées
    # print("Combinaisons: ", combinaisons.all(max_solutions))
    return combinaisons.all(max_solutions)


# Représente une refente sur laquelle on peut appliquer des poses.
class RefenteBuffer:
    def __init__(self, laizes):
        # Copy les laizes de la refente pour pouvoir travailler dessus
        self.laizes = laizes[:]
        # Définit l'index de la première laize non-occupée
        self.index = self.get_first_free_laize_index()
        # Initialise un encrier de taille 3
        self.encrier = Encriers(max_size=3)

    # Retourne l'index de la première laize qui n'est pas None.
    # Démarre à `start_index`.
    def get_first_free_laize_index(self, start_index=0):
        for i in range(start_index, len(self.laizes)):
            if self.laizes[i] is not None:
                return i
        return None

    # Vérifie si une bobine peut être appliquée sur la refente à un certain index
    def can_apply(self, bobine_selected, index=None):
        if index is None:
            index = self.index
        if self.laizes[index] is None:
            return False
        laize, size = self.get_current_laize(index)
        pose = self._get_real_pose(bobine_selected)
        return (laize == bobine_selected.laize and
                size >= pose and
                self.encrier.can_add_colors(bobine_selected.colors_cliche))

    # Génère toutes les combinaisons de refente en placant les bobine filles
    # dans les endroits disponible
    def get_combinaisons(self, bobines_selected):
        if not bobines_selected:
            return [self]
        refentes = []
        bobine_selected = bobines_selected[0]
        for i in range(len(self.laizes)):
            if self.can_apply(bobine_selected, i):
                r = self.copy()
                pose = self._get_real_pose(bobine_selected)
                for laize_index in range(i, i + pose):
                    r.laizes[laize_index] = None
                r.index = r.get_first_free_laize_index()
                r.encrier.add_colors(bobine_selected.colors_cliche)
                if len(bobines_selected) > 1:
                    for combi in r.get_combinaisons(bobines_selected[1:]):
                        combi.index = combi.get_first_free_laize_index()
                        refentes.append(combi)
                else:
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
    def _get_real_pose(bobine):
        return 1 if bobine.pose == 0 else bobine.pose

    # Applique une BobineFilleSelected sur la refente.
    def apply(self, bobine_pose):
        self.move_index(RefenteBuffer._get_real_pose(bobine_pose), 1)
        self.encrier.add_colors(bobine_pose.colors_cliche)

    # Enlève une BobineFilleSelected de la refente.
    def restore(self, bobine_pose):
        self.move_index(RefenteBuffer._get_real_pose(bobine_pose), -1)
        self.encrier.remove_colors(bobine_pose.colors_cliche)

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


# Représente une combinaison de couleurs utilisées avec une limite sur le nombre de couleurs
class Encriers:
    def __init__(self, max_size):
        self.max_size = max_size
        self.colors = {}

    def add_color(self, color):
        if color in self.colors:
            self.colors[color] += 1
        else:
            if self.is_full():
                raise Exception('Impossible d\'ajouter la couleur "{}", '
                                'l\'encrier est plein ({}).'
                                .format(color, ', '.join(self.colors.keys())))
            self.colors[color] = 1

    def add_colors(self, colors):
        if colors is None:
            return
        for color in colors:
            self.add_color(color)

    def remove_color(self, color):
        if color in self.colors:
            if self.colors[color] == 1:
                del(self.colors[color])
            else:
                self.colors[color] -= 1
        else:
            raise Exception('Impossible d\'enlever la couleur "{}", '
                            'l\'encrier ne la contient pas ({}).'.format(color, ', '.join(self.colors.keys())))

    def remove_colors(self, colors):
        if colors is None:
            return
        for color in colors:
            self.remove_color(color)

    def can_add_colors(self, colors):
        if colors is None:
            return True
        new_colors = set([c for c in colors if c not in self.colors])
        return len(self.colors) + len(new_colors) <= self.max_size

    def is_full(self):
        return len(self.colors) == self.max_size


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
        if not refente_buffer.can_apply(bobine_pose):
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
# Optimisation Audric
def is_valid_bobine_fille_for_bobine_fille(bobine_fille, bobine_fille_contrainte):
    if not bobine_fille_contrainte:
        return True
    if bobine_fille.contrainte != bobine_fille_contrainte.contrainte:
        return False
    return True
