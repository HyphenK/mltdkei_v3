# Python Module #
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import sqlite3
# IdolList for above ver.4.19 21/08/02

# Card Kind Info
# 1, 4 - Normal
# 2, 5 - Limited
# 3 - FES SSR
# 6, 7 - PST Ranking SR
# 8 - Million Collection SR/R
# 9 - Anniversary SSR

# LeaderSkill CenterID Section
# n - Normal
# ot - OneType
# sb - SongBonus
# 3tup - 105% + 10%
cg_actup = [201, 202, 301, 302, 401, 402]
cg_lifeup = [204, 205, 304, 305, 404, 405]
cg_allup = [111, 207, 208, 209, 307, 308, 309, 407, 408, 409]
cg_voup_n = [211, 212, 213, 311, 312, 313, 411, 412, 413]
cg_voup_ot = [221, 222, 321, 322, 421, 422]
cg_voup_sb = [231, 331, 431]
cg_voup_3tn = [121]
cg_voup_3tup = [122]
cg_daup_n = [214, 215, 216, 314, 315, 316, 414, 415, 416]
cg_daup_ot = [224, 225, 324, 325, 424, 425]
cg_daup_sb = [234, 334, 434]
cg_daup_3tn = [124]
cg_daup_3tup = [125]
cg_viup_n = [217, 218, 219, 317, 318, 319, 417, 418, 419]
cg_viup_ot = [227, 228, 327, 328, 427, 428]
cg_viup_sb = [237, 337, 437]
cg_viup_3tn = [127]
cg_viup_3tup = [128]

