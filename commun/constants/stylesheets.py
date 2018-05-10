from commun.constants.colors import (
    color_blanc,
    color_bleu_gris,
    color_gris_moyen,
    color_gris_fonce,
    color_gris_clair,
    color_orange,
    color_rouge,
    color_rouge_clair,
    color_vert,
    color_vert_fonce,
    color_vert_moyen,
    color_noir,
    color_bleu,
    color_bleu_dune,
    color_jaune_dune)

# ____________LABEL STYLESHEET____________


def create_qlabel_stylesheet(background_color=None,
                             color=color_blanc,
                             font_size="14px",
                             padding="0px 5px 0px 5px",
                             bold=None,
                             italic=None):
    return """
        QLabel {{
            background-color: {background_color};
            color: {color};
            font-size: {font_size};
            padding: {padding};
            font-weight: {bold};
            font-style: {italic};
        }}
    """.format(
        background_color=background_color.hex_string if background_color else "transparent",
        color=color.hex_string,
        font_size=font_size,
        padding=padding,
        bold=bold,
        italic=italic
    )


white_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                  background_color=color_bleu_gris)
white_12_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     background_color=color_bleu_gris,
                                                     font_size="12px")
test_label_stylesheet = create_qlabel_stylesheet(color=color_orange,
                                                 background_color=color_vert,
                                                 font_size="14px")
orange_label_stylesheet = create_qlabel_stylesheet(color=color_orange)
red_label_stylesheet = create_qlabel_stylesheet(color=color_rouge)
white_title_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                        background_color=color_bleu_gris,
                                                        font_size="16px")
white_22_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     font_size="22px")
red_title_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                      background_color=color_rouge,
                                                      font_size="16px")
red_12_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                   background_color=color_rouge,
                                                   font_size="12px")
red_14_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                   background_color=color_rouge,
                                                   font_size="14px")
red_16_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                   background_color=color_rouge,
                                                   font_size="16px")
gray_16_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                    background_color=color_gris_moyen,
                                                    font_size="16px")
blue_16_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                    background_color=color_bleu,
                                                    font_size="16px")
blue_14_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                    background_color=color_bleu,
                                                    font_size="14px")
blue_title_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                       background_color=color_bleu,
                                                       font_size="16px")
blue_12_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                    background_color=color_bleu,
                                                    font_size="12px")
orange_title_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                         background_color=color_orange,
                                                         font_size="16px")
green_title_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                        background_color=color_vert_fonce,
                                                        font_size="16px")
green_12_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     background_color=color_vert_fonce,
                                                     font_size="12px")
green_14_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     background_color=color_vert_moyen,
                                                     font_size="14px")
gray_title_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                       background_color=color_gris_moyen,
                                                       font_size="16px")
gray_12_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                    background_color=color_gris_moyen,
                                                    font_size="12px")
white_12_bold_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                          background_color=color_bleu_gris,
                                                          font_size="12px",
                                                          bold="bold")
gray_14_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                    background_color=color_gris_moyen,
                                                    font_size="14px")
gris_moyen_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                       background_color=color_gris_moyen,
                                                       font_size="16px")
gris_fonce_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                       background_color=color_gris_fonce,
                                                       font_size="16px")
vert_fonce_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                       background_color=color_vert_fonce,
                                                       font_size="16px")
white_20_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     font_size="20px")
white_title_20_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                           background_color=color_bleu_gris,
                                                           font_size="20px")
disable_16_label_stylesheet = create_qlabel_stylesheet(color=color_gris_moyen,
                                                       font_size="16px")
white_16_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     font_size="16px")
white_16_bold_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                          font_size="16px",
                                                          bold="bold")
black_12_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                     font_size="12px")
black_16_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                     font_size="16px")
black_14_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                     font_size="14px")
black_20_label_stylesheet = create_qlabel_stylesheet(color=color_noir, font_size="20px")
white_24_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     font_size="24px")
bleu_gris_20_label_stylesheet = create_qlabel_stylesheet(color=color_bleu_gris,
                                                         background_color=color_blanc,
                                                         font_size="20px")
bleu_gris_16_label_stylesheet = create_qlabel_stylesheet(color=color_bleu_gris,
                                                         background_color=color_blanc,
                                                         font_size="16px")
green_20_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                     background_color=color_vert_fonce,
                                                     font_size="20px")
yellow_20_label_stylesheet = create_qlabel_stylesheet(color=color_noir,
                                                      background_color=color_jaune_dune,
                                                      font_size="20px")
green_maj_label_stylesheet = create_qlabel_stylesheet(color=color_blanc,
                                                      background_color=color_vert_fonce,
                                                      font_size="16px",
                                                      padding="0px 20px 0px 20px",
                                                      bold="bold")
