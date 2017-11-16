from constants.colors import (
    color_blanc,
    color_bleu_gris,
    color_gris_moyen,
    color_orange,
    color_rouge,
    color_vert,
    color_vert_fonce,
    color_vert_moyen,
)


def create_qlabel_stylesheet(background_color=color_bleu_gris, color=color_blanc, font_size="14px"):
    return """
        QLabel {{
            background-color: {background_color};
            color: {color};
            font-size: {font_size};
        }}
    """.format(
        background_color=background_color.hex_string,
        color=color.hex_string,
        font_size=font_size,
    )

white_label_stylesheet = create_qlabel_stylesheet(color=color_blanc)
orange_label_stylesheet = create_qlabel_stylesheet(color=color_orange)
red_label_stylesheet = create_qlabel_stylesheet(color=color_rouge)
white_title_label_stylesheet = create_qlabel_stylesheet(color=color_blanc, font_size="16px")

button_stylesheet = """
    QPushButton {{
        background-color: {color_vert_fonce};
        border-radius: 5;
        color: {color_blanc};
        font-size: 22px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 2px;
        border-color: {color_rouge}
    }}
    QPushButton:disabled {{
        background-color: {color_gris_moyen};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,
)

button_stylesheet_unselected = """
    QPushButton {{
        background-color: {color_gris_moyen};
        border-radius: 5;
        color: {color_blanc};
        font-size: 22px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 2px;
        border-color: {color_rouge}
    }}
    QPushButton:disabled {{
        background-color: {color_gris_moyen};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,
)

white_text_edit_stylesheet = """
    QTextEdit {{
        background-color: {color_bleu_gris};
        color: {color_blanc};
        font-size: 14px;
    }}
""".format(
    color_bleu_gris=color_bleu_gris.hex_string,
    color_blanc=color_blanc.hex_string,
)