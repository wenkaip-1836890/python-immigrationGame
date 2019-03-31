#!/usr/bin/python3
"""Tk_SOLUZION_Client.py
 This file implements a simple "SOLUZION" client that
 permits a user ("problem solver") to explore a search tree
 for a suitably-formulated problem.  The user only has to
 input single-character commands to control the search.
 Output is purely textual, and thus the complexity of a
 graphical interface is avoided.

 This client runs standalone -- no server connection.
 It thus provides a bare-bones means of testing a problem
 formulation.

 Tk is the graphics and GUI Toolkit that ships with Python.
 This client program uses Tk only for its graphics, setting up
 a graphics window that is used for the display of each state
 of the problem-solution process.

 To take advantage of this, the problem formulation file should
 check to see if the global USE_TK_GRAPHICS is True, and if so, it
 should import a visualization file with a name similar to:
 Missionaries_Array_VIS_FOR_TK.py.

 One technical challenge in creating this client is that Tk graphics
 requires that the main execution thread be devoted to Tk,
 which means that a normal text-input loop cannot easily be
 sync'd with Tk.  The solution is to use a separate thread for
 the text loop and have it make calls re-draw the Tk graphic.
 Tk still runs the mainloop method in the main thread, which
 not only is there to handle any GUI events (but there are not any
 in this program) but also just to show the graphics window.
 If we don't call the mainloop method, the Tk graphic window
 will not show up until the rest of the program completely
 finishes, which is useless.  So there is a separate thread
 here for the user interaction loop.

 Status: Started on Aug. 2.
   Aug. 3. Basic array graphics is working. But now we
   need the strings and advanced options.
   
   Need example file Missionaries_Array_VIS_FOR_TK.py.
   Need code to display a color array, with defaults if anything
      is not provided.
   Need code to display a corresponding string array.
      consider options to include column headers, footers, and
      row titles on left and right.
   Add caption feature.
   The file for these features:  show_state_array.py

----

PURPOSE OF THIS MODULE:
        
    This module supports what we can call "interactive state
    space search".  Whereas traditional search algorithms in the
    context of artificial intelligence work completely automatically,
    this module lets the user make the moves.  It provides support
    to the user in terms of computing new states, displaying that
    portion of the state space that the user has embodied, and
    providing controls to permit the user to adapt the presentation
    to his or her needs.  This type of tool could ultimately be a
    powerful problem solving tool, useful in several different
    modes of use: interactive processing of individual objects,
    programming by demonstration (the path from the root to any
    other node in the state space represents a way of processing
    any object similar in structure to that of the root object.)

    """

import time
import subprocess
import My_Beloved_Leader

# The following line is used in the Tk_SOLUZION_Client and the IDLE_Text_SOLUZION_Client.
problem_name = "./My_Beloved_Leader"


def client_mainloop():
    print(TITLE)
    print(PROBLEM.GAME_NAME + "; " + PROBLEM.GAME_VERSION)
    global STEP, DEPTH, OPERATORS, CURRENT_STATE, STATE_STACK, Legal_immi_STACK, Illegal_immi_STACK
    CURRENT_STATE = PROBLEM.copy_state(PROBLEM.INITIAL_STATE)

    STATE_STACK = [CURRENT_STATE]
    Legal_immi_STACK = [PROBLEM.Legal_immi]
    Illegal_immi_STACK = [PROBLEM.Illegal_immi]
    Last_operator = 8

    STEP = 0
    DEPTH = 0
    PROBLEM.render_state(CURRENT_STATE, PROBLEM.year, PROBLEM.Legal_immi, PROBLEM.Illegal_immi)

    while (True):
        if PROBLEM.has_election():
            subprocess.call(["afplay", "baker_arduous.wav"])
            if PROBLEM.make_modal_window(CURRENT_STATE, PROBLEM.year, PROBLEM.choice_faction):
                subprocess.call(["afplay", "applause_y.wav"])
                pass
            else:
                subprocess.call(["afplay", "The-Price-Is-Wrong.wav"])
                print("Your approval rating went below 50%")
                print("You have lost the game")
                print("Thank you for playing!")
                time.sleep(4)
                return

        print("\nStep " + str(STEP) + ", Depth " + str(DEPTH))
        print("CURRENT_STATE = " + str(CURRENT_STATE))
        if PROBLEM.goal_test(CURRENT_STATE):
            print('''CONGRATULATIONS!
You have solved the problem by reaching a goal state.
Do you wish to continue exploring?
''')
            answer = input("Y or N? >> ")
            if answer == "Y" or answer == "y":
                print("OK, continue")
            else:
                return

        for i in range(len(OPERATORS)):
            if i != Last_operator:
                print(str(i) + ": " + OPERATORS[i].name)

        command = input("Enter command: 0, 1, 2, etc. for operator; B-back; H-help; Q-quit. >> ")
        if command == "B" or command == "b":
            if len(STATE_STACK) > 1:
                STATE_STACK.pop()
                Legal_immi_STACK.pop()
                Illegal_immi_STACK.pop()
                DEPTH -= 1
                STEP += 1
            else:
                print("You're already back at the initial state.")
                continue
            CURRENT_STATE = STATE_STACK[-1]
            PROBLEM.Legal_immi = Legal_immi_STACK[-1]
            PROBLEM.Illegal_immi = Illegal_immi_STACK[-1]
            PROBLEM.year -= 0.5
            PROBLEM.render_state(CURRENT_STATE, PROBLEM.year, PROBLEM.Legal_immi, PROBLEM.Illegal_immi)
            continue

        if command == "H" or command == "h": show_instructions(); continue
        if command == "Q" or command == "q": break
        if command == "": continue
        try:
            i = int(command)
        except:
            print("Unknown command or bad operator number.")
            continue
        print("Operator " + str(i) + " selected.")

        if i < 0 or i >= len(OPERATORS):
            print("There is no operator with number " + str(i))
            continue

        if i == Last_operator:
            print("You have chosen the same policy half a year ago. You cannot choose it this time.")
            subprocess.call(["afplay", "Game-Show-Buzzer.wav"])
            continue

        CURRENT_STATE = OPERATORS[i].apply(CURRENT_STATE)
        STATE_STACK.append(CURRENT_STATE)
        Legal_immi_STACK.append(PROBLEM.Legal_immi)
        Illegal_immi_STACK.append(PROBLEM.Illegal_immi)
        Last_operator = i
        PROBLEM.year += 0.5
        PROBLEM.render_state(CURRENT_STATE, PROBLEM.year, PROBLEM.Legal_immi, PROBLEM.Illegal_immi)
        
        DEPTH += 1
        STEP += 1


