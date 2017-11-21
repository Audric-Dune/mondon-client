# Database location
DATABASE_LOCATION = 'I:\data_prod_bob/mondon_arret.db'

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
LIST_CHOIX_RAISON_PREVU = [
    ("label", "Changement bobine papier"),
    ("label", "Changement bobine polypro"),
    ("label", "Réglage nouvelle production"),
    ("label", "Changement bobine papier et polypro"),
    ("label", "Démarrage production sans réglage"),
    ("label", "Fin de journée")
    ]
# Liste choix de raison d'un arrêt imprévu
# Définition dropdown
DROPDOWN_CASSE = ("Sélectionner une casse...", [
    "Casse calandre",
    "Casse enrouleur",
    "Casse dérouleur papier",
    "Casse dérouleur polypro"
    ])
DROPDOWN_TEST = ("Sélectionner un test...", [
    "Test calandre",
    "Test enrouleur",
    "Test dérouleur papier",
    "Test dérouleur polypro"
    ])
LIST_CHOIX_RAISON_IMPREVU = [
    ("dropdown", DROPDOWN_CASSE),
    ("label", "Mauvais encollage axes cartons"),
    ("label", "Problème buse colle à chaud"),
    ("dropdown", DROPDOWN_TEST),
    ("label", "Entretien machine"),
    ("label", "Essai technique"),
    ("label", "Maintenance")
    ]