red_16_bold_label_stylesheet = create_qlabel_stylesheet(color=color_rouge, font_size="16px", bold="bold")
red_12_bold_label_stylesheet = create_qlabel_stylesheet(color=color_rouge, font_size="12px", bold="bold")
green_16_bold_label_stylesheet = create_qlabel_stylesheet(color=color_vert_fonce, font_size="16px", bold="bold")
red_16_no_background_label_stylesheet = create_qlabel_stylesheet(color=color_rouge, font_size="16px")
green_16_label_stylesheet = create_qlabel_stylesheet(color=color_vert, font_size="16px")
orange_16_bold_label_stylesheet = create_qlabel_stylesheet(color=color_orange, font_size="16px", bold="bold")
blue_16_bold_label_stylesheet = create_qlabel_stylesheet(color=color_bleu_dune, font_size="16px", bold="bold")
blue_12_bold_label_stylesheet = create_qlabel_stylesheet(color=color_bleu_dune, font_size="12px", bold="bold")
dune_title_stylesheet = create_qlabel_stylesheet(color=color_jaune_dune,
                                                 font_size="20px",
                                                 background_color=color_bleu_dune)
gray_italic_stylesheet = create_qlabel_stylesheet(color=color_gris_fonce, font_size="12px", italic="italic")

# ____________BUTTON STYLESHEET____________

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
        border-width: 1px;
        border-color: {color_gris_moyen}
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
    color_rouge=color_rouge.hex_string,)

button_14_stylesheet = """
    QPushButton {{
        background-color: {color_vert_fonce};
        border-radius: 2;
        color: {color_blanc};
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
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
    color_rouge=color_rouge.hex_string,)

button_no_radius_stylesheet = """
    QPushButton {{
        background-color: none;
        border: none;
        color: {color_noir};
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
        color: {color_blanc};

    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
    }}
""".format(
    color_noir=color_noir.hex_string,
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,)

button_no_radius_no_hover_stylesheet= """
    QPushButton {{
        background-color: none;
        border: none;
        color: {color_noir};
        font-size: 14px;
    }}
