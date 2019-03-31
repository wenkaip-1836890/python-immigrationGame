'''FarmerFox_Array_VIS_FOR_TK.py
Version of Aug. 29, 2018. Works with the formulation of
Missionaries and Cannibals that uses a State class for
representing states.

'''

from show_state_array import initialize_tk, state_array, state_display, make_modalW


WIDTH = 1700
HEIGHT = 900
TITLE = "My Beloved Leader"

def initialize_vis(country, choice_faction):
    initialize_tk(WIDTH, HEIGHT, TITLE, country, choice_faction)

def render_state(s, year, Legal_immi, Illegal_immi):
    # Note that font creation is only allowed after the Tk root has been
    # defined.  So we check here if the font creation is still needed,
    # and we do it (the first time this method is called).

    infos = [s.pp, s.stability, s.gov_support, s.money, s.citizen_approval]

    the_state_array = state_array()

    the_state_array.show(infos, year, Legal_immi, Illegal_immi)
    the_state_array.progress_bar(year)


def make_modal_window(s, year, choice_faction):

    infos1 = [s.pp, s.stability, s.gov_support, s.money, s.citizen_approval]

    return make_modalW(infos1, year, choice_faction)
