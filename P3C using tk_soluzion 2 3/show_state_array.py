'''show_state_array.py
This Python module provides the means to use Tk graphics to display a
state visualization that consists of a 2D array of colored boxes, and
possibly some textual labels on them.

It is meant to be used together with the Tk_SOLUZION_Client.py program,
and an appropriately structured problem formulation file and visualization
file such as Missionaries.py and Missionaries_Array_VIS_FOR_TK.py



Version of Aug. 29, 2018. Prints fewer diagnostics than the version of
 Aug. 6, 2017.
S. Tanimoto

'''
import tkinter as tk

import time

from random import *

import sys


root = None
STATE_WINDOW = None
img = None

ns = 250 * 0.52 + 430 * 0.48
gs = 250*0.6+430*0.4
ca = 250*0.55+430*0.45
# graph data
graph1 = [[40, 340]]
graph2 = [[310, ns]]
graph3 = [[580, 340]]
graph4 = [[850, gs]]
graph5 = [[1120, ca]]

class state_array:

    def __init__(self):
        pass

    def show(self, text, year, Legal_immi, Illegal_immi):
        STATE_WINDOW.canvas.delete("points")
        STATE_WINDOW.canvas.create_text(165, 230, text=str(round(text[0], 4))+"pp", font=("Courier New", 25), tag="points", fill="white")
        STATE_WINDOW.canvas.create_text(435, 230, text=str(round(text[1], 4))+"%", font=("Courier New", 25), tag="points", fill="white")
        STATE_WINDOW.canvas.create_text(705, 230, text=str(round(text[3], 4))+"$", font=("Courier New", 25), tag="points", fill="white")
        STATE_WINDOW.canvas.create_text(970, 230, text=str(round(text[2], 4))+"%", font=("Courier New", 25), tag="points", fill="white")
        STATE_WINDOW.canvas.create_text(1250, 230, text=str(round(text[4], 4))+"%", font=("Courier New", 25), tag="points", fill="white")

        graph1.append([((year - 2018) / 15) * 290 + (1 - (year - 2018) / 15) * 40, (text[0] / 2000) * 250 + (1 - text[0] / 2000) * 430])
        graph2.append([((year - 2018) / 15) * 560 + (1 - (year - 2018) / 15) * 310, (text[1] / 100) * 250 + (1 - text[1] / 100) * 430])
        graph3.append([((year - 2018) / 15) * 830 + (1 - (year - 2018) / 15) * 580, (text[3] / 200) * 250 + (1 - text[3] / 200) * 430])
        graph4.append([((year - 2018) / 15) * 1100 + (1 - (year - 2018) / 15) * 850, (text[2] / 100) * 250 + (1 - text[2] / 100) * 430])
        graph5.append([((year - 2018) / 15) * 1370 + (1 - (year - 2018) / 15) * 1120, (text[4] / 100) * 250 + (1 - text[4] / 100) * 430])


        for i in [-1,0,1]:
            STATE_WINDOW.canvas.create_line(graph1[-2][0], graph1[-2][1]+i, graph1[-1][0], graph1[-1][1]+i, fill='#ff7f50')
            STATE_WINDOW.canvas.create_line(graph2[-2][0], graph2[-2][1]+i, graph2[-1][0], graph2[-1][1]+i, fill='#c9d744')
            STATE_WINDOW.canvas.create_line(graph3[-2][0], graph3[-2][1]+i, graph3[-1][0], graph3[-1][1]+i, fill='#65ace4')
            STATE_WINDOW.canvas.create_line(graph4[-2][0], graph4[-2][1]+i, graph4[-1][0], graph4[-1][1]+i, fill='#dbbc86')
            STATE_WINDOW.canvas.create_line(graph5[-2][0], graph5[-2][1]+i, graph5[-1][0], graph5[-1][1]+i, fill='#ae8dbc')

        STATE_WINDOW.canvas.create_text(320, 500, text='The number of Legal Immigrants: ' + str("{:,d}".format(Legal_immi)),font=("Courier New", 25), tag="points", fill='white')
        STATE_WINDOW.canvas.create_text(355, 560, text='The number of Illegal Immigrants: ' + str("{:,d}".format(Illegal_immi)), font=("Courier New", 25), tag="points", fill='white')

        if Legal_immi-47000000 >= 0:
            immi_color = '#65ace4'
            immi_updown = "( +"+"{:,d}".format(Legal_immi-47000000)+" )"
        else:
            immi_color = '#ff7f50'
            immi_updown = "( -" + "{:,d}".format(47000000-Legal_immi) + " )"

        if Illegal_immi-11200000 >= 0:
            immi1_color = '#65ace4'
            immi1_updown = "( +" + "{:,d}".format(Illegal_immi - 11200000) + " )"
        else:
            immi1_color = '#ff7f50'
            immi1_updown = "( -" + "{:,d}".format(11200000 - Illegal_immi) + " )"

        STATE_WINDOW.canvas.create_text(750, 500, text=immi_updown, font=("Tahoma", 25), tag="points", fill=immi_color)

        STATE_WINDOW.canvas.create_text(790, 560, text=immi1_updown, font=("Tahoma", 25), tag="points", fill=immi1_color)

    def progress_bar(self, year=2018):
        STATE_WINDOW.canvas.delete("year_indi")
        year_per = (year-2018)/15*750
        STATE_WINDOW.canvas.create_polygon([300+year_per, 840, 294+year_per, 855, 306+year_per, 855], tag='year_indi', fill='#c9d744')
        STATE_WINDOW.canvas.create_oval(290+year_per, 851, 310+year_per, 871, tag='year_indi', fill='#c9d744', outline='#c9d744', width=2)
        STATE_WINDOW.canvas.create_rectangle(300, 830, 300+year_per, 840, fill='#c9d744', outline='')