def exit_client():
    print("Terminating Text_SOLUZION_Client session.")
    log("Exiting")
    exit()


def show_instructions():
    print('''\nINSTRUCTIONS:\n
        Welcome to My Beloved Leader,
        
        We are proud to present you the player to lead the most powerful nation in the world, The United States of America. The road ahead of you will be arduous, filled with many kinds of obstacles left and right, but we hope that you can make it through all 15 years of service without being kicked from office. It is important to bear in mind that your primary goal while in power is to correct the immigration crisis in this country and to maintain your authority while uplifting the happiness of your people.
        
        Listed below will be the resources available for you to utilize:
        Political points (pp) - These points are an manifestation of your authority and will be required to be spent if you want people to pay heed to your orders.
        Stability - This percentage will measure the economic stability of your country
        Citizen approval - The approval of your people will largely determine the result of your reelection.
        Money - Money inside the Federal Reserve (used for government programs/projects)
        
        Listed below will be the operators available for you to utilize:
        Immigration Forward - Support immigration? Then choose an immigration forward policy
        Immigration Backward - Immigration levels are too high? Then choose an immigration backward policy.
        Money Forward - Are your people being discontent and the economy is heading down? Then choose the Money Forward policy to increase government spending.
        Money Backward - Are you running out of money due to high amounts of spending? Then choose the Money Backward policy to recall government spending.
        Spend pp to increase government support for the policy of your choice
        
        Be careful though, what decisions you make now will affect the changes of your reelection down the road. With two more very important elections coming up, it's important that your people are supportive of the immigration policies that you’ve been passing. If the number of illegal immigrants are kept down while legal immigration goes up, then at the end of your 15 year term, your name may go down in history as “My Beloved Leader”''')


import sys, importlib.util

# Get the PROBLEM name from the command-line arguments

if len(sys.argv) < 2:
    """ The following few lines go with the LINUX version of the text client.
  print('''
       Usage: 
./IDLE_Text_SOLUZION_Client <PROBLEM NAME>
       For example:
./IDLE_Text_SOLUZION_Client Missionaries
  ''')
  exit(1)
  """
    sys.argv = ['Tk_SOLUZION_Client.py', problem_name]  # IDLE and Tk version only.
    # Sets up sys.argv as if it were coming in on a Linux command line.

problem_name = sys.argv[1]
print("problem_name = " + problem_name)

try:
    spec = importlib.util.spec_from_file_location(problem_name, problem_name + ".py")
    PROBLEM = spec.loader.load_module()
    # spec.loader.exec_module(PROBLEM)
except Exception as e:
    print(e)
    exit(1)

try:
    spec = importlib.util.spec_from_file_location(problem_name + '_Array_VIS_FOR_TK',
                                                  problem_name + '_Array_VIS_FOR_TK.py')
    VIS = spec.loader.load_module()
    spec.loader.exec_module(VIS)
    print("Using TK vis routine")
    PROBLEM.render_state = VIS.render_state
    PROBLEM.make_modal_window = VIS.make_modal_window
    
    VIS.initialize_vis(PROBLEM.country, PROBLEM.choice_faction)
except Exception as e:
    print(e)
    exit(1)

OPERATORS = PROBLEM.OPERATORS
STATE_STACK = []
Legal_immi_STACK = []
Illegal_immi_STACK = []

TITLE = "Tk_SOLUZION_Client (Version 0-1)"

import threading


class Client(threading.Thread):
    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        client_mainloop()
        self.root.quit()
        exit(0)
        # self.root.update()


# The following is only executed if this module is being run as the main
# program, rather than imported from another one.
if __name__ == '__main__':
    import show_state_array

    client = Client(show_state_array.STATE_WINDOW)
    show_state_array.STATE_WINDOW.mainloop()
    print("The session is finished.")
