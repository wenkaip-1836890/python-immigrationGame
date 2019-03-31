'''FarmerFox_Array_VIS_FOR_TK.py
Version of Aug. 29, 2018. Works with the formulation of
Missionaries and Cannibals that uses a State class for
representing states.

'''

from show_state_array import initialize_tk, state_array, state_display, make_modalW

from tkinter import font

import importlib.util


WIDTH = 1700
HEIGHT = 900
TITLE = "My Beloved Leader"

PROBLEM1 = None

def load_file():
    try:
      spec = importlib.util.spec_from_file_location("My_Beloved_Leader", "My_Beloved_Leader" + ".py")
      global PROBLEM1
      PROBLEM1 = spec.loader.load_module()
      spec.loader.exec_module(PROBLEM1)
    except Exception as e:
      print(e)
      exit(1)

def initialize_vis():
    load_file()

    initialize_tk(WIDTH, HEIGHT, TITLE, PROBLEM1.choice_faction)

def render_state(s):

    # Note that font creation is only allowed after the Tk root has been
    # defined.  So we check here if the font creation is still needed,
    # and we do it (the first time this method is called).
    if PROBLEM1.year <= 2032.5:

        PROBLEM1.year += 0.5

        infos = [s.pp, s.stability, s.gov_support, s.money, s.citizen_approval]

        the_state_array = state_array()
        the_state_array.show(infos, PROBLEM1.year, PROBLEM1.Legal_immi, PROBLEM1.Illegal_immi)
        the_state_array.progress_bar(PROBLEM1.year)

        if PROBLEM1.year == 2023 or PROBLEM1.year == 2028 or PROBLEM1.year == 2033:
            make_modal_window(infos)

def make_modal_window(infos):
    return make_modalW(infos, PROBLEM1.year, PROBLEM1.choice_faction)