# IdolSkill SkillID Info
# 1, 2, 3 - Perfect Support
# 5 - Damage Guard
# 6 - Life Plus
# 7 - Combo Support
# 10, 11 - Score
# 12, 13 - Overclock
# 14, 15, 24, 25 - Multi Up
# 20, 21 - Combo
# 22, 23 - Overrondo
# 30, 31 - Double Boost
# 34 - Double Effect

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

    pbar_varp = IntVar()

    uil_set_container = Frame(uil_root, borderwidth=2, relief="groove")
    uil_set_container.grid(row=0, column=0)
    uil_container = Frame(uil_root)
    uil_container.grid(row=1, column=0)

    def buttoncmd_save():
        writedata = "\n".join(infodata)
        infofile = open(info_name, 'w', encoding='utf-8')
        infofile.write(writedata)
        infofile.close()
        msgbox.showinfo("Save Complete", "Save Complete")
        
    def make_list():
        ra = [i.get() for i in cbnra_list]
        ty = [i.get() for i in cbnty_list]
        ki = [i.get() for i in cbnki_list]
        ls = [i.get() for i in cbnls_list]
        lp = [i.get() for i in cbnlp_list]
        sk = [i.get() for i in cbnsk_list]
        r, rare, type = [["SSR+"], ["SR+"], ["R+"], ["N+"]], [], []
        for i in range(4):
            if ra[i] == 1: rare = rare + r[i]
            if ty[i] == 1: type = type + [i+1]
        a = ["'BRAND NEW PERFORMANCE%'", "'UNI-ONAIR%'", "'CHALLENGE FOR GLOW-RY DAYS%'", "'Reach 4 the Dream%'"]
        k, kind, anni = [[1, 4], [2, 5], [3], [6, 7], [8]], [], []
        for i in range(5):
            if ki[i] == 1: kind = kind + k[i]
        if 1 in ki[5:9]:
            for i in range(5, 9):
                if ki[i] == 1: anni.append(a[i-5])
        leader = []
        if ls[0] == 1:
            l = [cg_voup_n, cg_voup_ot, cg_voup_sb, cg_voup_3tn, cg_voup_3tup]
            for i in range(5):
                if lp[i] == 1: leader = leader + l[i]
        if ls[1] == 1:
            l = [cg_daup_n, cg_daup_ot, cg_daup_sb, cg_daup_3tn, cg_daup_3tup]
            for i in range(5):
                if lp[i] == 1: leader = leader + l[i]
        if ls[2] == 1:
            l = [cg_viup_n, cg_viup_ot, cg_viup_sb, cg_viup_3tn, cg_viup_3tup]
            for i in range(5):
                if lp[i] == 1: leader = leader + l[i]
        if ls[3] == 1:
            leader = leader + cg_allup
        if ls[4] == 1:
            leader = leader + cg_lifeup
        if ls[5] == 1:
            leader = leader + cg_actup
        s, skill = [[10, 11], [12, 13], [30, 31], [1, 2, 3], [5], [14, 15, 24, 25], [20, 21], [22, 23], [34], [6], [7]], []
        for i in range(11):
            if sk[i] == 1: skill = skill + s[i]
        while len(rare) < 2: rare = rare + [0]
        while len(type) < 2: type = type + [0]
        while len(kind) < 2: kind = kind + [0]
        while len(leader) < 2: leader = leader + [0]
        while len(skill) < 2: skill = skill + ['l']
        rare, type, kind, leader, skill = tuple(rare), tuple(type), tuple(kind), tuple(leader), tuple(skill)
        print_list = cur1.execute(f'''select idnumber, maxrank, photocode from idoldb
            natural inner join photocodedb natural inner join idoldb_sub natural inner join centerdb
            natural inner join skilldb where rare in {rare} and type in {type} and kind in {kind}
            and centerid in {leader} and skillid in {skill}''').fetchall()
        if len(anni) != 0:
            for i in range(len(anni)):
                print_list = print_list + cur1.execute(f'''select idnumber, maxrank, photocode from idoldb
                    natural inner join photocodedb natural inner join idoldb_sub natural inner join centerdb
                    natural inner join skilldb where name like {anni[i]} and rare in {rare} and type in {type}
                    and centerid in {leader} and skillid in {skill}''').fetchall()
        if "N+" in rare:
            print_list = print_list + cur1.execute('''select idnumber, maxrank, photocode from idoldb
                natural inner join photocodedb where rare = "N+"''').fetchall()
        return print_list

    def print_gui(inputed_list):
        nonlocal uil_container
        button_write.config(state="disabled")
        cbxhave_open.set(havevalues[0])
        cbxrank_open.set(rankvalues[0])
        cbxskill_open.set(skillvalues[0])
        uil_container.destroy()
        uil_container = Frame(uil_root)
        uil_canvas = Canvas(uil_container, width=990, height=505)
        scrollbar = Scrollbar(uil_container, command=uil_canvas.yview)
        scrollable_frame = Frame(uil_canvas)

        scrollable_frame.bind("<Configure>", lambda e: uil_canvas.configure(scrollregion=uil_canvas.bbox("all")))

        uil_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        uil_canvas.configure(yscrollcommand=scrollbar.set)

        uil_container.grid(row=1, column=0)
        uil_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        lb_protect1 = Label(uil_set_container, text="Now Loading...")
        lb_protect1.grid(row=0, column=0, rowspan=3, columnspan=5, sticky=N+E+W+S)
        lb_protect2 = Label(uil_set_container, text=" ")
        lb_protect2.grid(row=3, column=0, sticky=N+E+W+S)
        countout, lenin, countcol, countrow = 0, len(inputed_list), 0, 0
        lb_progressleft.config(text=countout)
        lb_progressright.config(text=lenin)
        pbar_varp.set(countout)
        pbr_progress.config(maximum=lenin)
        uil_root.update()

        def dataprint(inputed_data, maxrank, image, r, c):
            inputed_data = inputed_data.split(',')
            idnumber = int(inputed_data[0])
            have, rank, skill = inputed_data[-3:]

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
                if triple[1] <= 4 and int(data[-2]) > 4: data[-2] = '4'
                if triple[1] <= 4 and int(data[-1]) > 10: data[-1] = '10'
                edited_data = ",".join(data)
                if IDB_name == 'mltdkei_idoldata.sqlite':
                    if triple[0] < 1064: infodata[triple[0]-1] = edited_data
                    elif triple[0] > 1065: infodata[triple[0]-3] = edited_data
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if triple[0] > 9000: infodata[triple[0]-9001] = edited_data
                    elif triple[0] < 1064: infodata[triple[0]+2] = edited_data
                    elif triple[0] > 1065: infodata[triple[0]] = edited_data
            print_gui(inputed_list)

        lb_protect1.destroy()
        lb_protect2.destroy()
        button_write.config(command=config_all, state="normal")

    button_save = Button(uil_set_container, text="Save", width=7, command=buttoncmd_save)
    button_save.grid(row=0, column=0, rowspan=2, sticky=N+S)
    
    button_load = Button(uil_set_container, text="Load", width=7, command=lambda: print_gui(make_list()))
    button_load.grid(row=2, column=0, rowspan=2, sticky=N+S)
    
    # Rare Section
    cbnra_list = [IntVar() for i in range(4)]
    cbnra_text = ["SSR", "SR", "R", "N"]
    cbnra_list[0].set(1)
    
    uil_ra_container = Frame(uil_set_container, borderwidth=2, relief="groove")
    uil_ra_container.grid(row=0, column=1, sticky=N+E+W+S)
    
    lb_ra = Label(uil_ra_container, text="Rarity")
    lb_ra.grid(row=0, column=0)
    
    for i in range(len(cbnra_list)):
        cbnra = Checkbutton(uil_ra_container, text=cbnra_text[i], variable=cbnra_list[i])
        cbnra.grid(row=0, column=i+1)
    
    # Type Section
    cbnty_list = [IntVar() for i in range(4)]
    cbnty_text = ["Pr", "Fa", "An", "Ex"]
    cbnty_list[0].set(1)
    
    uil_ty_container = Frame(uil_set_container, borderwidth=2, relief="groove")
    uil_ty_container.grid(row=0, column=2, sticky=N+E+W+S)
    
    lb_ty = Label(uil_ty_container, text="Type")
    lb_ty.grid(row=0, column=0)
    
    for i in range(len(cbnty_list)):
        cbnty = Checkbutton(uil_ty_container, text=cbnty_text[i], variable=cbnty_list[i])
        cbnty.grid(row=0, column=i+1)
    
    # Kind Section
    cbnki_list = [IntVar() for i in range(9)]
    cbnki_text = ["Normal", "Limited", "FES", "PST", "Milicore", "1st", "2nd", "3rd", "4th"]
    for i in range(3):
        cbnki_list[i].set(1)
        
    uil_ki_container = Frame(uil_set_container, borderwidth=2, relief="groove")
    uil_ki_container.grid(row=0, column=3, columnspan=2, sticky=N+E+W+S)
    
    lb_ki = Label(uil_ki_container, text="Category")
    lb_ki.grid(row=0, column=0)
    
    for i in range(len(cbnki_list)):
        cbnki = Checkbutton(uil_ki_container, text=cbnki_text[i], variable=cbnki_list[i])
        cbnki.grid(row=0, column=i+1)
    
    # Leader Skill Section
    cbnls_list = [IntVar() for i in range(6)]
    cbnls_text = ["Vocal", "Dance", "Visual", "All", "Life", "SkillAct"]
    for i in range(len(cbnls_list)):
        cbnls_list[i].set(1)
    cbnlp_list = [IntVar() for i in range(5)]
    cbnlp_text = ["Normal", "OneType", "SongBonus", "3Type", "3Type+SkillAct"]
    for i in range(len(cbnlp_list)):
        cbnlp_list[i].set(1)
        
    uil_ls_container = Frame(uil_set_container, borderwidth=2, relief="groove")
    uil_ls_container.grid(row=1, column=1, rowspan=2, columnspan=3, sticky=N+E+W+S)
    
    lsct_line1 = Frame(uil_ls_container)
    lsct_line1.grid(row=0, column=0)
    
    lsct_line2 = Frame(uil_ls_container)
    lsct_line2.grid(row=1, column=0)
    
    lb_ls = Label(lsct_line1, text="LeaderSkill")
    lb_ls.grid(row=0, column=0)
    
    for i in range(len(cbnls_list)):
        cbnls = Checkbutton(lsct_line1, text=cbnls_text[i], variable=cbnls_list[i])
        cbnls.grid(row=0, column=i+1)
        
    for i in range(len(cbnlp_list)):
        cbnlp = Checkbutton(lsct_line2, text=cbnlp_text[i], variable=cbnlp_list[i])
        cbnlp.grid(row=0, column=i)
        
    # Skill Section
    cbnsk_list = [IntVar() for i in range(11)]
    cbnsk_text = ["ScoreUp", "OverClock", "DoubleBoost", "LifeHeal", "PerfectSupport",
                  "MultiUp", "ComboUp", "OverRondo", "DoubleEffect", "NoDamage", "ComboSupport"]
    for i in range(len(cbnsk_list)):
        cbnsk_list[i].set(1)
    
    uil_sk_container = Frame(uil_set_container, borderwidth=2, relief="groove")
    uil_sk_container.grid(row=1, column=4, rowspan=2, sticky=N+E+W+S)
    
    lb_sk = Label(uil_sk_container, text="Idol Skill")
    lb_sk.grid(row=0, column=0)
    
    for i in range(5):
        cbnsk = Checkbutton(uil_sk_container, text=cbnsk_text[i], variable=cbnsk_list[i])
        cbnsk.grid(row=0, column=i+1)
        
    for i in range(6):
        cbnsk = Checkbutton(uil_sk_container, text=cbnsk_text[i+5], variable=cbnsk_list[i+5])
        cbnsk.grid(row=1, column=i)
        
    # Line 4 Section
    uil_line4_container = Frame(uil_set_container, borderwidth=2, relief="groove")
    uil_line4_container.grid(row=3, column=1, columnspan=4)
    
    # Progress Section
    lb_progressleft = Label(uil_line4_container, width=7, borderwidth=2, relief="groove", bg="white")
    lb_progressleft.grid(row=0, column=0, sticky=N+E+W+S)

    lb_progressmiddle = Label(uil_line4_container, text="/")
    lb_progressmiddle.grid(row=0, column=1)

    lb_progressright = Label(uil_line4_container, width=7, borderwidth=2, relief="groove", bg="white")
    lb_progressright.grid(row=0, column=2, sticky=N+E+W+S)
    
    fr_progress = Frame(uil_line4_container, width=285)
    fr_progress.grid(row=0, column=3, sticky=N+E+W+S)

    pbr_progress = ttk.Progressbar(fr_progress, maximum=100, variable=pbar_varp)
    pbr_progress.place(x=0, y=0, width=285, height=25)

    # Editor Section
    lb_openhave = Label(uil_line4_container, text="Have", width=8)
    lb_openhave.grid(row=0, column=4, sticky=E+W)

    havevalues = ["--", "Have"]
    cbxhave_open = ttk.Combobox(uil_line4_container, height=2, width=5, values=havevalues, state="readonly")
    cbxhave_open.grid(row=0, column=5, sticky=N+E+W+S)
    cbxhave_open.set(havevalues[0])

    lb_openrank = Label(uil_line4_container, text="Rank", width=8)
    lb_openrank.grid(row=0, column=6, sticky=E+W)

    rankvalues = ["★" + str(irv) for irv in range(6)]
    cbxrank_open = ttk.Combobox(uil_line4_container, height=6, width=5, values=rankvalues, state="readonly")
    cbxrank_open.grid(row=0, column=7, sticky=N+E+W+S)
    cbxrank_open.set(rankvalues[0])

    lb_openskill = Label(uil_line4_container, text="Skill", width=8)
    lb_openskill.grid(row=0, column=8, sticky=E+W)

    skillvalues = ["Lv" + str(isv) for isv in range(1, 13)]
    cbxskill_open = ttk.Combobox(uil_line4_container, height=13, width=5, values=skillvalues, state="readonly")
    cbxskill_open.grid(row=0, column=9, sticky=N+E+W+S)
    cbxskill_open.set(skillvalues[0])

    button_write = Button(uil_line4_container, text="Change All", width=24, state="disabled")
    button_write.grid(row=0, column=10, sticky=E+W)

    uil_root.mainloop()
