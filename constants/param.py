# Database location
DATABASE_LOCATION = 'I:\data_prod_bob/mondon.db'
# DATABASE_LOCATION = '../mondon.db'

# Mot de passe
password = "dunesa"

# Hypothèse
VITESSE_LIMITE_ASSIMILATION_ARRET = 60
VITESSE_MOYENNE_MAXI = 172.5
PERCENT_PROD_THEROIQUE_MAXI = 82.12

# Horaire de production
DEBUT_PROD_MATIN = 6
FIN_PROD_MATIN = 14
DEBUT_PROD_SOIR = 14
FIN_PROD_SOIR = 22
FIN_PROD_MATIN_VENDREDI = 13
FIN_PROD_SOIR_VENDREDI = 20

# Définition dropdown
values = []
DROPDOWN_MODEL = {"titre": str, "placeholder": str, "values": values}

# Liste choix de raison d'un arrêt prévu
TEXT_EDIT_AUTRE = {"titre": "Autre", "placeholder": "Entrer une raison..."}
values = ["1 couleur", "2 couleurs", "3 couleurs"]
DROPDOWN_CLICHE = {"titre": "Pose de cliché(s)",
                   "placeholder": "Sélectionner le nombre de couleur...",
                   "values": values}

LIST_CHOIX_RAISON_PREVU = [
    ("label", "Changement bobine papier"),
    ("label", "Changement bobine polypro"),
    ("label", "Changement bobine papier et polypro"),
    ("dropdown", DROPDOWN_CLICHE),
    ("label", "Réglage nouvelle production"),
    ("label", "Démarrage production sans réglage"),
    ("label", "Démarrage production avec réglage"),
    ("label", "Fin de journée"),
    ("text_edit", TEXT_EDIT_AUTRE)
    ]
# Liste choix de raison d'un arrêt imprévu

values = ["Calandre", "Enrouleur", "Dérouleur papier", "Dérouleur polypro"]
DROPDOWN_CASSE = {"titre": "Casse", "placeholder": "Sélectionner une casse...", "values": values}

LIST_CHOIX_RAISON_IMPREVU = [
    ("dropdown", DROPDOWN_CASSE),
    ("label", "Mauvais encollage axes cartons"),
    ("label", "Mauvais enroulement bobine fille au démarage"),
    ("label", "Problème buse colle à chaud"),
    ("label", "Entretien machine"),
    ("label", "Essai technique"),
    ("label", "Maintenance"),
    ("text_edit", TEXT_EDIT_AUTRE)
    ]

# Liste choix d'une tache d'entretien
# Définition dropdown

values = ["Calandre", "Couteau", "Barre axe carton", "Lame de coupe"]
DROPDOWN_NETTOYAGE = {"titre": "Nettoyage", "placeholder": "Sélectionner un nettoyage...", "values": values}
values = ["N.1", "N.2", "N.3", "N.4", "N.5", "N.6", "N.7", "N.8", "N.9"]
DROPDOWN_N_BUSE = {"titre": "Changement buse", "placeholder": "Sélectionner un numero de buse...", "values": values}

LIST_CHOIX_ENTRETIEN = [
    ("dropdown", DROPDOWN_NETTOYAGE),
    ("dropdown", DROPDOWN_N_BUSE),
    ("label", "Changement bande téflon cylindre caoutchouc calandre"),
    ("label", "Changement radian perforation"),
    ("text_edit", TEXT_EDIT_AUTRE)
    ]

