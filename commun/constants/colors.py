class Color:
    def __init__(self, hex_string):
        self.hex_string = hex_string
        self.rgb_components = Color.rgb_components_from_hex_string(hex_string)

    @staticmethod
    def rgb_components_from_hex_string(hex_string):
        # Enlève le "#"
        hex_string = hex_string[1:]
        # Sépare les trois couleurs
        red = hex_string[0:2]
        green = hex_string[2:4]
        blue = hex_string[4:6]
        # Convertis en tableau d'entier
        return [int(red, 16), int(green, 16), int(blue, 16)]


# Gestion des couleurs
color_noir = Color('#262626')
color_blanc = Color('#FFFFFF')

color_bleu_gris = Color('#2C3E50')
color_bleu = Color('#2980BD')
color_bleu_dune = Color('#0053a5')

color_jaune_dune = Color('#ffc30b')

color_vert = Color('#27AE60')
color_vert_moyen = Color('#1ABC9C')
color_vert_fonce = Color('#16A085')

color_orange = Color('#E67E22')
color_rouge = Color('#C0392B')
color_rouge_clair = Color('#E74C3C')

color_beige = Color('#ddd9c3')
color_gris = Color('#f2f2f2')
color_gris_moyen = Color('#BDC3C7')
color_gris_clair = Color('#ECF0F1')
color_gris_fonce = Color('#95A5A6')

# Gestion des couleurs bobines
bob_orange = Color("#e67e22")
bob_blanc = Color("#ffda79")
bob_ivoire = Color("#f7f1e3")
bob_jaune = Color("#f1c40f")
bob_ecru = Color("#f7d794")
bob_noir = Color("#3d3d3d")
bob_prune = Color("#9b59b6")
bob_rouge = Color("#e74c3c")
bob_vert = Color("#2ecc71")
bob_marron = Color("#784212")

