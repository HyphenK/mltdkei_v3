# Python Module #
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import sqlite3
# IdolList for above ver.4.5 22/02/22

# Card Kind Info
# 1, 4 - Normal SSR // SR, R, N
# 2, 5 - Limited SSR // SR
# 3 - FES SSR
# 6, 7 - PST Ranking // Point SR
# 8 - Million Collection SR, R
# 9 - Anniversary SSR

# Vdv(Leader Effect) Info
# 1 - Vocal
# 2 - Dance
# 3 - Visual
# 4 - All
# 5 - Life
# 6 - Skill
# 7 - No Effect

# Idol Skill SkillID Info
# 0 - No Skill
# 1, 2, 3 - Perfect Support
# 5 - Damage Guard
# 6 - Life Plus
# 7 - Combo Support
# 10, 11 - Score
# 13 - Overclock (12)
# 15 - Multi Up (14, 24, 25)
# 20 - Combo (21)
# 22 - Overrondo (23)
# 30 - Double Boost (31)
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

    fr_set = Frame(uil_root, borderwidth=2, relief="groove")
    fr_set.grid(row=0, column=0, rowspan=2)
    
    # Editor Section
    fr_edi = Frame(uil_root, borderwidth=2, relief="groove")
    fr_edi.grid(row=0, column=1)
    
    lb_openhave = Label(fr_edi, text="Have", width=6)
    lb_openhave.grid(row=0, column=0)

    havevalues = ["--", "Have"]
    cbxhave_open = ttk.Combobox(fr_edi, height=2, width=6, values=havevalues, state="readonly")
    cbxhave_open.grid(row=0, column=1)
    cbxhave_open.set(havevalues[0])

    lb_openrank = Label(fr_edi, text="Rank", width=6)
    lb_openrank.grid(row=0, column=2)

    rankvalues = ["★" + str(irv) for irv in range(6)]
    cbxrank_open = ttk.Combobox(fr_edi, height=6, width=6, values=rankvalues, state="readonly")
    cbxrank_open.grid(row=0, column=3)
    cbxrank_open.set(rankvalues[0])

    lb_openskill = Label(fr_edi, text="Skill", width=6)
    lb_openskill.grid(row=0, column=4)

    skillvalues = ["Lv" + str(isv) for isv in range(1, 13)]
    cbxskill_open = ttk.Combobox(fr_edi, height=13, width=6, values=skillvalues, state="readonly")
    cbxskill_open.grid(row=0, column=5)
    cbxskill_open.set(skillvalues[0])

    button_write = Button(fr_edi, text="Change All Idols on Window", width=24, state="disabled")
    button_write.grid(row=0, column=6)
    
    fr_card = Frame(uil_root)
    fr_card.grid(row=1, column=1)
    uil_canvas = Canvas(fr_card, width=499, height=500)
    uil_canvas.pack(side="left", fill="both", expand=True)
    scrollbar = Scrollbar(fr_card, command=uil_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    def buttoncmd_save():
        writedata = "\n".join(infodata)
        infofile = open(info_name, 'w', encoding='utf-8')
        infofile.write(writedata)
        infofile.close()
        msgbox.showinfo("Save Complete", "Save Complete")
        
    def make_list():
        hv = set_have.read_set() # mltdkei_info.txt
        ty = set_type.read_set() # IdolDB - Type
        ra = set_rare.read_set() # IdolDB - Rare
        mr = set_maxr.read_set() # IdolDB - MaxRank
        ki = set_kind.read_set() # IdolDB_sub - Kind & Hair // IdolDB - Name
        cl = set_cloth.read_set() # IdolDB - Name
        ls = set_leaderB.read_set() # IdolDB_sub - Vdv
        lp = set_leaderT.read_set() # CenterDB - CenterID
        sk = set_skill.read_set() # SkillDB - SkillID
        ct = set_cool.read_set() # SkillDB - Gap
        na = set_idol.read_set() # IdolDB_sub - IdolID
                
        # Type // Rare
        r, rare, type = [["SSR+"], ["SR+"], ["R+"], ["N+"]], [], []
        for i in range(4):
            if ty[i] == 1: type = type + [i+1]
            if ra[i] == 1: rare = rare + r[i]
        
        # MaxRank
        maxr = []
        for i in range(2):
            if mr[i] == 1: maxr = maxr + [i+4]
        
        # Category(Kind) // Hair
        a = ["'BRAND NEW PERFORMANCE%'", "'UNI-ONAIR%'", "'CHALLENGE FOR GLOW-RY DAYS%'", "'Reach 4 the Dream%'"]
        k, kind, anni = [[1, 4], [2, 5], [3], [2], [6, 7], [8]], [], []
        for i in range(6):
            if ki[i] == 1: kind = kind + k[i]
        for i in range(6, 10):
            if ki[i] == 1: anni.append(a[i-6])
        if len(kind) == 1 and ki[3] == 1: hair = [-1, 2]
        elif len(kind) != 1 and ki[3] == 1: hair = [1, 2]
        else: hair = [-1, 1]
        
        # Clothes
        c = ["'制服シリーズ%'", "'MILLION LIVE CLOSET!%'", "'夏服シリーズ%'", "'MILLION LIVE CONFERENCE!%'"]
        clot = []
        for i in range(4):
            if cl[i] == 1: clot.append(c[i])
        
        # Leader Effect
        leader = []
        if ls[0] == 1: # Normal // One Type // Song Bonus // 3Type // 3Type + Skill
            l = [[211, 212, 213, 311, 312, 313, 411, 412, 413], [221, 222, 321, 322, 421, 422], [231, 331, 431], [121], [122]]
            for i in range(5):
                if lp[i] == 1: leader = leader + l[i]
        if ls[1] == 1: # Normal // One Type // Song Bonus // 3Type // 3Type + Skill
            l = [[214, 215, 216, 314, 315, 316, 414, 415, 416], [224, 225, 324, 325, 424, 425], [234, 334, 434], [124], [125]]
            for i in range(5):
                if lp[i] == 1: leader = leader + l[i]
        if ls[2] == 1: # Normal // One Type // Song Bonus // 3Type // 3Type + Skill
            l = [[217, 218, 219, 317, 318, 319, 417, 418, 419], [227, 228, 327, 328, 427, 428], [237, 337, 437], [127], [128]]
            for i in range(5):
                if lp[i] == 1: leader = leader + l[i]
        if ls[3] == 1: # All Up
            leader = leader + [111, 207, 208, 209, 307, 308, 309, 407, 408, 409]
        if ls[4] == 1: # Life
            leader = leader + [204, 205, 304, 305, 404, 405]
        if ls[5] == 1: # Skill
            leader = leader + [201, 202, 301, 302, 401, 402]
        if ls[6] == 1: # No Effect
            leader = leader + [101]
            
        # Skill
        s, skill = [[10, 11], [12, 13], [20, 21], [22, 23], [30, 31], [34], [14, 15, 24, 25], [1, 2, 3], [5], [6], [7], [0]], []
        for i in range(12):
            if sk[i] == 1: skill = skill + s[i]
            
        # Cooltime
        l, cool = [6, 7, 8, 9, 10, 11, 12, 13, 14, 0], []
        for i in range(10):
            if ct[i] == 1: cool.append(l[i])
            
        # Idol Name
        name = []
        for i in range(56):
            if na[i] == 1: name = name + [i+1]
        
        while len(type) < 2: type = type + [-1]
        while len(rare) < 2: rare = rare + [-1]
        while len(maxr) < 2: maxr = maxr + [-1]
        while len(kind) < 2: kind = kind + [-1]
        while len(leader) < 2: leader = leader + [-1]
        while len(skill) < 2: skill = skill + [-1]
        while len(cool) < 2: cool = cool + [-1]
        while len(name) < 2: name = name + [-1]
        type, rare, maxr, kind, leader, skill, cool, name = tuple(type), tuple(rare), tuple(maxr), tuple(kind), tuple(leader), tuple(skill), tuple(cool), tuple(name)
        hair, anni, clot = tuple(hair), tuple(anni), tuple(clot)
        
        print_list = []
        if len(clot) == 0:
            print_list = print_list + cur1.execute(f'''select idnumber, maxrank, photocode from idoldb
                natural inner join photocodedb natural inner join idoldb_sub natural inner join centerdb
                natural inner join skilldb where type in {type} and rare in {rare} and maxrank in {maxr} and kind in {kind}
                and centerid in {leader} and skillid in {skill} and gap in {cool} and idolid in {name} and hair in {hair}''').fetchall()
            if len(anni) != 0:
                for i in range(len(anni)):
                    print_list = print_list + cur1.execute(f'''select idnumber, maxrank, photocode from idoldb
                        natural inner join photocodedb natural inner join idoldb_sub natural inner join centerdb
                        natural inner join skilldb where name like {anni[i]} and type in {type} and rare in {rare} and maxrank in {maxr} 
                        and centerid in {leader} and skillid in {skill} and gap in {cool} and idolid in {name} and hair in {hair}''').fetchall()
        else:
            for i in range(len(clot)):
                print_list = print_list + cur1.execute(f'''select idnumber, maxrank, photocode from idoldb
                    natural inner join photocodedb natural inner join idoldb_sub natural inner join centerdb
                    natural inner join skilldb where name like {clot[i]} and type in {type} and rare in {rare} and maxrank in {maxr} 
                    and centerid in {leader} and skillid in {skill} and gap in {cool} and idolid in {name} and hair in {hair}''').fetchall()
        print_list.sort()
        
        # Have
        if hv == [1, 1]:
            return print_list
        else:
            print_list2 = []
            for triple in print_list:
                if IDB_name == 'mltdkei_idoldata.sqlite':
                    if triple[0] < 1064: d = infodata[triple[0]-1].split(",")[-3]
                    elif 1065 < triple[0] < 1444: d = infodata[triple[0]-3].split(",")[-3]
                    elif 1444 < triple[0]: d = infodata[triple[0]-4].split(",")[-3]
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if triple[0] > 9000: d = infodata[triple[0]-9001].split(",")[-3]
                    else: d = infodata[triple[0]+2].split(",")[-3]
                if hv[0] == 1 and d == '1': print_list2.append(triple)
                if hv[1] == 1 and d == '0': print_list2.append(triple)
            return print_list2

    def print_gui(inputed_list):
        nonlocal uil_canvas, scrollbar
        button_write.config(state="disabled")
        cbxhave_open.set(havevalues[0])
        cbxrank_open.set(rankvalues[0])
        cbxskill_open.set(skillvalues[0])
        
        uil_canvas.destroy()
        uil_canvas = Canvas(fr_card, width=499, height=500)
        uil_canvas.pack(side="left", fill="both", expand=True)
        scrollable_frame = Frame(uil_canvas)
        scrollable_frame.bind("<Configure>", lambda e: uil_canvas.configure(scrollregion=uil_canvas.bbox("all")))
        uil_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        uil_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=uil_canvas.yview)

        lb_protect1 = Label(fr_set, text="Now Loading...")
        lb_protect1.grid(row=2, column=0, columnspan=2, sticky=N+E+W+S)
        button_save.config(state="disabled")
        button_load.config(state="disabled")
        countout, lenin, countcol, countrow = 0, len(inputed_list), 0, 0
        lb_pgrL.config(text=countout)
        lb_pgrR.config(text=lenin)
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
                    elif 1065 < idnumber < 1444: infodata[idnumber-3] = edited_data
                    elif 1444 < idnumber: infodata[idnumber-4] = edited_data
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if idnumber > 9000: infodata[idnumber-9001] = edited_data
                    else: infodata[idnumber+2] = edited_data

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
                elif 1065 < triple[0] < 1444: data = infodata[triple[0]-3]
                elif 1444 < triple[0]: data = infodata[triple[0]-4]
            elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                if triple[0] > 9000: data = infodata[triple[0]-9001]
                else: data = infodata[triple[0]+2]
            dataprint(data, triple[1], triple[2], countrow, countcol)
            countout = countout + 1
            lb_pgrL.config(text=countout)
            pbar_varp.set(countout)
            countcol = countcol + 1
            uil_root.update()
            if countcol == 8:
                countcol = 0
                countrow = countrow + 4

        def config_all():
            if len(inputed_list) == 0: return
            for triple in inputed_list:
                if IDB_name == 'mltdkei_idoldata.sqlite':
                    if triple[0] < 1064: data = infodata[triple[0]-1]
                    elif 1065 < triple[0] < 1444: data = infodata[triple[0]-3]
                    elif 1444 < triple[0]: data = infodata[triple[0]-4]
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if triple[0] > 9000: data = infodata[triple[0]-9001]
                    else: data = infodata[triple[0]+2]
                data = data.split(",")
                data[-3] = str(havevalues.index(cbxhave_open.get()))
                data[-2] = str(rankvalues.index(cbxrank_open.get()))
                data[-1] = str(skillvalues.index(cbxskill_open.get())+1)
                if triple[1] <= 4 and int(data[-2]) > 4: data[-2] = '4'
                if triple[1] <= 4 and int(data[-1]) > 10: data[-1] = '10'
                edited_data = ",".join(data)
                if IDB_name == 'mltdkei_idoldata.sqlite':
                    if triple[0] < 1064: infodata[triple[0]-1] = edited_data
                    elif 1065 < triple[0] < 1444: infodata[triple[0]-3] = edited_data
                    elif 1444 < triple[0]: infodata[triple[0]-4] = edited_data
                elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
                    if triple[0] > 9000: infodata[triple[0]-9001] = edited_data
                    else: infodata[triple[0]+2] = edited_data
            print_gui(inputed_list)

        lb_protect1.destroy()
        button_save.config(state="normal")
        button_load.config(state="normal")
        button_write.config(command=config_all, state="normal")
            
    button_save = Button(fr_set, text="Save", command=buttoncmd_save)
    button_save.grid(row=0, column=0, ipady=14, sticky=N+E+W+S)
    
    button_load = Button(fr_set, text="Load", command=lambda: print_gui(make_list()))
    button_load.grid(row=0, column=1, ipady=14, sticky=N+E+W+S)
        
    # Progress Section
    fr_pgr = Frame(fr_set, borderwidth=2, relief="groove")
    fr_pgr.grid(row=1, column=0, columnspan=2, sticky="N"+"E"+"W"+"S")
    
    lb_pgrL = Label(fr_pgr, width=6, borderwidth=2, relief="groove", bg="white")
    lb_pgrL.grid(row=0, column=0, ipady=1)

    lb_pgrM = Label(fr_pgr, text="/")
    lb_pgrM.grid(row=0, column=1)

    lb_pgrR = Label(fr_pgr, width=6, borderwidth=2, relief="groove", bg="white")
    lb_pgrR.grid(row=0, column=2, ipady=1)
    
    fr_progress = Frame(fr_pgr, width=225)
    fr_progress.grid(row=0, column=3, sticky="N"+"E"+"W"+"S")

    pbr_progress = ttk.Progressbar(fr_progress, maximum=100, variable=pbar_varp)
    pbr_progress.place(x=0, y=0, width=225, height=22)

    # Setting Section    
    ntSet = ttk.Notebook(fr_set)
    ntSet.grid(row=2, column=0, columnspan=2)
    
    ntGS = Frame(fr_set)
    ntSet.add(ntGS, text="  General / Clothes  ")
    
    ntSS = Frame(fr_set)
    ntSet.add(ntSS, text="  Leader Effect / Skill  ")
    
    ntName = Frame(fr_set)
    ntSet.add(ntName, text="  Idol Name  ")
        
    class Settings:
        def __init__(self, wf, name, wx, wy, amount, txt, split, default):
            self.fr = Frame(wf, borderwidth=2, relief="groove")
            self.fr.grid(row=wx, column=wy, sticky="N"+"E"+"W"+"S")
            
            self.fr_up = Frame(self.fr)
            self.fr_up.grid(row=0, column=0, sticky="W")
            self.lb_name = Label(self.fr_up, text=name)
            self.lb_name.grid(row=0, column=0, sticky="W")
            self.var_all = IntVar()
            self.cbn_all = Checkbutton(self.fr_up, text="All", variable=self.var_all)
            self.cbn_all.grid(row=0, column=1, sticky="W")
            
            self.fr_list = [Frame(self.fr) for i in range(len(split))]
            for i in range(len(split)): self.fr_list[i].grid(row=i+1, column=0, sticky="W")
            
            self.var_list = [IntVar() for i in range(amount)]
            self.spl, self.split = 0, []
            for i in split:
                for j in range(i):
                    self.split.append(self.spl)
                self.spl += 1
            self.cbn_list = [Checkbutton(self.fr_list[self.split[i]], text=txt[i], variable=self.var_list[i]) for i in range(amount)]
            for i in range(amount): self.cbn_list[i].grid(row=0, column=i, sticky="W")
            
            def change_all(event):
                if self.var_all.get() == 0:
                    for i in self.cbn_list: i.select()
                elif self.var_all.get() == 1:
                    for i in self.cbn_list: i.deselect()
            self.cbn_all.bind('<Button-1>', change_all)
            
            for i in default:
                if i == 0:
                    for j in self.cbn_list: j.select()
                    self.cbn_all.select()
                else:
                    self.cbn_list[i-1].select()
            
        def read_set(self):
            return [i.get() for i in self.var_list]
        
    # Have Section
    set_have = Settings(ntGS, "Have", 0, 0, 2, ["Have", "Non-Have"], [2], [0])
    # Type Section
    set_type = Settings(ntGS, "Type", 1, 0, 4, ["Pr", "Fa", "An", "Ex"], [4], [1])
    # Rare Section
    set_rare = Settings(ntGS, "Rarity", 2, 0, 4, ["SSR", "SR", "R", "N"], [4], [1])
    # MaxRank Section
    set_maxr = Settings(ntGS, "Max Master Rank", 3, 0, 2, ["★4", "★5"], [2], [0])
    # Category(Kind) Section
    set_kind = Settings(ntGS, "Category", 4, 0, 10, ["Normal", "Limited", "FES", "SHS", "PST", "Milicore", "1st", "2nd", "3rd", "4th      "], [4, 6], [1, 2, 3, 4])
    # Clothes Section
    set_cloth = Settings(ntGS, "Clothes Series (Exclusive)", 5, 0, 4, ["制服シリーズ", "MILLION LIVE CLOSET!", "夏服シリーズ", "MILLION LIVE CONFERENCE!"], [1, 1, 1, 1], [])
    # Leader Effect (Object) Section
    set_leaderB = Settings(ntSS, "Leader Effect (Object)", 0, 0, 7, ["Vocal", "Dance", "Visual", "All Up", "Life", "Skill", "No Effect"], [3, 4], [0])
    # Leader Effect (Type) Section
    set_leaderT = Settings(ntSS, "Leader Effect (Type)", 1, 0, 5, ["Normal", "One Type", "Song Bonus", "3Type", "3Type + Skill"], [3, 2], [0])
    # Skill Section
    set_skill = Settings(ntSS, "Idol Skill", 2, 0, 12, ["Score Up", "Overclock", "Combo Up", "Overrondo", "Double Boost", "Double Effect", "Multi Up", "Life Recovery", "Damage Guard", "Perfect Support", "Combo Support", "No Skill        "], [2, 2, 2, 3, 3], [0])
    # Cooltime Section
    set_cool = Settings(ntSS, "Cooltime", 3, 0, 10, ["6", "7", "8", "9", "10", "11", "12", "13", "14", "0"], [5, 5], [0])
    # Idol Section
    set_idol = Settings(ntName, "Idol Name", 0, 0, 56, cur1.execute('select name from TypeStorage').fetchall(), [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [0])

    uil_root.mainloop()
