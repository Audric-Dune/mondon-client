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
values = ["Papier", "Polypro", "Papier & polypro"]
DROPDOWN_CHGT_BOB = {"titre": "Changement de bobine mère (bobine finie)",
                     "placeholder": "Sélectionner une bobine...",
                     "values": values}
values = ["Nouveau plan avec impression", "Nouveau plan sans impression"]
DROPDOWN_CHGT_FORMAT = {"titre": "Changement de plan de production",
                        "placeholder": "Nouveau avec ou sans impression ?",
                        "values": values}

LIST_CHOIX_RAISON_PREVU = [
    ("dropdown", DROPDOWN_CHGT_BOB),
    ("dropdown", DROPDOWN_CHGT_FORMAT),
    ("label", "Démarrage production SANS REGLAGE"),
    ("label", "Fin de journée"),
    ("text_edit", TEXT_EDIT_AUTRE)]

# Liste choix de raison d'un arrêt imprévu
TEXT_EDIT_ESSAI = {"titre": "Essai technique", "placeholder": "..."}
TEXT_EDIT_MAINTENANCE = {"titre": "Maintenance", "placeholder": "..."}
values = ["Calandre",
          "Groupe enrouleur",
          "Dérouleur papier",
          "Dérouleur polypro",
          "Perforation",
          "Groupe imprimeur",
          "Cadre guidage"]
DROPDOWN_CASSE = {"titre": "Casse", "placeholder": "Sélectionner une casse...", "values": values}

values = ["Bord flottant", "Choc sur bobine"]
DROPDOWN_QUALITE_BM = {"titre": "Problème qualité bobine mère",
                    "placeholder": "Sélectionner la qualité défectueuse...",
                    "values": values}

values = ["Impression",
          "Largeur : Mauvaise position couteaux",
          "Défaut perfo",
          "Flanc bobine fille inconvenable"]
DROPDOWN_QUALITE_BF = {"titre": "Problème qualité bobine fille",
                    "placeholder": "Sélectionner la qualité défectueuse...",
                    "values": values}

values = ["Buse de colle à chaud",
          "Bobine mère polypro",
          "Changement bande téflon"]
DROPDOWN_MAUVAIS_COLLAGE = {"titre": "Mauvais collage",
                    "placeholder": "Sélectionner la raison...",
                    "values": values}

LIST_CHOIX_RAISON_IMPREVU = [
    ("dropdown", DROPDOWN_CASSE),
    ("dropdown", DROPDOWN_MAUVAIS_COLLAGE),
    ("dropdown", DROPDOWN_QUALITE_BF),
    ("dropdown", DROPDOWN_QUALITE_BM),
    ("label", "Mauvais encollage axes cartons (colle à froid)"),
    ("text_edit", TEXT_EDIT_ESSAI),
    ("text_edit", TEXT_EDIT_MAINTENANCE),
    ("text_edit", TEXT_EDIT_AUTRE)]

# Liste choix d'une tache d'entretien

LIST_CHOIX_ENTRETIEN = [
    ("label", "Calandre"),
    ("label", "Couteau"),
    ("label", "Barre axe carton"),
    ("label", "Lame coupe"),
    ("label", "Bague perfo"),
    ("text_edit", TEXT_EDIT_AUTRE)]