""".format(
    color_noir=color_noir.hex_string,
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,)

button_red_stylesheet = """
    QPushButton {{
        background-color: {color_rouge};
        border-radius: 5;
        color: {color_blanc};
        font-size: 22px;
    }}
    QPushButton:hover {{
        background-color: {color_rouge_clair};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
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
    color_rouge_clair=color_rouge_clair.hex_string)

button_white_stylesheet = """
    QPushButton {{
        background-color: {color_blanc};
        text-align: left;
        padding-left: 5px;
        border-radius: 0;
        color: {color_bleu_gris};
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_fonce};
        color: {color_blanc};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
    }}
    QPushButton:disabled {{
        background-color: {color_gris_moyen};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_bleu_gris=color_bleu_gris.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,)

button_green_stylesheet = """
    QPushButton {{
        background-color: {color_vert_fonce};
        color: {color_blanc};
        text-align: left;
        padding-left: 5px;
        border-radius: 0;
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
        color: {color_blanc};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
    }}
    QPushButton:disabled {{
        background-color: {color_gris_moyen};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_bleu_gris=color_bleu_gris.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,)

button_little_stylesheet = """
    QPushButton {{
        background-color: {color_vert_fonce};
        border-radius: 5;
        color: {color_blanc};
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
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
    color_rouge=color_rouge.hex_string,)

button_little_red_stylesheet = """
    QPushButton {{
        background-color: {color_rouge};
        border-radius: 5;
        color: {color_blanc};
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {color_rouge_clair};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
    }}
    QPushButton:disabled {{
        background-color: {color_gris_moyen};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_rouge_clair=color_rouge_clair.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,)

button_stylesheet_unselected = """
    QPushButton {{
        background-color: {color_gris_moyen};
        border-radius: 5;
        color: {color_blanc};
        font-size: 22px;
    }}
    QPushButton:hover {{
        background-color: {color_gris_fonce};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
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
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)

button_menu_stylesheet = """
    QPushButton {{
        padding: 0px 10px 0px 10px;
        background-color: {color_vert_fonce};
        border: none;
        color: {color_blanc};
        font-size: 16px;
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)

button_menu_stylesheet_unselected = """
    QPushButton {{
        padding: 0px 10px 0px 10px;
        background-color: {color_gris_fonce};
        border: none;
        color: {color_blanc};
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
    }}
    QPushButton:disabled {{
        background-color: {color_gris_fonce};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)

button_arrow_stylesheet = """
    QPushButton {{
        background-color: {color_blanc};
        border: none;
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen};
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
    color_rouge=color_rouge.hex_string,)

button_red_cross_stylesheet = """
    QPushButton {{
        background-color: {color_rouge};
        border: none;
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,)

button_gray_cross_stylesheet = """
    QPushButton {{
        background-color: {color_gris_moyen};
        border: none;
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,)

button_blue_cross_stylesheet = """
    QPushButton {{
        background-color: {color_bleu};
        border: none;
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_bleu=color_bleu.hex_string,
    color_rouge=color_rouge.hex_string,)

button_dropdown_stylesheet = """
    QPushButton {{
        background-color: {color_blanc};
        color: {color_noir};
        padding-left: 5px;
        font-size: 16px;
        border-style: none;
        text-align:left;
    }}
    QPushButton:hover {{
        color: {color_vert_moyen};
    }}
    QPushButton:disabled {{
        background-color: {color_gris_moyen};
        color: {color_gris_clair};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,
    color_noir=color_noir.hex_string,
    color_gris_clair=color_gris_clair.hex_string)

button_dropdown_placeholder_stylesheet = """
    QPushButton {{
        background-color: {color_blanc};
        color: {color_gris_moyen};
        padding-left: 5px;
        font-size: 16px;
        border-style: none;
        text-align:left;
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_rouge=color_rouge.hex_string,
    color_noir=color_noir.hex_string,
    color_gris_clair=color_gris_clair.hex_string)

button_no_stylesheet = """
    QPushButton {
        background-color: none;
        border: none;
    }
"""

# ____________CHECK BOX STYLESHEET____________

check_box_off_stylesheet = """
    QPushButton {{
        background-color: {color_blanc};
        border-radius: 2px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)

check_box_on_stylesheet = """
    QPushButton {{
        background-color: {color_vert_fonce};
        border-radius: 2px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_fonce};
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)

check_box_disabled_stylesheet = """
    QPushButton {{
        background-color: {color_gris_moyen};
        border-radius: 2px;
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)

check_box_unselected_stylesheet = """
    QPushButton {{
        background-color: {color_gris_moyen};
        border-radius: 2px;
    }}
    QPushButton:hover {{
        background-color: {color_vert_moyen};
    }}
    QPushButton:pressed {{
        border-style: solid;
        border-width: 1px;
        border-color: {color_gris_moyen}
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)

# ____________TEXT EDIT STYLESHEET____________

white_text_edit_stylesheet = """
    QTextEdit {{
        background-color: {color_blanc};
        color: {color_vert};
        font-size: 14px;
        border: none;
    }}
""".format(
    color_vert=color_vert.hex_string,
    color_blanc=color_blanc.hex_string)

red_text_edit_stylesheet = """
    QTextEdit {{
        background-color: {color_blanc};
        color: {color_rouge};
        font-size: 14px;
        border: none;
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_rouge=color_rouge.hex_string)

# ____________LINE EDIT STYLESHEET____________

line_edit_stylesheet = """
    QLineEdit {{
        qproperty-frame: false;
        background-color: {color_blanc};
        color: {color_noir};
        font-size: 16px;
        border: none;
    }}
    QLineEdit:focus {{
        color: {color_vert_fonce};
    }}
""".format(
    color_vert_fonce=color_vert_fonce.hex_string,
    color_blanc=color_blanc.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_noir=color_noir.hex_string,)

line_edit_green_stylesheet = """
    QLineEdit {{
        qproperty-frame: false;
        background-color: {color_vert_fonce};
        color: {color_blanc};
        font-size: 16px;
        border: none;
        selection-background-color: {color_gris_fonce};
    }}
""".format(
    color_vert_fonce=color_vert_fonce.hex_string,
    color_blanc=color_blanc.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_noir=color_noir.hex_string,)

line_edit_red_stylesheet = """
    QLineEdit {{
        qproperty-frame: false;
        background-color: {color_blanc};
        color: {color_rouge};
        font-size: 16px;
        border: 1px solid {color_rouge};
        selection-background-color: {color_gris_fonce};
    }}
""".format(
    color_vert_fonce=color_vert_fonce.hex_string,
    color_blanc=color_blanc.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_noir=color_noir.hex_string,
    color_rouge=color_rouge.hex_string)

# ____________SCROLLBAR STYLESHEET____________

scroll_bar_stylesheet = """
QScrollBar:vertical {{
    background-color: {color_blanc};
    width: 14px;
    padding: 2px;
}}

QScrollBar::handle:vertical {{
    background-color: {color_gris_moyen};
    min-height: 20px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {color_gris_fonce};
}}

QScrollBar::handle:vertical:pressed {{
    background-color: {color_gris_fonce};
}}

QScrollBar::add-line:vertical {{
    width: 0px;
}}

QScrollBar::sub-line:vertical {{
    width: 0px;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: {color_blanc};
}}
""".format(
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_clair=color_gris_clair.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_blanc=color_blanc.hex_string)

# ____________RADIOBUTTON STYLESHEET____________

radio_button_stylesheet = """
    QRadioButton {{
        background: {color_vert_fonce}
    }}
""".format(
    color_blanc=color_blanc.hex_string,
    color_vert_fonce=color_vert_fonce.hex_string,
    color_vert_moyen=color_vert_moyen.hex_string,
    color_vert=color_vert.hex_string,
    color_gris_moyen=color_gris_moyen.hex_string,
    color_gris_fonce=color_gris_fonce.hex_string,
    color_rouge=color_rouge.hex_string,)
