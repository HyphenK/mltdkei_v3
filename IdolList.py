# Python Module #
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import sqlite3
# IdolList for above ver.4.12 21/07/13

def main_idollist(iconext, IDB_name, info_name):
    conn1 = sqlite3.connect(IDB_name)
    cur1 = conn1.cursor()
    try:
        infofile = open(info_name, 'r', encoding='utf-8')
        infodata = infofile.read().split('\n')
        infofile.close()
        if len(infodata)-1 != int(cur1.execute('select count(idnumber) from idoldb').fetchone()[0]): raise Exception
    except:
        msgbox.showinfo('Error', 'Info File is damaged or not updated.\nPlease check your file or update DB first.')
        return

    uil_root = Toplevel()
    uil_root.title("Idol List Editor for MLTD Deck Analyzer")
    uil_root.geometry("+80+25")
    uil_root.resizable(False, False)

    hlist = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    whath = ['SSR-Pr', 'SSR-Fa', 'SSR-An', 'SR-Pr', 'SR-Fa', 'SR-An', 'SR-Ex',
        'R-Pr', 'R-Fa', 'R-An', 'N-All', 'SSR-1st', 'SSR-2nd', 'SSR-3rd', 'SSR-4th']

    anniversary = ["'BRAND NEW PERFORMANCE%'", "'UNI-ONAIR%'", "'CHALLENGE FOR GLOW-RY DAYS%'", "'Reach 4 the Dream%'"]
    pbar_varp = IntVar()

    hlist[0] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        natural inner join idoldb_sub where kind < 4 and type = 1''').fetchall()
    hlist[1] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        natural inner join idoldb_sub where kind < 4 and type = 2''').fetchall()
    hlist[2] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        natural inner join idoldb_sub where kind < 4 and type = 3''').fetchall()
    hlist[3] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "SR+" and type = 1''').fetchall()
    hlist[4] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "SR+" and type = 2''').fetchall()
    hlist[5] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "SR+" and type = 3''').fetchall()
    hlist[6] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "SR+" and type = 4''').fetchall()
    hlist[7] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "R+" and type = 1''').fetchall()
    hlist[8] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "R+" and type = 2''').fetchall()
    hlist[9] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "R+" and type = 3''').fetchall()
    hlist[10] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        where rare = "N+"''').fetchall()
    hlist[11] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        natural inner join idoldb_sub where kind = 9 and name like {anniversary[0]}''').fetchall()
    hlist[12] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        natural inner join idoldb_sub where kind = 9 and name like {anniversary[1]}''').fetchall()
    hlist[13] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        natural inner join idoldb_sub where kind = 9 and name like {anniversary[2]}''').fetchall()
    hlist[14] = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb natural inner join photocodedb
        natural inner join idoldb_sub where kind = 9 and name like {anniversary[3]}''').fetchall()

    uil_set_container = Frame(uil_root, width=1015, height=75, borderwidth=2, relief="groove")
    uil_set_container.grid(row=0, column=0)
    uil_container = Frame(uil_root)
    uil_container.grid(row=1, column=0)

    def buttoncmd_save():
        writedata = "\n".join(infodata)
        infofile = open(info_name, 'w', encoding='utf-8')
        infofile.write(writedata)
        infofile.close()
        msgbox.showinfo("Save Complete", "Save Complete")

    def print_gui(inputed_list):
        nonlocal uil_container
        button_write.config(state="disabled")
        cbxhave_open.set(havevalues[0])
        cbxrank_open.set(rankvalues[0])
        cbxskill_open.set(skillvalues[0])
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

        lb_opendeck.config(text=whath[hlist.index(inputed_list)])
        uil_root.update()

        def dataprint(inputed_data, maxrank, image, r, c):
            inputed_data = inputed_data.split(',')
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

            def printdata(what):
                if what == "have": inputed_data[-3] = str(havevalues.index(cbxhave.get()))
                elif what == "rank": inputed_data[-2] = str(rankvalues.index(cbxrank.get()))
                elif what == "skill": inputed_data[-1] = str(skillvalues.index(cbxskill.get())+1)
                edited_data = ",".join(inputed_data)
                if IDB_name == 'mltdkei_idoldata.sqlite':
                    if idnumber < 1064: infodata[idnumber-1] = edited_data
                    elif idnumber > 1065: infodata[idnumber-3] = edited_data
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if idnumber > 9000: infodata[idnumber-9001] = edited_data
                    elif idnumber < 1064: infodata[idnumber+2] = edited_data
                    elif idnumber > 1065: infodata[idnumber] = edited_data

            cbxhave = ttk.Combobox(scrollable_frame, height=2, width=5, values=havevalues, state="readonly")
            cbxhave.grid(row=r+1, column=c)
            cbxhave.set(havevalues[int(have)])
            cbxhave.bind("<<ComboboxSelected>>", lambda unused_option: printdata("have"))

            rv = ["★" + str(irv) for irv in range(5)]
            if maxrank == 5: rv = rv + ["★5"]
            cbxrank = ttk.Combobox(scrollable_frame, height=6, width=5, values=rv, state="readonly")
            cbxrank.grid(row=r+2, column=c)
            cbxrank.set(rankvalues[int(rank)])
            cbxrank.bind("<<ComboboxSelected>>", lambda unused_option: printdata("rank"))

            sv = ["Lv" + str(isv) for isv in range(1, 11)]
            if maxrank == 5: sv = sv + ["Lv11", "Lv12"]
            cbxskill = ttk.Combobox(scrollable_frame, height=13, width=5, values=sv, state="readonly")
            cbxskill.grid(row=r+3, column=c)
            cbxskill.set(skillvalues[int(skill)-1])
            cbxskill.bind("<<ComboboxSelected>>", lambda unused_option: printdata("skill"))

        for triple in inputed_list:
            if IDB_name == 'mltdkei_idoldata.sqlite':
                if triple[0] < 1064: data = infodata[triple[0]-1]
                elif triple[0] > 1065: data = infodata[triple[0]-3]
            elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                if triple[0] > 9000: data = infodata[triple[0]-9001]
                elif triple[0] < 1064: data = infodata[triple[0]+2]
                elif triple[0] > 1065: data = infodata[triple[0]]
            dataprint(data, triple[1], triple[2], countrow, countcol)
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
            for triple in inputed_list:
                if IDB_name == 'mltdkei_idoldata.sqlite':
                    if triple[0] < 1064: data = infodata[triple[0]-1]
                    elif triple[0] > 1065: data = infodata[triple[0]-3]
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if triple[0] > 9000: data = infodata[triple[0]-9001]
                    elif triple[0] < 1064: data = infodata[triple[0]+2]
                    elif triple[0] > 1065: data = infodata[triple[0]]
                data = data.split(",")
                data[-3] = str(havevalues.index(cbxhave_open.get()))
                data[-2] = str(rankvalues.index(cbxrank_open.get()))
                data[-1] = str(skillvalues.index(cbxskill_open.get())+1)
                edited_data = ",".join(data)
                if IDB_name == 'mltdkei_idoldata.sqlite':
                    if triple[0] < 1064: infodata[triple[0]-1] = edited_data
                    elif triple[0] > 1065: infodata[triple[0]-3] = edited_data
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if triple[0] > 9000: infodata[triple[0]-9001] = edited_data
                    elif triple[0] < 1064: infodata[triple[0]+2] = edited_data
                    elif triple[0] > 1065: infodata[triple[0]] = edited_data
            print_gui(inputed_list)

        lb_protect.destroy()
        button_write.config(command=config_all, state="normal")

    button_save = Button(uil_set_container, text="Save", width=7, command=buttoncmd_save)
    button_save.grid(row=0, column=0, rowspan=2, sticky=N+S)

    class PB:
        def place(self, no, r, c):
            self.button = Button(uil_set_container, text=whath[no], width=7, command=lambda: print_gui(hlist[no]))
            self.button.grid(row=r, column=c)

    button_ssrpr = PB()
    button_ssrpr.place(0, 0, 1)

    button_ssrfa = PB()
    button_ssrfa.place(1, 0, 2)

    button_ssran = PB()
    button_ssran.place(2, 0, 3)

    button_ssr1st = PB()
    button_ssr1st.place(11, 0, 4)

    button_ssr2nd = PB()
    button_ssr2nd.place(12, 0, 5)

    button_ssr3rd = PB()
    button_ssr3rd.place(13, 0, 6)

    button_ssr4th = PB()
    button_ssr4th.place(14, 0, 7)

    button_ssr5th = Button(uil_set_container, text="SSR-5th", state="disabled")
    button_ssr5th.grid(row=0, column=8, sticky=E+W)

    button_srpr = PB()
    button_srpr.place(3, 1, 1)

    button_srfa = PB()
    button_srfa.place(4, 1, 2)

    button_sran = PB()
    button_sran.place(5, 1, 3)

    button_srex = PB()
    button_srex.place(6, 1, 4)

    button_rpr = PB()
    button_rpr.place(7, 1, 5)

    button_rfa = PB()
    button_rfa.place(8, 1, 6)

    button_ran = PB()
    button_ran.place(9, 1, 7)

    button_nall = PB()
    button_nall.place(10, 1, 8)

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

    rankvalues = ["★" + str(irv) for irv in range(6)]
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
