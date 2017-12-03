# Database location
DATABASE_LOCATION = '../mondon.db'

# Hypothèse
VITESSE_LIMITE_ASSIMILATION_ARRET = 60

# Horaire de production
DEBUT_PROD_MATIN = 6
FIN_PROD_MATIN = 14
DEBUT_PROD_SOIR = 14
FIN_PROD_SOIR = 22
FIN_PROD_MATIN_VENDREDI = 13
FIN_PROD_SOIR_VENDREDI = 20

# Liste choix de raison d'un arrêt prévu
TEXT_EDIT_AUTRE = {"titre": "Autre", "placeholder": "Entrer une raison..."}

LIST_CHOIX_RAISON_PREVU = [
    ("label", "Changement bobine papier"),
    ("label", "Changement bobine polypro"),
    ("label", "Réglage nouvelle production"),
    ("label", "Changement bobine papier et polypro"),
    ("label", "Démarrage production sans réglage"),
    ("label", "Fin de journée"),
    ("text_edit", TEXT_EDIT_AUTRE)
    ]
# Liste choix de raison d'un arrêt imprévu
# Définition dropdown
values = []
DROPDOWN_MODEL = {"titre": str, "placeholder": str, "values": values}

values = ["Casse calandre", "Casse enrouleur", "Casse dérouleur papier", "Casse dérouleur polypro"]
DROPDOWN_CASSE = {"titre": "Casse", "placeholder": "Sélectionner une casse...", "values": values}

LIST_CHOIX_RAISON_IMPREVU = [
    ("dropdown", DROPDOWN_CASSE),
    ("label", "Mauvais encollage axes cartons"),
    ("label", "Problème buse colle à chaud"),
    ("label", "Entretien machine"),
    ("label", "Essai technique"),
    ("label", "Maintenance"),
    ]

