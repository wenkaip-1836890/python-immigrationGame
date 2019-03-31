'''My_Beloved_Leader.py
("My Beloved Leader" game)
A SOLUZION problem formulation.  UPDATED AUGUST 2018.
The XML-like tags used here may not be necessary, in the end.
But for now, they serve to identify key sections of this
problem formulation.  It is important that COMMON_CODE come
before all the other sections (except METADATA), including COMMON_DATA.
'''

# <METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "My Beloved Leader"
PROBLEM_VERSION = "1.0"
GROUP_MEMBERS = ['John Kim', 'Ken Pan', 'Guanxuan Wu', 'Haoyuan Chen']
GAME_CREATION_DATE = "6-SEPT-2018"
GAME_DESC = \
    '''This version differs from earlier ones by (a) using a new
State class to represent problem states, rather than just
a dictionary, and (b) avoidance of list comprehensions
and the use of default parameter values in lambda expressions.

The following are new methods here for the State version of
the formulation:
__eq__, __hash__, __str__, and the implcit constructor State().

The previous version was written to accommodate the
Brython version of the solving client
and the Brython version of Python.
However, everything else is generic Python 3, and this file is intended
to work a future Python+Tkinter client that runs on the desktop.
Anything specific to the Brython context should be in the separate 
file MissionariesVisForBRYTHON.py, which is imported by this file when
being used in the Brython SOLUZION client.

The operators are defined here in the same order as on the
worksheet "Depth-First Search for the M&C Problem."
'''
# </METADATA>

# <COMMON_DATA>
# </COMMON_DATA>

# <COMMON_CODE>
from random import *

import time

from show_state_array import close_window, show_media