class state_display(tk.Frame):
    def __init__(self, parent, width=300, height=300, x=0, y=0, bg='white'):
        super(state_display, self).__init__(parent)
        self.width=width; self.height=height
        self.canvas = tk.Canvas(parent, bg=bg, width=self.width, height=self.height)
        self.canvas.place(x=x, y=y)
        self.canvas.pack()
        # self.label = tk.Label(self, text="version=''")
        # self.label.pack(padx=20, pady=20)


def initialize_tk(width=300, height=300, title='State Display Window', country='', cho_fac=''):
    global root
    global STATE_WINDOW
    root = tk.Tk()
    root.title(title)
    the_display = state_display(root, width=width, height=height, bg='#424242')
    the_display.pack(fill="both", expand=True)
    STATE_WINDOW = the_display

    global img, img_cnn, img_fox, img_msnbc, img_flag
    img = tk.PhotoImage(file="./white-house.gif")
    img_cnn = tk.PhotoImage(file="./CNN-logo.gif")
    img_fox = tk.PhotoImage(file="./FOX-logo.gif")
    img_msnbc = tk.PhotoImage(file="./MSNBC-logo.gif")
    img_flag = tk.PhotoImage(file="./US_flag.gif")

    STATE_WINDOW.canvas.create_image(95, 50, image=img_flag)
            
    STATE_WINDOW.canvas.create_text(320, 30, text="your faction: ", font=("Times New Roman", 30), fill="white")
    STATE_WINDOW.canvas.create_text(310, 98, text="Requirements", font=("Times New Roman", 26), fill='white')
    STATE_WINDOW.canvas.create_text(690, 30, text="election 1", font=("Times New Roman", 30), fill='white')
    STATE_WINDOW.canvas.create_text(950, 30, text="election 2", font=("Times New Roman", 30), fill='white')
    STATE_WINDOW.canvas.create_text(1210, 30, text="election 3", font=("Times New Roman", 30), fill='white')
    STATE_WINDOW.canvas.create_line(230, 58, 1300, 58, fill='orange')
    STATE_WINDOW.canvas.create_line(560, 13, 560, 131, fill='orange')
    STATE_WINDOW.canvas.create_line(820, 13, 820, 131, fill='orange')
    STATE_WINDOW.canvas.create_line(1080, 13, 1080, 131, fill='orange')
    STATE_WINDOW.canvas.create_line(400, 98, 1300, 98, fill='orange', dash=(3, 4))
    STATE_WINDOW.canvas.create_line(400, 58, 400, 131, fill='orange', dash=(3, 4))
    STATE_WINDOW.canvas.create_text(475, 78, text="Legal Immi", font=("Times New Roman", 23), fill="white")
    STATE_WINDOW.canvas.create_text(475, 116, text="Illegal Immi", font=("Times New Roman", 23), fill="white")
            

    if cho_fac == 'liberal' or cho_fac == 'socialist':
        Req_le_immi = ["+5,000,000", "+9,000,000", "+14,000,000"]
        Req_ille_immi = ["none", "none", "none"]
    elif cho_fac == 'conservative' or cho_fac == 'populist':
        Req_le_immi = ["-5,000,000", "-9,000,000", "-14,000,000"]
        Req_ille_immi = ["-2,000,000", "-4,000,000", "-6,000,000"]
    elif cho_fac == 'centrist':
        Req_le_immi = ["+2,000,000", "+4,000,000", "+6,000,000"]
        Req_ille_immi = ["-1,500,000", "-2,500,000", "-3,000,000"]
                                    
    for i in range(3):
        STATE_WINDOW.canvas.create_text(690+260*i, 78, text=Req_le_immi[i], font=("Times New Roman", 25), fill="white")
        STATE_WINDOW.canvas.create_text(690+260*i, 117, text=Req_ille_immi[i], font=("Times New Roman", 25), fill="white")
                                            
    if cho_fac=='conservative':
        fac_place = 480
    else:
        fac_place = 460
                                                            
    STATE_WINDOW.canvas.create_text(fac_place, 30, text=cho_fac.capitalize(), font=("Marker Felt", 32), fill="#ff6666")



    STATE_WINDOW.canvas.create_text(165, 170, font=("Courier New", 20), text='pp(political power)', fill='white')
    STATE_WINDOW.canvas.create_text(435, 170, font=("Courier New", 20), text='national stability', fill='white')
    STATE_WINDOW.canvas.create_text(705, 170, font=("Courier New", 20), text='budget', fill='white')
    STATE_WINDOW.canvas.create_text(975, 170, font=("Courier New", 20), text='government support', fill='white')
    STATE_WINDOW.canvas.create_text(1245, 170, font=("Courier New", 20), text='citizen approval', fill='white')
    STATE_WINDOW.canvas.create_rectangle(40, 190, 290, 200, fill='#ff7f50', outline='')
    STATE_WINDOW.canvas.create_rectangle(310, 190, 560, 200, fill='#c9d744', outline='')
    STATE_WINDOW.canvas.create_rectangle(580, 190, 830, 200, fill='#65ace4', outline='')
    STATE_WINDOW.canvas.create_rectangle(850, 190, 1100, 200, fill='#dbbc86', outline='')
    STATE_WINDOW.canvas.create_rectangle(1120, 190, 1370, 200, fill='#ae8dbc', outline='')

    STATE_WINDOW.canvas.create_line(40, 250, 40, 430, fill='white')
    STATE_WINDOW.canvas.create_line(40, 430, 290, 430, fill='white')
    STATE_WINDOW.canvas.create_oval(36, 336, 44, 344, fill='#ff7f50', outline='')


    STATE_WINDOW.canvas.create_line(310, 250, 310, 430, fill='white')
    STATE_WINDOW.canvas.create_line(310, 430, 560, 430, fill='white')
    STATE_WINDOW.canvas.create_oval(306, ns-4, 314, ns+4, fill='#c9d744', outline='')
        
    STATE_WINDOW.canvas.create_line(580, 250, 580, 430, fill='white')
    STATE_WINDOW.canvas.create_line(580, 430, 830, 430, fill='white')
    STATE_WINDOW.canvas.create_oval(576, 336, 584, 344, fill='#65ace4', outline='')
            
            
    STATE_WINDOW.canvas.create_line(850, 250, 850, 430, fill='white')
    STATE_WINDOW.canvas.create_line(850, 430, 1100, 430, fill='white')
    STATE_WINDOW.canvas.create_oval(846, gs-4, 854, gs+4, fill='#dbbc86', outline='')
                
                
    STATE_WINDOW.canvas.create_line(1120, 250, 1120, 430, fill='white')
    STATE_WINDOW.canvas.create_line(1120, 430, 1370, 430, fill='white')
    STATE_WINDOW.canvas.create_oval(1116, ca-4, 1124, ca+4, fill='#ae8dbc', outline='')
                    
                        
    STATE_WINDOW.canvas.create_rectangle(300, 830, 1050, 840, fill='#dcdcdc', outline='')
                            
    STATE_WINDOW.canvas.create_rectangle(0, 450, 1400, 454, fill='white', outline='')


    # Forward Immigration policies
    STATE_WINDOW.canvas.create_text(330, 630, font=("Courier New", 18), text='Forward Immigration policies', fill='#add8e6')
    STATE_WINDOW.canvas.create_text(350, 680, font=("Courier New", 17), text='- Increase annual capability on immigration', fill='white')
    STATE_WINDOW.canvas.create_text(295, 710, font=("Courier New", 17), text='- Permit refugees to enter', fill='white')
    STATE_WINDOW.canvas.create_text(305, 740, font=("Courier New", 17), text='- Increase the number of visas', fill='white')
    STATE_WINDOW.canvas.create_text(320, 770, font=("Courier New", 17), text='- Lower the quota for skilled labors', fill='white')

    STATE_WINDOW.canvas.create_line(100, 630, 160, 630, fill='white')
    STATE_WINDOW.canvas.create_line(100, 630, 100, 800, fill='white')
    STATE_WINDOW.canvas.create_arc(100, 630, 120, 650, start=90, extent=90, outline='white', style='arc')
    STATE_WINDOW.canvas.create_arc(100, 630, 140, 670, start=90, extent=90, outline='white', style='arc')
    STATE_WINDOW.canvas.create_line(100, 800, 93, 790, fill='white')
    STATE_WINDOW.canvas.create_line(107, 790, 100, 780, fill='white')
    STATE_WINDOW.canvas.create_line(93, 790, 100, 780, fill='white')
    STATE_WINDOW.canvas.create_line(100, 800, 107, 790, fill='white')

    STATE_WINDOW.canvas.create_text(1030, 630, font=("Courier New", 18), text='Backward Immigration policies', fill='#ffd700')
    STATE_WINDOW.canvas.create_text(1080, 680, font=("Courier New", 17), text='- Prohibit contracted laborers from entering', fill='white')
    STATE_WINDOW.canvas.create_text(970, 710, font=("Courier New", 17), text='- Deport illegal immigrants', fill='white')
    STATE_WINDOW.canvas.create_text(1000, 740, font=("Courier New", 17), text='- Increase border enforcement', fill='white')
    STATE_WINDOW.canvas.create_text(1100, 770, font=("Courier New", 17), text='- Restrict immigration from all emigrant continents', fill='white')

    STATE_WINDOW.canvas.create_line(800, 630, 860, 630, fill='white')
    STATE_WINDOW.canvas.create_line(800, 630, 800, 790, fill='white')
    STATE_WINDOW.canvas.create_arc(800, 630, 820, 650, start=90, extent=90, outline='white', style='arc')
    STATE_WINDOW.canvas.create_arc(800, 630, 840, 670, start=90, extent=90, outline='white', style='arc')
    STATE_WINDOW.canvas.create_line(794, 790, 806, 790, fill='white')
    STATE_WINDOW.canvas.create_line(794, 790, 794, 784, fill='white')
    STATE_WINDOW.canvas.create_line(794, 784, 806, 784, fill='white')
    STATE_WINDOW.canvas.create_line(806, 784, 806, 790, fill='white')

    STATE_WINDOW.canvas.create_line(550, 830, 550, 870, fill='white', dash=(3, 4))
    STATE_WINDOW.canvas.create_line(800, 830, 800, 870, fill='white', dash=(3, 4))
    STATE_WINDOW.canvas.create_line(1050, 830, 1050, 870, fill='white', dash=(3, 4))

    STATE_WINDOW.canvas.create_text(550, 880, text='1st election', fill='white')
    STATE_WINDOW.canvas.create_text(800, 880, text='2nd election', fill='white')
    STATE_WINDOW.canvas.create_text(1050, 880, text='3rd election', fill='white')


    # media
    STATE_WINDOW.canvas.create_rectangle(1400, 0, 1700, 295, fill='#222222', outline='')
    STATE_WINDOW.canvas.create_image(1459, 55, image=img_cnn)
    STATE_WINDOW.canvas.create_polygon(1400, 103, 1400, 115, 1386, 103, fill='#800000', outline='')

    STATE_WINDOW.canvas.create_rectangle(1402, 305, 1702, 595, fill='#333333', outline='')
    STATE_WINDOW.canvas.create_image(1461, 355, image=img_fox)
    STATE_WINDOW.canvas.create_polygon(1402, 398, 1402, 409, 1388, 398, fill='#00558f', outline='')

    STATE_WINDOW.canvas.create_rectangle(1400, 605, 1700, 895, fill='#222222', outline='')
    STATE_WINDOW.canvas.create_image(1459, 655, image=img_msnbc)
    STATE_WINDOW.canvas.create_polygon(1400, 696, 1400, 707, 1387, 696, fill='#c0c0c0', outline='')


    print("VIS initialization finished")


