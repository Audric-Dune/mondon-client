from commun.constants.param import PERCENT_PROD_THEROIQUE_MAXI
from commun.model.bobine_fille_valid import BobineFilleValid
from commun.model.bobine_fille_selected import BobineFilleSelected
from commun.stores.bobine_papier_store import bobine_papier_store
from commun.stores.bobine_poly_store import bobine_poly_store
from commun.stores.refente_store import refente_store
from commun.stores.perfo_store import perfo_store
from commun.stores.bobine_fille_store import bobine_fille_store


def get_bobine_papier(code):
    for bobine in bobine_papier_store.bobines:
        if bobine.code == code:
            return bobine


def get_bobine_poly(code):
    for bobine in bobine_poly_store.bobines:
        if bobine.code == code:
            return bobine


def get_refente(code):
    for refente in refente_store.refentes:
        if refente.code == code:
            return refente


def get_perfo_from_refente(refente):
    for perfo in perfo_store.perfos:
        if perfo.code == refente.code_perfo:
            return perfo


def get_bobines(code_bobines_filles):
    bobines = []
    code_bobines_filles_split = code_bobines_filles.split("_")
    index = 0
    while True:
        if code_bobines_filles_split[index]:
            bobine = bobine_fille_store.get_bobine(code_bobines_filles_split[index])
            bobine_selected = BobineFilleSelected(bobine=bobine,
                                                  pose=int(code_bobines_filles_split[index+1]),
                                                  index=int(code_bobines_filles_split[index+2]))
            bobines.append(bobine_selected)
            index += 3
        else:
            break
    return bobines


def init_store(store, items):
    for item in items:
        store.add_item(item)
    return store


def init_bobine_fille_store(store, bobines):
    for bobine in bobines:
        if bobine.sommeil == "Sommeil":
            pass
        elif bobine.vente_annuelle == 0:
            pass
        else:
            new_bobine = BobineFilleValid(bobine=bobine)
            store.add_item(new_bobine)
    return store


def get_time_prod(plan_prod):
    return (plan_prod.longueur * plan_prod.tours/3)*(PERCENT_PROD_THEROIQUE_MAXI/100)


def get_code_bobine_selected(bobines_filles_selected):
    def sort_item(items, sort_name, sort_asc):
        items = sorted(items, key=lambda b: b.get_value(sort_name), reverse=not sort_asc)
        return items
    sort_item(items=bobines_filles_selected, sort_name="index", sort_asc=True)
    code_bobines_selected = ""
    for bobine in bobines_filles_selected:
        code_bobines_selected += str(bobine.code)
        code_bobines_selected += "_"
        code_bobines_selected += str(bobine.pose)
        code_bobines_selected += "_"
        code_bobines_selected += str(bobine.index)
        code_bobines_selected += "_"
    return code_bobines_selected


def get_color_encrier_last_plan_prod(color):
    if color is None:
        return None
    elif color[0] == "_":
        return color
    else:
        return "_{}".format(color)
