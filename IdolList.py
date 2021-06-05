# Python Module #
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import sqlite3

version = "[3.0] 21/06/05"
conn1 = sqlite3.connect('mltdkei_idoldata.sqlite')
cur1 = conn1.cursor()

def version_check():
    return version

def main_idollist(iconext):
    try:
        infofile = open('mltdkei_info.txt', 'r', encoding='utf-8')
        infodata = infofile.read().split('\n')
        infofile.close()
    except:
        msgbox.showinfo('Error', 'Info File is damaged or not updated.\nPlease check your file or update DB first.')
        return

    uil_root = Toplevel()
    uil_root.title("Idol List Editor for MLTD Deck Analyzer")
    uil_root.geometry("+60+25")
    uil_root.resizable(False, False)

    ssr_princess, ssr_fairy, ssr_angel = list(), list(), list()
    ssr_1st, ssr_2nd, ssr_3rd = list(), list(), list()
    sr_princess, sr_fairy, sr_angel, sr_ex = list(), list(), list(), list()
    r_princess, r_fairy, r_angel, n_all = list(), list(), list(), list()
    anniversary = ["BRAND NEW PERFORMANCE", "UNI-ONAIR", "CHALLENGE FOR GLOW-RY DAYS"]
    pbar_varp = IntVar()

    listtem = cur1.execute('''select idnumber, rare, name, type from IdolDB''').fetchall()
    for quartet in listtem:
        if quartet[1] == "SSR+":
            if anniversary[0] in quartet[2]: ssr_1st.append(int(quartet[0]))
            elif anniversary[1] in quartet[2]: ssr_2nd.append(int(quartet[0]))
            elif anniversary[2] in quartet[2]: ssr_3rd.append(int(quartet[0]))
            elif quartet[3] == 1: ssr_princess.append(int(quartet[0]))
            elif quartet[3] == 2: ssr_fairy.append(int(quartet[0]))
            elif quartet[3] == 3: ssr_angel.append(int(quartet[0]))
        elif quartet[1] == "SR+":
            if quartet[3] == 1: sr_princess.append(int(quartet[0]))
            elif quartet[3] == 2: sr_fairy.append(int(quartet[0]))
            elif quartet[3] == 3: sr_angel.append(int(quartet[0]))
            elif quartet[3] == 4: sr_ex.append(int(quartet[0]))
        elif quartet[1] == "R+":
            if quartet[3] == 1: r_princess.append(int(quartet[0]))
            elif quartet[3] == 2: r_fairy.append(int(quartet[0]))
            elif quartet[3] == 3: r_angel.append(int(quartet[0]))
        elif quartet[1] == "N+":
            n_all.append(int(quartet[0]))

    uil_set_container = Frame(uil_root, width=1015, height=75, borderwidth=2, relief="groove")
    uil_set_container.grid(row=0, column=0)
    uil_container = Frame(uil_root)
    uil_container.grid(row=1, column=0)

    def buttoncmd_save():
        writedata = "\n".join(infodata)
        infofile = open('mltdkei_info.txt', 'w', encoding='utf-8')
        infofile.write(writedata)
        infofile.close()
        msgbox.showinfo("Save Complete", "Save Complete")

    def print_gui(inputed_list):
        nonlocal uil_container
        button_write.config(state="disabled")
        uil_container.destroy()
        uil_container = Frame(uil_root)
        uil_canvas = Canvas(uil_container, width=995, height=505)
        scrollbar = Scrollbar(uil_container, command=uil_canvas.yview)
        scrollable_frame = Frame(uil_canvas)

        scrollable_frame.bind("<Configure>", lambda e: uil_canvas.configure(scrollregion=uil_canvas.bbox("all")))

        uil_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        uil_canvas.configure(yscrollcommand=scrollbar.set)

        uil_container.grid(row=1, column=0)
        uil_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        lb_protect = Label(uil_set_container, text="Now Loading...")
        lb_protect.grid(row=0, column=0, rowspan=2, columnspan=9, sticky=N+E+W+S)
        countout, lenin, countcol, countrow = 0, len(inputed_list), 0, 0
        lb_progressleft.config(text=countout)
        lb_progressright.config(text=lenin)
        pbar_varp.set(countout)
        pbr_progress.config(maximum=lenin)
        if inputed_list == ssr_princess: lb_opendeck.config(text="SSR-Pr")
        elif inputed_list == ssr_fairy: lb_opendeck.config(text="SSR-Fa")
        elif inputed_list == ssr_angel: lb_opendeck.config(text="SSR-An")
        elif inputed_list == ssr_1st: lb_opendeck.config(text="SSR-1st")
        elif inputed_list == ssr_2nd: lb_opendeck.config(text="SSR-2nd")
        elif inputed_list == ssr_3rd: lb_opendeck.config(text="SSR-3rd")
        elif inputed_list == sr_princess: lb_opendeck.config(text="SR-Pr")
        elif inputed_list == sr_fairy: lb_opendeck.config(text="SR-Fa")
        elif inputed_list == sr_angel: lb_opendeck.config(text="SR-An")
        elif inputed_list == sr_ex: lb_opendeck.config(text="SR-Ex")
        elif inputed_list == r_princess: lb_opendeck.config(text="R-Pr")
        elif inputed_list == r_fairy: lb_opendeck.config(text="R-Fa")
        elif inputed_list == r_angel: lb_opendeck.config(text="R-An")
        elif inputed_list == n_all: lb_opendeck.config(text="N-All")
        uil_root.update()

        def dataprint(inputed_data, r, c):
            def printdata(what):
                if what == "have": inputed_data[-3] = str(havevalues.index(cbxhave.get()))
                elif what == "rank": inputed_data[-2] = str(rankvalues.index(cbxrank.get()))
                elif what == "skill": inputed_data[-1] = str(skillvalues.index(cbxskill.get())+1)
                edited_data = ",".join(inputed_data)
                if idnumber < 1064: infodata[idnumber-1] = edited_data
                elif idnumber > 1065: infodata[idnumber-3] = edited_data

            inputed_data = inputed_data.split(',')
            image = cur1.execute('''select photocode from PhotoCodeDB
                where idnumber = %d''' % int(inputed_data[0])).fetchone()[0]
            idnumber = int(inputed_data[0])
            have, rank, skill = inputed_data[-3:]
            idolname = ",".join(inputed_data[2:inputed_data.index(have)])

            lb_loadid.config(text=idnumber)
            lb_loadname.config(text=idolname)
            uil_root.update()

            deckphoto = iconext(idnumber, image, 58)
            uil_photolabel = Label(scrollable_frame, image=deckphoto)
            uil_photolabel.image = deckphoto
            uil_photolabel.grid(row=r, column=c)

            cbxhave = ttk.Combobox(scrollable_frame, height=2, width=5, values=havevalues, state="readonly")
            cbxhave.grid(row=r+1, column=c)
            cbxhave.set(havevalues[int(have)])
            cbxhave.bind("<<ComboboxSelected>>", lambda unused_option: printdata("have"))

            cbxrank = ttk.Combobox(scrollable_frame, height=6, width=5, values=rankvalues, state="readonly")
            cbxrank.grid(row=r+2, column=c)
            cbxrank.set(rankvalues[int(rank)])
            cbxrank.bind("<<ComboboxSelected>>", lambda unused_option: printdata("rank"))

            cbxskill = ttk.Combobox(scrollable_frame, height=13, width=5, values=skillvalues, state="readonly")
            cbxskill.grid(row=r+3, column=c)
            cbxskill.set(skillvalues[int(skill)-1])
            cbxskill.bind("<<ComboboxSelected>>", lambda unused_option: printdata("skill"))

        for idnumber in inputed_list:
            if idnumber < 1064:
                try: data = infodata[idnumber-1]
                except IndexError: break
            elif idnumber > 1065:
                try: data = infodata[idnumber-3]
                except IndexError: break
            dataprint(data, countrow, countcol)
            countout = countout + 1
            lb_progressleft.config(text=countout)
            pbar_varp.set(countout)
            countcol = countcol + 1
            uil_root.update()
            if countcol == 16:
                countcol = 0
                countrow = countrow + 4

        def config_all():
            if len(inputed_list) == 0: return
            for idnumber in inputed_list:
                if idnumber < 1064:
                    try: data = infodata[idnumber-1]
                    except IndexError: break
                elif idnumber > 1065:
                    try: data = infodata[idnumber-3]
                    except IndexError: break
                data = data.split(",")
                data[-3] = str(havevalues.index(cbxhave_open.get()))
                data[-2] = str(rankvalues.index(cbxrank_open.get()))
                data[-1] = str(skillvalues.index(cbxskill_open.get())+1)
                edited_data = ",".join(data)
                if idnumber < 1064: infodata[idnumber-1] = edited_data
                elif idnumber > 1065: infodata[idnumber-3] = edited_data
            print_gui(inputed_list)

        lb_protect.destroy()
        button_write.config(command=config_all, state="normal")
        cbxhave_open.set(havevalues[0])
        cbxrank_open.set(rankvalues[0])
        cbxskill_open.set(skillvalues[0])

    button_save = Button(uil_set_container, text="Save", width=7, command=buttoncmd_save)
    button_save.grid(row=0, column=0, rowspan=2, sticky=N+S)

    button_ssrpr = Button(uil_set_container, text="SSR-Pr", width=7, command=lambda: print_gui(ssr_princess))
    button_ssrpr.grid(row=0, column=1)

    button_ssrfa = Button(uil_set_container, text="SSR-Fa", width=7, command=lambda: print_gui(ssr_fairy))
    button_ssrfa.grid(row=0, column=2)

    button_ssran = Button(uil_set_container, text="SSR-An", width=7, command=lambda: print_gui(ssr_angel))
    button_ssran.grid(row=0, column=3)

    button_ssr1st = Button(uil_set_container, text="SSR-1st", width=7, command=lambda: print_gui(ssr_1st))
    button_ssr1st.grid(row=0, column=4)

    button_ssr2nd = Button(uil_set_container, text="SSR-2nd", width=7, command=lambda: print_gui(ssr_2nd))
    button_ssr2nd.grid(row=0, column=5)

    button_ssr3rd = Button(uil_set_container, text="SSR-3rd", width=7, command=lambda: print_gui(ssr_3rd))
    button_ssr3rd.grid(row=0, column=6)

    button_comingsoon = Button(uil_set_container, text="Coming Soon")
    button_comingsoon.grid(row=0, column=7, columnspan=2, sticky=E+W)

    button_srpr = Button(uil_set_container, text="SR-Pr", width=7, command=lambda: print_gui(sr_princess))
    button_srpr.grid(row=1, column=1)

    button_srfa = Button(uil_set_container, text="SR-Fa", width=7, command=lambda: print_gui(sr_fairy))
    button_srfa.grid(row=1, column=2)

    button_sran = Button(uil_set_container, text="SR-An", width=7, command=lambda: print_gui(sr_angel))
    button_sran.grid(row=1, column=3)

    button_srex = Button(uil_set_container, text="SR-Ex", width=7, command=lambda: print_gui(sr_ex))
    button_srex.grid(row=1, column=4)

    button_rpr = Button(uil_set_container, text="R-Pr", width=7, command=lambda: print_gui(r_princess))
    button_rpr.grid(row=1, column=5)

    button_rfa = Button(uil_set_container, text="R-Fa", width=7, command=lambda: print_gui(r_fairy))
    button_rfa.grid(row=1, column=6)

    button_ran = Button(uil_set_container, text="R-An", width=7, command=lambda: print_gui(r_angel))
    button_ran.grid(row=1, column=7)

    button_nall = Button(uil_set_container, text="N-All", width=7, command=lambda: print_gui(n_all))
    button_nall.grid(row=1, column=8)

    uil_progress_container = Frame(uil_set_container, width=485, height=50)
    uil_progress_container.grid(row=0, column=9, rowspan=2)

    lb_nowloading = Label(uil_progress_container, text="Now Loading")
    lb_nowloading.place(x=0, y=0, width=80, height=25)

    lb_progress = Label(uil_progress_container, text="Progress")
    lb_progress.place(x=0, y=25, width=80, height=25)

    lb_loadid = Label(uil_progress_container, borderwidth=2, relief="groove", bg="white")
    lb_loadid.place(x=80, y=0, width=45, height=25)

    lb_loadname = Label(uil_progress_container, borderwidth=2, relief="groove", bg="white")
    lb_loadname.place(x=125, y=0, width=360, height=25)

    lb_progressleft = Label(uil_progress_container, borderwidth=2, relief="groove", bg="white")
    lb_progressleft.place(x=80, y=25, width=45, height=25)

    lb_progressmiddle = Label(uil_progress_container, text="/", borderwidth=2)
    lb_progressmiddle.place(x=125, y=25, width=10, height=25)

    lb_progressright = Label(uil_progress_container, borderwidth=2, relief="groove", bg="white")
    lb_progressright.place(x=135, y=25, width=45, height=25)

    pbr_progress = ttk.Progressbar(uil_progress_container, maximum=100, variable=pbar_varp)
    pbr_progress.place(x=180, y=25, width=304, height=24)

    lb_opentext = Label(uil_set_container, text="Now Opening")
    lb_opentext.grid(row=2, column=0, columnspan=2, sticky=N+E+W+S)

    lb_opendeck = Label(uil_set_container, text="--", borderwidth=2, relief="groove", bg="white")
    lb_opendeck.grid(row=2, column=2, sticky=N+E+W+S)

    lb_openhave = Label(uil_set_container, text="Have")
    lb_openhave.grid(row=2, column=3, sticky=E+W)

    havevalues = ["--", "Have"]
    cbxhave_open = ttk.Combobox(uil_set_container, height=2, width=5, values=havevalues, state="readonly")
    cbxhave_open.grid(row=2, column=4, sticky=N+E+W+S)
    cbxhave_open.set(havevalues[0])

    lb_openrank = Label(uil_set_container, text="Rank")
    lb_openrank.grid(row=2, column=5, sticky=E+W)

    rankvalues = ["★" + str(irv) for irv in range(0, 6)]
    cbxrank_open = ttk.Combobox(uil_set_container, height=6, width=5, values=rankvalues, state="readonly")
    cbxrank_open.grid(row=2, column=6, sticky=N+E+W+S)
    cbxrank_open.set(rankvalues[0])

    lb_openskill = Label(uil_set_container, text="Skill")
    lb_openskill.grid(row=2, column=7, sticky=E+W)

    skillvalues = ["Lv" + str(isv) for isv in range(1, 13)]
    cbxskill_open = ttk.Combobox(uil_set_container, height=13, width=5, values=skillvalues, state="readonly")
    cbxskill_open.grid(row=2, column=8, sticky=N+E+W+S)
    cbxskill_open.set(skillvalues[0])

    button_write = Button(uil_set_container, text="Change All", state="disabled")
    button_write.grid(row=2, column=9, sticky=E+W)

    uil_root.mainloop()