def make_modalW(current_state=[], year=2018, cho_fac=''):
    STATE_WINDOW.canvas.create_polygon([270, 150, 850, 150, 550, 750, 270, 750], fill='#000099', tag='modal_contents')
    STATE_WINDOW.canvas.create_polygon([850, 150, 1130, 150, 1130, 750, 550, 750], fill='#ea0032', tag='modal_contents')
    STATE_WINDOW.canvas.create_rectangle(300, 180, 1100, 720, fill='white', outline='', tag='modal_contents')

    STATE_WINDOW.canvas.create_rectangle(400, 295, 1000, 305, fill='black', outline='', tag='modal_contents')
    STATE_WINDOW.canvas.create_rectangle(990, 305, 1000, 595, fill='black', outline='', tag='modal_contents')
    STATE_WINDOW.canvas.create_rectangle(400, 595, 1000, 615, fill='black', outline='', tag='modal_contents')
    STATE_WINDOW.canvas.create_rectangle(400, 305, 410, 595, fill='black', outline='', tag='modal_contents')
    STATE_WINDOW.canvas.create_polygon([600, 615, 608, 615, 593, 640, 585, 640], fill='black', tag='modal_contents')
    STATE_WINDOW.canvas.create_polygon([792, 615, 800, 615, 815, 640, 807, 640], fill='black', tag='modal_contents')
    STATE_WINDOW.canvas.create_polygon([593, 640, 595, 635, 805, 635, 807, 640], fill='black', tag='modal_contents')
    STATE_WINDOW.canvas.create_rectangle(410, 305, 450, 595, fill='#222222', outline='', tag='modal_contents')
    STATE_WINDOW.canvas.create_rectangle(950, 305, 990, 595, fill='#222222', outline='', tag='modal_contents')

    STATE_WINDOW.canvas.create_image(700, 450, image=img, tag='modal_contents')


    STATE_WINDOW.canvas.create_rectangle(460, 320, 660, 580, fill='#f5fffa', outline='', tag='modal_contents')
    STATE_WINDOW.canvas.create_text(560, 360, font=("Courier New", 28), text=str(int(year)), tag='modal_contents')
    STATE_WINDOW.canvas.create_text(560, 390, font=("Courier New", 18), text='year election', tag='modal_contents')


    if current_state[4] >= 50:
        descri = '   Mr.You in '+cho_fac+' party has been elected as a president of America'
    else:
        if cho_fac=='conservative' or cho_fac=='populist':
            oppse_fac = 'liberal'
        else:
            oppse_fac = 'conservative'
        descri = '   Mr.A in ' + oppse_fac + ' party has been elected as a president of America'

    STATE_WINDOW.canvas.create_text(565, 480, font=("Courier New", 16), width=160, text=descri, tag='modal_contents')


    rate_arc = current_state[4] * 3.6
    rest = uniform((100-current_state[4]-4), (100-current_state[4]-1))
    rate_arc1 = rest * 3.6
    rate_arc2 = (100-current_state[4]-rest) * 3.6

    STATE_WINDOW.canvas.create_arc(720, 361, 904, 545, fill='white', start=90+(rate_arc1+rate_arc2), extent=rate_arc, outline='#00acff', width=15, style='arc', tag='modal_contents')
    STATE_WINDOW.canvas.create_oval(722, 363, 902, 543, fill='white', outline='', tag='modal_contents')

    STATE_WINDOW.canvas.create_arc(722, 363, 902, 543, start=90+rate_arc2, extent=rate_arc1, outline='#a4ca68', width=7, style='arc', tag='modal_contents')
    STATE_WINDOW.canvas.create_arc(722, 363, 902, 543, start=90, extent=rate_arc2, outline='yellow', width=7, style='arc', tag='modal_contents')
    STATE_WINDOW.canvas.create_text(812, 453, font=("Courier New", 30), text=str(round(current_state[4], 4))+'%', tag='modal_contents')
    STATE_WINDOW.canvas.create_text(812, 475, font=("Courier New", 15), text='citizen approval', tag='modal_contents')
    STATE_WINDOW.canvas.create_text(812, 491, font=("Courier New", 15), text='rate', tag='modal_contents')

    time.sleep(2)
    STATE_WINDOW.canvas.create_rectangle(500,665,900,705, fill='white', outline='black', tag='modal_contents')
    STATE_WINDOW.canvas.create_text(700, 685, font=("Courier New", 23), text='enter q in command to close', tag='modal_contents')

    ch = input("quit the election screen[q]: ")
    if ch == 'q':
        STATE_WINDOW.canvas.delete("modal_contents")
        if current_state[4] >= 50:
            return True
        else:
            return False