class State:
    # initialization
    def __init__(self, old=None):
        self.pp = 1000  # political point
        self.stability = 52  # stability point
        self.gov_support = 60  # government policy support rate
        self.money = 100  # money (unit : a million dollars)
        self.citizen_approval = 55  # citizen approval rate for the president

        if not old is None: # copy state
            self.pp = old.pp
            self.stability = old.stability
            self.gov_support = old.gov_support
            self.money = old.money
            self.citizen_approval = old.citizen_approval

    # judge whether the player can make the policy
    def can_make(self, choice_policy):
        return True

    # calculate total support rate
    def Cal_government(self, choice_policy, gov_support):
        support = 0
        if self.stability >= 50:
            support = uniform(60, 68)
        else:
            support = uniform(62, 70)
        # if choose a left wing party
        if (choice_faction == "socialist" or choice_faction == "liberal"):
            right_wing = ["conservative", "populist"]
            n = randint(0, 1)
            opposite_faction = right_wing[n]
            left_ratio = 52
            change_ratio1 = randint(0, 5)
            change_ratio2 = randint(0, 5)
            left_ratio = left_ratio - change_ratio1 + change_ratio2
            right_ratio = 100 - left_ratio
            if (choice_policy == "immigration forward"):
                support = gov_support*uniform(0.98, 1.04)
            elif (choice_policy == "immigration backward"):
                if (opposite_faction == "conservative"):
                    if (self.stability >= 50):
                        support = (randint(30, 40)+gov_support)/2
                    elif (self.stability >= 40 and self.stability <= 50):
                        support = (randint(20, 30)+gov_support)/2
                    else:
                        support = (randint(10, 20)+gov_support)/2
                else:
                    support = (randint(20, 40)+gov_support)/2

        # if choose a right wing party
        elif (choice_faction == "conservative" or choice_faction == "populist"):
            left_wing = ["socialist", "liberal"]
            n = randint(0, 1)
            opposite_faction = left_wing[n]
            right_ratio = 52
            change_ratio1 = randint(0, 5)
            change_ratio2 = randint(0, 5)
            right_ratio = right_ratio - change_ratio1 + change_ratio2
            left_ratio = 100 - right_ratio
            if (choice_policy == "immigration forward"):
                if (opposite_faction == "liberal"):
                    if (self.stability >= 50):
                        support = (randint(30, 40) + gov_support) / 2
                    elif (self.stability >= 40 and self.stability <= 50):
                        support = (randint(20, 30) + gov_support) / 2
                    else:
                        support = (randint(10, 20) + gov_support) / 2
                else:
                    support = (randint(20, 40) + gov_support) / 2
        
            elif (choice_policy == "immigration backward"):
                support = gov_support*uniform(0.98, 1.04)

        # if choose a neutral party
        elif (choice_faction == "centrist"):
            '''left_wing = ["socialist", "liberal"]
            right_wing = ["conservative", "populist"]
            n1 = randint(0, 1)
            n2 = randint(0, 1)
            left_faction = left_wing[n]
            right_faction = right_wing[n]
            support_rate = randint(40, 60)'''
            if (choice_policy == "immigration backward" or choice_policy == "immigration forward"):
                support = gov_support*uniform(0.8, 1.1)

        return support

    # make the policy and update the data
    def make(self, choice_policy):
        global Legal_immi, Illegal_immi
        news = State(old=self)  # Make a copy of the current state.
        if (choice_policy != "money forward" and choice_policy != "money backward"):
            news.gov_support = news.Cal_government(choice_policy, news.gov_support)

            if news.gov_support < 50:
                print("You couldn't make this policy! You have only " + str(news.gov_support) + "% support rate for the policy.")
            else:
                # left wing parties
                if (choice_faction == "socialist" or choice_faction == "liberal"):
                    if (choice_policy == "immigration forward"):
                        # self.gov_support += 4
                        news.stability += 5
                        news.pp += 100
                        news.citizen_approval += 4

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)),
                                            int(600000 * (80000000 / Legal_immi)))
                        Legal_immi += immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.96, 1.09))
                        Illegal_immi = int(Illegal_immi * uniform(0.98, 1.08))
                    elif (choice_policy == "immigration backward"):
                        # self.gov_support -= 4
                        news.stability -= 5
                        news.pp -= 100
                        news.citizen_approval -= 8

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)),
                                            int(600000 * (80000000 / Legal_immi)))
                        Legal_immi -= immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.91, 1.04))
                        Illegal_immi -= randint(200000, 600000)
                        Illegal_immi = int(Illegal_immi * uniform(0.92, 1.02))

                # right wing parties
                elif (choice_faction == "conservative" or choice_faction == "populist"):
                    if (choice_policy == "immigration forward"):
                        # self.gov_support -= 4
                        news.stability -= 5
                        news.pp -= 100
                        news.citizen_approval -= 8

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)),
                                            int(600000 * (80000000 / Legal_immi)))
                        Legal_immi += immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.96, 1.09))
                        Illegal_immi = int(Illegal_immi * uniform(0.98, 1.08))
                    elif (choice_policy == "immigration backward"):
                        # self.gov_support += 4
                        news.stability += 5
                        news.pp += 100
                        news.citizen_approval += 4

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)),
                                            int(600000 * (80000000 / Legal_immi)))
                        Legal_immi -= immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.91, 1.04))
                        Illegal_immi -= randint(200000, 600000)
                        Illegal_immi = int(Illegal_immi * uniform(0.92, 1.02))
                # neutral parties
                else:
                    point1 = randrange(-2, 3, 4)
                    point2 = randrange(-100, 101, 200)
                    news.gov_support += point1
                    news.stability += point1
                    news.pp += point2
                    news.citizen_approval += point1
                    Legal_immi = int(Legal_immi * uniform(0.95, 1.05))
                    Illegal_immi = int(Illegal_immi * uniform(0.95, 1.05))


        # money policies posted by all parties
        if (choice_policy == "money forward" or choice_policy == "money backward"):
            print("Where do you want to spend/save money on" \
                  + "(invest in employment centers[a]/invest in public transportation[b]/invest in tighter border enforcement[c]/send foreign aid[d]): ",
                  end="")
            time.sleep(0.2)
            a_d = choice(['a', 'b', 'c', 'd'])
            print(a_d)
            '''while (choice != 'a' and choice != 'b' and choice != 'c' and choice != 'd'):
                print("Invalid input!")
                choice = input("Please enter again: ")
            '''
            money = 0
            # key = ''

            if (choice == 'a'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "invest in employment centers"
            elif (choice == 'b'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "invest in public transportation"
            elif (choice == 'c'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "invest in tighter border enforcement"
            elif (choice == 'd'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "send foreign aid"

            '''if (money_use[key] < money):
                print("You must input up to " + str(money_use[key]) + "$.")
            '''

            if (choice_policy == "money forward"):
                news.money -= money
                rate1 = randint(2, 4)
                rate2 = randint(2, 4)
                rate3 = randint(2, 4)
                news.pp += self.pp * rate1 / 100
                news.stability += self.stability * rate2 / 100
                news.citizen_approval += self.citizen_approval * rate3 / 100
            else:
                news.money += money
                rate1 = randint(2, 4)
                rate2 = randint(2, 4)
                rate3 = randint(2, 4)
                news.pp -= self.pp * rate1 / 100
                news.stability -= self.stability * rate2 / 100
                news.citizen_approval -= self.citizen_approval * rate3 / 100

        news.pp = news.pp * uniform(0.95, 1.05)
        if news.pp > 1500:
            news.pp -= uniform(40, 150)
        if news.pp < 400:
            news.pp += uniform(60, 200)
        if news.pp < 0:
            news.pp = 0

        news.gov_support = news.gov_support * uniform(0.95, 1.05)
        if news.gov_support > 80:
            news.gov_support -= uniform(5.8, 10)
        elif news.gov_support > 70:
            news.gov_support -= uniform(2.3, 5.7)
        if news.gov_support > 88:
            news.gov_support = 88
        if news.gov_support < 15:
            news.gov_support = 15

        news.money = news.money * uniform(0.9, 1.1)

        news.stability = news.stability * uniform(0.95, 1.08)
        if news.stability > 85:
            news.stability -= uniform(4.0, 8.0)
        elif news.stability > 75:
            news.stability -= uniform(1.0, 4.0)
        if news.stability > 95:
            news.stability = 95
        if news.stability < 10:
            news.stability = 10

        if news.stability >= 50:
            news.citizen_approval = news.citizen_approval * uniform(0.95, 1.1)
        else:
            news.citizen_approval = news.citizen_approval * uniform(0.92, 1.1)

        if news.citizen_approval >78:
            news.citizen_approval -= uniform(5, 10)
        elif news.citizen_approval >68:
            news.citizen_approval -= uniform(1, 2)

        Legal_immi = int(Legal_immi*uniform(0.99, 1.01))
        Illegal_immi = int(Illegal_immi * uniform(0.99, 1.01))

        #global year
        #year += 0.5

        media(choice_policy)
        
        show_media(choice_policy, choice_faction)

        return news


    def make_double(self, choice_policy):
        global Legal_immi, Illegal_immi
        # news = State(old=self)  # Make a copy of the current state.

        self.gov_support = self.Cal_government(choice_policy, self.gov_support)
        if (choice_policy != "money forward" and choice_policy != "money backward"):

            if self.gov_support < 50:
                print("You cannot make this policy! You have only " + str(self.gov_support) + "% support rate.")
            else:
                # left wing parties
                if (choice_faction == "socialist" or choice_faction == "liberal"):
                    if (choice_policy == "immigration forward"):
                        #self.gov_support += 4
                        self.stability += 5
                        self.pp += 100
                        self.citizen_approval += 4

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)), int(600000 * (80000000 / Legal_immi)))
                        Legal_immi += immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.96, 1.09))
                        Illegal_immi = int(Illegal_immi * uniform(0.98, 1.08))
                    elif (choice_policy == "immigration backward"):
                        #self.gov_support -= 4
                        self.stability -= 5
                        self.pp -= 100
                        self.citizen_approval -= 8

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)), int(600000 * (80000000 / Legal_immi)))
                        Legal_immi -= immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.91, 1.04))
                        Illegal_immi -= randint(200000, 600000)
                        Illegal_immi = int(Illegal_immi * uniform(0.92, 1.02))

                # right wing parties
                elif (choice_faction == "conservative" or choice_faction == "populist"):
                    if (choice_policy == "immigration forward"):
                        #self.gov_support -= 4
                        self.stability -= 5
                        self.pp -= 100
                        self.citizen_approval -= 8

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)), int(600000 * (80000000 / Legal_immi)))
                        Legal_immi += immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.96, 1.09))
                        Illegal_immi = int(Illegal_immi * uniform(0.98, 1.08))
                    elif (choice_policy == "immigration backward"):
                        #self.gov_support += 4
                        self.stability += 5
                        self.pp += 100
                        self.citizen_approval += 4

                        immi_chan = randint(int(300000 * (80000000 / Legal_immi)), int(600000 * (80000000 / Legal_immi)))
                        Legal_immi -= immi_chan
                        Legal_immi = int(Legal_immi * uniform(0.91, 1.04))
                        Illegal_immi -= randint(200000, 600000)
                        Illegal_immi = int(Illegal_immi * uniform(0.92, 1.02))
                # neutral parties
                else:
                    point1 = randrange(-2, 3, 4)
                    point2 = randrange(-100, 101, 200)
                    self.gov_support += point1
                    self.stability += point1
                    self.pp += point2
                    self.citizen_approval += point1
                    Legal_immi = int(Legal_immi * uniform(0.95, 1.05))
                    Illegal_immi = int(Illegal_immi * uniform(0.95, 1.05))

        # money policies posted by all parties
        if (choice_policy == "money forward" or choice_policy == "money backward"):
            print("Where do you want to spend/save money on" \
                  + "(invest in employment centers[a]/invest in public transportation[b]/invest in tighter border enforcement[c]/send foreign aid[d]): ", end="")
            time.sleep(0.2)
            a_d = choice(['a', 'b', 'c', 'd'])
            print(a_d)
            '''while (choice != 'a' and choice != 'b' and choice != 'c' and choice != 'd'):
                print("Invalid input!")
                choice = input("Please enter again: ")
            '''
            money = 0
            # key = ''

            if (choice == 'a'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "invest in employment centers"
            elif (choice == 'b'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "invest in public transportation"
            elif (choice == 'c'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "invest in tighter border enforcement"
            elif (choice == 'd'):
                print("How much money would you like to spend/save (up to 20$): ", end="")
                money = randint(1, 20)
                time.sleep(0.2)
                print(money)
                # key = "send foreign aid"

            '''if (money_use[key] < money):
                print("You must input up to " + str(money_use[key]) + "$.")
            '''

            if (choice_policy == "money forward"):
                self.money -= money
                rate1 = randint(2, 4)
                rate2 = randint(2, 4)
                rate3 = randint(2, 4)
                self.pp += self.pp * rate1 / 100
                self.stability += self.stability * rate2 / 100
                self.citizen_approval += self.citizen_approval * rate3 / 100
            else:
                self.money += money
                rate1 = randint(2, 4)
                rate2 = randint(2, 4)
                rate3 = randint(2, 4)
                self.pp -= self.pp * rate1 / 100
                self.stability -= self.stability * rate2 / 100
                self.citizen_approval -= self.citizen_approval * rate3 / 100

        self.pp = self.pp * uniform(0.95, 1.05)
        if self.pp > 1500:
            self.pp -= uniform(40, 150)
        if self.pp < 400:
            self.pp += uniform(60, 200)
        if self.pp < 0:
            self.pp = 0


        self.gov_support = self.gov_support * uniform(0.95, 1.05)
        if self.gov_support > 80:
            self.gov_support -= uniform(5.8, 10)
        elif self.gov_support > 70:
            self.gov_support -= uniform(2.3, 5.7)
        if self.gov_support > 88:
            self.gov_support = 88
        if self.gov_support < 15:
            self.gov_support = 15

        self.money = self.money * uniform(0.9, 1.1)

        self.stability = self.stability * uniform(0.95, 1.08)
        if self.stability > 85:
            self.stability -= uniform(4.0, 8.0)
        elif self.stability > 75:
            self.stability -= uniform(1.0, 4.0)
        if self.stability > 95:
            self.stability = 95
        if self.stability < 10:
            self.stability = 10

        if self.stability >= 50:
            self.citizen_approval = self.citizen_approval * uniform(0.95, 1.1)
        else:
            self.citizen_approval = self.citizen_approval * uniform(0.92, 1.1)

        if self.citizen_approval >78:
            self.citizen_approval -= uniform(5, 10)
        elif self.citizen_approval >68:
            self.citizen_approval -= uniform(1, 2)


        Legal_immi = int(Legal_immi * uniform(0.99, 1.01))
        Illegal_immi = int(Illegal_immi * uniform(0.99, 1.01))

        #global year
        #year += 0.5

        media(choice_policy)

        show_media(choice_policy, choice_faction)

    # print the policy content
    '''def print_policy(self, choice_policy):
        news = State(old=self)  # Make a copy of the current state.

        for key in policy:
            if (key == choice_policy):
                print(policy[key])

        return news
    '''
    # increase government support rate
    def increase_support(self, choice_policy):
        print("How much pp do you want to convert?: ", end="")
        ch1 = randint(70, 220)
        time.sleep(0.2)
        print(ch1)

        self.pp -= ch1
        self.gov_support += ch1 / 10


        if choice_policy == "immigration forward":
            if self.can_make("immigration forward"):
                self.make_double("immigration forward")
        elif choice_policy == "immigration backward":
            if self.can_make("immigration backward"):
                self.make_double("immigration backward")
        elif choice_policy == "money forward":
            if self.can_make("money forward"):
                self.make_double("money forward")
        elif choice_policy == "money backward":
            if self.can_make("money backward"):
                self.make_double("money backward")

        news = State(old=self)  # Make a copy of the current state.
        return news

    def describe_state(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        nmr = self.n_missionaries_on_right
        ncr = self.n_cannibals_on_right
        txt = "M on left:" + str(3 - nmr) + "\n"
        txt += "C on left:" + str(3 - ncr) + "\n"
        txt += "  M on right:" + str(nmr) + "\n"
        txt += "  C on right:" + str(ncr) + "\n"
        side = 'left'
        if self.n_boats_on_right == 1: side = 'right'
        txt += " boat is on the " + side + ".\n"
        return txt

    def is_goal(self):
        if (self.pp ==0 or self.stability < 25 or self.citizen_approval < 25 or self.money <= 0):
            print("You have lost the game")
            close_window("lost", "your administration is too unstable")

        if (Legal_immi < Illegal_immi):
            print("You have lost the game")
            close_window("lost", "the number of illegal immigrants has exceeded that of legal immigrants")

        if (has_election() and self.citizen_approval < 50):
            print("You have lost the game")
            close_window("lost", "You have lost the "+str(int(year))+" election")

        if has_election():
            if lose_check():
                print("You have lost the game")
                close_window("lost", "You did not satisfy the requirement regarding the number of legal and illegal immigrants")

        if (year == 2033 and self.citizen_approval >= 50):
            print("CONGRATULATIONS! You have solved the problem by reaching a goal state.")
            close_window("won", "very good")


    def __eq__(self, s2):
        if s2 == None: return False
        if self.n_boats_on_right != s2.n_boats_on_right: return False
        if self.n_missionaries_on_right != s2.n_missionaries_on_right: return False
        if self.n_cannibals_on_right != s2.n_cannibals_on_right: return False
        return True

    # print the current state
    def __str__(self):
        st = '(pp:' + str(self.pp)
        st += ', stability:' + str(self.stability)
        st += ', gov_support:' + str(self.gov_support)
        st += ', budget:' + str(self.money)
        st += ', citizen_approval:' + str(self.citizen_approval) + ')'
        return st

    def __hash__(self):
        return (str(self)).__hash__()


def goal_test(s): s.is_goal()


def goal_message(s):
    return "You have successfully become the beloved leader of United State of America!"

# copy state
def copy_state(s):
    return State(old=s)

def has_election():
    if year == 2023 or year == 2028 or year == 2033:
        return True
    else:
        return False


def lose_check():
    a = Legal_immi - 47000000
    b = Illegal_immi - 11200000
    if choice_faction == 'liberal' or choice_faction == 'socialist':
        Req_le_immi = [5000000, 9000000, 14000000]
    elif choice_faction == 'conservative' or choice_faction == 'populist':
        Req_le_immi = [-5000000, -9000000, -14000000]
        Req_ille_immi = [-2000000, -4000000, -6000000]
    elif choice_faction == 'centrist':
        Req_le_immi = [2000000, 4000000, 6000000]
        Req_ille_immi = [-1500000, -2500000, -3000000]

    if year==2023:
        if choice_faction == 'liberal' or choice_faction == 'socialist' or choice_faction == 'centrist':
            if a < Req_le_immi[0]: return True
        else:
            if a > Req_le_immi[0]: return True

        if choice_faction == 'conservative' or choice_faction == 'populist' or choice_faction == 'centrist':
            if b > Req_ille_immi[0]: return True

    elif year==2028:
        if choice_faction == 'liberal' or choice_faction == 'socialist' or choice_faction == 'centrist':
            if a < Req_le_immi[1]: return True
        else:
            if a > Req_le_immi[1]: return True

        if choice_faction == 'conservative' or choice_faction == 'populist' or choice_faction == 'centrist':
            if b > Req_ille_immi[1]: return True

    elif year==2033:
        if choice_faction == 'liberal' or choice_faction == 'socialist' or choice_faction == 'centrist':
            if a < Req_le_immi[2]: return True
        else:
            if a > Req_le_immi[2]: return True

        if choice_faction == 'conservative' or choice_faction == 'populist' or choice_faction == 'centrist':
            if b > Req_ille_immi[2]: return True

    return False

def media(choice_policy):

    # media report on the policies
    positive_policy_effect = ["5% increase in stability", \
                              "4% increase in citizen approval rate for the president", \
                              "100 point increase in political power"]
    negative_policy_effect = ["5% decrease in stability", \
                              "8% decrease in citizen approval rate for the president", \
                              "100 point decrease in political power"]


    n1 = randint(0, len(positive_policy_effect) - 1)
    choice1 = positive_policy_effect[n1]
    n2 = randint(0, len(negative_policy_effect) - 1)
    choice2 = negative_policy_effect[n2]
    choice3 = positive_policy_effect[n1]
    while (choice3 == choice1):
        n1 = randint(0, len(positive_policy_effect) - 1)
        choice3 = positive_policy_effect[n1]
    choice4 = negative_policy_effect[n2]
    while (choice4 == choice2):
        n2 = randint(0, len(negative_policy_effect) - 1)
        choice4 = negative_policy_effect[n2]

    for i in range(len(media_companies)):
        print(media_companies[i] + ": The president has made " + choice_policy + " reform, ", end="")

        if (media_companies[i] == "Cable News Network (CNN)"):

            if (choice_policy == "immigration forward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                print("the people have been supportive of it as shown by a " + choice1)

            elif (choice_policy == "immigration backward" and \
                  (choice_faction == "liberal" or choice_faction == "socialist")):
                print("the people have been against of it as shown by a " + choice2)

            elif (choice_policy == "immigration forward" and \
                  (choice_faction == "conservative" or choice_faction == "populist")):
                print("though in the short run the president and the country needs to make sacrifice," \
                      + " we believe that its benefits will be greater in the long run.")

            elif (choice_policy == "immigration backward" and \
                  (choice_faction == "conservative" or choice_faction == "populist")):
                print("though in the short run the president and the country can benefit from this reform, " \
                      + "we believe in the long run it can lead to serious problems in the country.")

        elif (media_companies[i] == "Fox Broadcasting Company (FOX)"):
            if (choice_policy == "immigration forward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                print("though in the short run the president and the country can benefit from this reform, " \
                      + "we believe in the long run it can lead to serious problems in the country.")

            elif (choice_policy == "immigration backward" and \
                  (choice_faction == "liberal" or choice_faction == "socialist")):
                print("though in the short run the president and the country needs to make sacrifice," \
                      + " we believe that its benefits will be greater in the long run.")

            elif (choice_policy == "immigration forward" and \
                  (choice_faction == "conservative" or choice_faction == "populist")):
                print("the people have been against of it as shown by a " + choice2)

            elif (choice_policy == "immigration backward" and \
                  (choice_faction == "conservative" or choice_faction == "populist")):
                print("the people have been supportive of it as shown by a " + choice1)

        elif (media_companies[i] == "Microsoft and NBC (MSNBC)"):
            if (choice_policy == "immigration forward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                print("the people have been supportive of it as shown by a " + choice3)

            elif (choice_policy == "immigration backward" and \
                  (choice_faction == "liberal" or choice_faction == "socialist")):
                print("the people have been against of it as shown by a " + choice4)

            elif (choice_policy == "immigration forward" and \
                  (choice_faction == "conservative" or choice_faction == "populist")):
                print("the people have been against of it as shown by a " + choice4)

            elif (choice_policy == "immigration backward" and \
                  (choice_faction == "conservative" or choice_faction == "populist")):
                print("the people have been supportive of it as shown by a " + choice3)

        if (choice_policy == "money forward"):
            print("though more budgets are used, the current conditions of both the country and the " \
                  + "presidents become better.")

        elif (choice_policy == "money backward"):
            print("though the current conditions of both the country and the presidents become worse, " \
                  + "more budgets can be saved for future use.")
# set operator
class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <INITIAL_STATE>
# initial variables
immigration_continent = ['NA', 'EU', 'OC']
emigration_continent = ['SA', 'LA', 'ME', 'AF', 'EA', 'EER', 'CA']
faction = ["socialist", "liberal", "conservative", "populist", "centrist"]
policy = {"immigration forward": "Provide work place for illegal immigrants", "immigration backward": "Make a wall", "money forward": "", "money backward": ""}
money_use = {"invest in employment centers": 20, "invest in public transportation": 20, "invest in tighter border enforcement": 20, "send foreign aid": 20}
year = 2017.5
Legal_immi = 47000000
Illegal_immi = 11200000
media_companies = ["Cable News Network (CNN)", "Fox Broadcasting Company (FOX)", "Microsoft and NBC (MSNBC)"]


# Faction Information    *For = Forward
Socialist = {"Social_For": "100", "Political_For": [50, 60, 100], "Immigrant_For": "100"}
Liberal = {"Social_For": "0", "Political_For": "100", "Immigrant_For": "100"}
Centrist = {"Social_For": "50", "Political_For": "50", "Immigrant_For": "50"}
Conservative = {"Social_For": [0, 20, 100], "Political_For": "0", "Immigrant_For": "0"}
Populist = {"Social_For": "50", "Political_For": "0", "Immigrant_For": "0"}

country = 'United States of America'
choice_faction = choice(faction)


# initialize the initial state
INITIAL_STATE = State()
# </INITIAL_STATE>

# <OPERATORS>

phi0 = Operator("Make a forward immigration policy",
                lambda s: s.can_make("immigration forward"),
                lambda s: s.make("immigration forward"))

phi1 = Operator("Make a backward immigration policy",
                lambda s: s.can_make("immigration backward"),
                lambda s: s.make("immigration backward"))

phi2 = Operator("Make a forward money policy",
                lambda s: s.can_make("money forward"),
                lambda s: s.make("money forward"))

phi3 = Operator("Make a backward money policy",
                lambda s: s.can_make("money backward"),
                lambda s: s.make("money backward"))

'''
phi4 = Operator("Print the forward immigration policy content",
                lambda s: True,
                lambda s: s.print_policy("immigration forward"))

phi5 = Operator("Print the backward immigration policy content",
                lambda s: True,
                lambda s: s.print_policy("immigration backward"))
'''

phi4 = Operator("Use political point(pp) to increase the government support rate for forward immigration"
                + " policy(50 pp equals 5 percentage increase in government support rate)",
                lambda s: True,
                lambda s: s.increase_support("immigration forward"))

phi5 = Operator("Use political point(pp) to increase the government support rate for backward immigration"
                + " policy(50 pp equals 5 percentage increase in government support rate)",
                lambda s: True,
                lambda s: s.increase_support("immigration backward"))

phi6 = Operator("Use political point(pp) to increase the government support rate for forward money"
                + " policy(50 pp equals 5 percentage increase in government support rate)",
                lambda s: True,
                lambda s: s.increase_support("money forward"))

phi7 = Operator("Use political point(pp) to increase the government support rate for backward money"
                + " policy(50 pp equals 5 percentage increase in government support rate)",
                lambda s: True,
                lambda s: s.increase_support("money backward"))


OPERATORS = [phi0, phi1, phi2, phi3, phi4, phi5, phi6, phi7]
# </OPERATORS>


# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s, has_election(), year)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

# <STATE_VIS>

# </STATE_VIS>