def close_window(w_l='', reason=''):
    STATE_WINDOW.canvas.create_rectangle(350, 320, 1350, 580, fill='#333333', outline='')
    STATE_WINDOW.canvas.create_text(850, 420, text="You have "+w_l+" this game", font=("Courier New", 70), fill='yellow')
    STATE_WINDOW.canvas.create_text(850, 510, text=reason, font=("Courier New", 26), width='800', fill='white')
    if reason=="your administration is too unstable" or reason=="the number of illegal immigrants has exceeded that of legal immigrants":
        subprocess.call(["afplay", "Debbie-Downer-wah-wah-wah.wav"])
    elif reason=="the number of illegal immigrants has exceeded that of legal immigrants":
        subprocess.call(["afplay", "Debbie-Downer-wah-wah-wah.wav"])
    elif reason=="You did not satisfy the requirement regarding the number of legal and illegal immigrants":
        subprocess.call(["afplay", "The-Price-Is-Wrong.wav"])
    elif reason=="very good":
        subprocess.call(["afplay", "applause_y.wav"])
        subprocess.call(["afplay", "bush_god_bless.wav"])
    else:
        subprocess.call(["afplay", "pacman_death.wav"])
    
    
    # time.sleep(5)
    # root.withdraw()
    sys.exit()



media_companies = ["Cable News Network (CNN)", "Fox Broadcasting Company (FOX)", "Microsoft and NBC (MSNBC)"]

positive_policy_effect = ["around 5% increase in stability", \
                          "around 4% increase in citizen approval rate for the president", \
                          "around 100 point increase in political power"]
negative_policy_effect = ["around 5% decrease in stability", \
                          "around 8% decrease in citizen approval rate for the president", \
                          "around 100 point decrease in political power"]

def show_media(choice_policy,choice_faction):
    # media report on the policies
    STATE_WINDOW.canvas.delete("media_info")
    
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
        # print(media_companies[i] + ": The president has made " + choice_policy + " reform, ", end="")

        if (media_companies[i] == "Cable News Network (CNN)"):
                                              
            if (choice_policy == "immigration forward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                STATE_WINDOW.canvas.create_text(1540, 200, font=("Courier New", 18), width=250, text=" The people have been supportive of it as shown by an " + choice1, fill='white', tag='media_info')
                                                      
            elif (choice_policy == "immigration backward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                STATE_WINDOW.canvas.create_text(1540, 200, font=("Courier New", 18), width=250, text=" The people have been against of it as shown by an " + choice2, fill='white', tag='media_info')
                                                              
            elif (choice_policy == "immigration forward" and \
                    (choice_faction == "conservative" or choice_faction == "populist")):
                STATE_WINDOW.canvas.create_text(1540, 200, font=("Courier New", 18), width=250, text=" Though in the short run the president and the country needs to make sacrifice," \
                    + " we believe that its benefits will be greater in the long run.", fill='white', tag='media_info')
                                                                      
            elif (choice_policy == "immigration backward" and \
                    (choice_faction == "conservative" or choice_faction == "populist")):
                STATE_WINDOW.canvas.create_text(1540, 200, font=("Courier New", 18), width=250, text=" Though in the short run the president and the country can benefit from this reform, " \
                    + "we believe in the long run it can lead to serious problems in the country.", fill='white', tag='media_info')
                                                                              
        elif (media_companies[i] == "Fox Broadcasting Company (FOX)"):
            if (choice_policy == "immigration forward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                STATE_WINDOW.canvas.create_text(1540, 500, font=("Courier New", 18), width=250, text=" Though in the short run the president and the country can benefit from this reform, " \
                    + "we believe in the long run it can lead to serious problems in the country.", fill='white', tag='media_info')
                                                                                          
            elif (choice_policy == "immigration backward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                STATE_WINDOW.canvas.create_text(1540, 500, font=("Courier New", 18), width=250, text=" Though in the short run the president and the country needs to make sacrifice," \
                    + " we believe that its benefits will be greater in the long run.", fill='white', tag='media_info')
                                                                                                  
            elif (choice_policy == "immigration forward" and \
                    (choice_faction == "conservative" or choice_faction == "populist")):
                STATE_WINDOW.canvas.create_text(1540, 500, font=("Courier New", 18), width=250, text=" The people have been against of it as shown by an " + choice2, fill='white', tag='media_info')
                                                                                                          
            elif (choice_policy == "immigration backward" and \
                    (choice_faction == "conservative" or choice_faction == "populist")):
                STATE_WINDOW.canvas.create_text(1540, 500, font=("Courier New", 18), width=250, text=" The people have been supportive of it as shown by an " + choice1, fill='white', tag='media_info')

        elif (media_companies[i] == "Microsoft and NBC (MSNBC)"):
            if (choice_policy == "immigration forward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                STATE_WINDOW.canvas.create_text(1540, 800, font=("Courier New", 18), width=250, text=" The people have been supportive of it as shown by an " + choice3, fill='white', tag='media_info')
                                                                                                                              
            elif (choice_policy == "immigration backward" and \
                    (choice_faction == "liberal" or choice_faction == "socialist")):
                STATE_WINDOW.canvas.create_text(1540, 800, font=("Courier New", 18), width=250, text=" The people have been against of it as shown by an " + choice4, fill='white', tag='media_info')
                                                                                                                                      
            elif (choice_policy == "immigration forward" and \
                    (choice_faction == "conservative" or choice_faction == "populist")):
                STATE_WINDOW.canvas.create_text(1540, 800, font=("Courier New", 18), width=250, text=" The people have been against of it as shown by an " + choice4, fill='white', tag='media_info')
                                                                                                                                              
            elif (choice_policy == "immigration backward" and \
                    (choice_faction == "conservative" or choice_faction == "populist")):
                STATE_WINDOW.canvas.create_text(1540, 800, font=("Courier New", 18), width=250, text=" The people have been supportive of it as shown by an " + choice3, fill='white', tag='media_info')
                                                                                                                                                      
        '''if (choice_policy == "money forward"):
                                                
            print("though more budgets are used, the current conditions of both the country and the " \
                  + "presidents become better.")
                                                                                                                                                              
        if (choice_policy == "money backward"):
            print("though the current conditions of both the country and the presidents become worse, " \
                  + "more budgets can be saved for future use.")'''

