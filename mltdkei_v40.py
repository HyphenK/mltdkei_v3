# Python Module #
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from PIL import ImageTk, Image
from tkinter.font import Font
import sqlite3
import webbrowser
from io import BytesIO
from re import findall
from os import cpu_count
from urllib.request import urlopen
from time import time, sleep
from multiprocessing import Process, freeze_support, Manager
# mltdkei Module #
import AppealCalc
import SimulateCalc
import UpdateHub
import IdolList
import MakeUnit
# mltdkei_mainframe for ver.4.24 22/03/21

def multi_appeal(work_id, result, tclist, temp_splist, zST, difull, zLT, IDB_name, check, friend):
    temp_result = AppealCalc.appeal_calculator(tclist, temp_splist, zST, difull, zLT, work_id, IDB_name, check, friend)
    result.put(temp_result)
    return

def single_appeal(tclist, temp_splist, zST, difull, zLT, work_id, IDB_name, check, friend):
    temp_result = AppealCalc.appeal_calculator(tclist, temp_splist, zST, difull, zLT, work_id, IDB_name, check, friend)
    return temp_result

def multi_ideal(work_id, ntcalc, result, songinfo, songinfo_zSN, songinfo_zDI, IDB_name):
    temp_result = SimulateCalc.calculator(ntcalc, True, 1, songinfo, songinfo_zSN, songinfo_zDI, work_id, IDB_name)
    result.put(temp_result)
    return

def single_ideal(ntcalc, songinfo, songinfo_zSN, songinfo_zDI, work_id, IDB_name):
    temp_result = SimulateCalc.calculator(ntcalc, True, 1, songinfo, songinfo_zSN, songinfo_zDI, work_id, IDB_name)
    return temp_result

def multi_calculator(work_id, ntcalc, result, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB, IDB_name):
    temp_result = [(fair1[zOB], fair1, fair2) for fair1, fair2 in SimulateCalc.calculator(ntcalc, False, zTC, songinfo, songinfo_zSN, songinfo_zDI, work_id, IDB_name)]
    result.put(temp_result)
    return

def mltdkei_mainframe(IDB_name, MDB_name, info_name, SongDB_name, pypy):
    freeze_support()
    root = Tk()
    root.title("MLTD Deck Analyzer 4.24")
    root.geometry("+80+25")
    root.resizable(False, False)
    
    lb_loading = Label(root, text="Loading")
    lb_loading.grid(row=0, column=0, ipadx=10, ipady=10)
    
    def help_open():
        readme_url = 'https://github.com/HyphenK/mltdkei_v3'
        webbrowser.open(readme_url, new=1)
    
    version = "4.24"
    try:
        versioncheck = urlopen("https://raw.githubusercontent.com/HyphenK/mltdkei_v3/v40_main/version_check").read().decode('utf-8')
        versioncheck = findall('Version (.+)\n', versioncheck)[0]
        if version != versioncheck:
            response = msgbox.askyesno("Update Avaliable",
                f"""New version is avaliable.\nCurrent Version: {version}\nNew Version: {versioncheck}\nDo you want to update now?""")
            if response == 1: help_open()
    except:
        msgbox.showerror("Internet Required", "Internet Connection is required to run the program.")
        exit()

    lb_loading.destroy()
    conn1 = sqlite3.connect(IDB_name)
    cur1 = conn1.cursor()
    conn2 = sqlite3.connect(MDB_name)
    cur2 = conn2.cursor()
    if IDB_name == 'mltdkei_idoldata.sqlite': matsuri_storage = "https://storage.matsurihi.me/mltd/icon_l/"
    elif IDB_name == 'mltdkei_idoldata_kr.sqlite': matsuri_storage = "https://storage.matsurihi.me/mltd_ko/icon_l/"
    photodict, songdict, resultdict = dict(), dict(), dict()
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    font9b = Font(family="Arial", size=9, weight="bold")
    font10 = Font(family="Arial", size=10)
    font12 = Font(family="Arial", size=12)
    process_count = cpu_count()

    def iconext(code1, code2, size):
        try:
            pil_img = photodict[code1]
        except:
            try:
                image_url = matsuri_storage + code2
                my_page = urlopen(image_url)
                my_picture = BytesIO(my_page.read())
                pil_img = Image.open(my_picture)
                photodict[code1] = pil_img
            except:
                image_url = matsuri_storage + code2.replace("_1", "_0")
                my_page = urlopen(image_url)
                my_picture = BytesIO(my_page.read())
                pil_img = Image.open(my_picture)
                photodict[code1] = pil_img
        pil_img = pil_img.resize((size, size))
        photoinfo = ImageTk.PhotoImage(pil_img)
        return photoinfo

    ##### Definition for Extra Setting Window #####

    zCB, zIC, zSC, zTC = 20, 2000, 30, 1000
    zAH, zAR, zAS, zDC = 0, 0, 0, 0
    zMS = [0, 0]

    def extra_setting():
        try:
            infofile_sldm = open(info_name, 'r', encoding='utf-8')
            infodata_sldm = infofile_sldm.read().split('\n')
            infofile_sldm.close()
        except:
            msgbox.showinfo('Error', 'Info File is damaged or not updated.\nPlease check your file or update DB first.')
            return
        ext_root = Toplevel()
        ext_root.title("MLTD Deck Analyzer Advanced Setting")
        ext_root.geometry(f"+{80+main_width+1}+25")
        ext_root.resizable(False, False)

        total_all = dict()
        annis, total_anni = ("BRAND NEW PERFORMANCE", "UNI-ONAIR", "CHALLENGE FOR GLOW-RY DAYS", "Reach 4 the Dream"), list()
        
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
        cglist = [[0], cg_voup_n, cg_voup_ot, cg_voup_sb, cg_voup_3tn, cg_voup_3tup,
                  cg_daup_n, cg_daup_ot, cg_daup_sb, cg_daup_3tn, cg_daup_3tup,
                  cg_viup_n, cg_viup_ot, cg_viup_sb, cg_viup_3tn, cg_viup_3tup,
                  cg_allup, cg_lifeup, cg_actup, [101]]
        cgtext = ["All Skills", "Vocal-Normal", "Vocal-OneType", "Vocal-SongBonus", "Vocal-3Type", "Vocal-3Type+SkillAct",
                  "Dance-Normal", "Dance-OneType", "Dance-SongBonus", "Dance-3Type", "Dance-3Type+SkillAct",
                  "Visual-Normal", "Visual-OneType", "Visual-SongBonus", "Visual-3Type", "Visual-3Type+SkillAct",
                  "All-Normal", "LifeUp", "SkillAct", "NoSkill"]

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
        sklist = [[100], [10, 11], [20, 21], [30, 31], [14, 15, 24, 25], [12, 13], [22, 23], [34],
                  [1, 2, 3], [5], [6], [7], [0]]
        sktext = ["All Skills", "Score Up", "Combo Up", "Double Boost", "Multi Up", "OverClock", "OverRondo", "Double Effect",
                  "Perfect Support", "Damage Guard", "Life Plus", "Combo Support", "No Skill"]

        for idolinfo in infodata_sldm: # 1,N+,天海春香,0,0,1
            if idolinfo == '': continue
            idolinfo = idolinfo.split(',')
            if idolinfo[3] == '1':
                total_all[idolinfo[0]] = idolinfo[4]
            for anni in annis:
                if anni in idolinfo[2]:
                    total_anni.append(idolinfo[0])

        nonlocal zCB, zIC, zSC, zTC, zAH, zAR, zAS, zDC, zMS
        cbnlist = [IntVar() for i in range(6)]
        cbnlist[1].set(1)

        def save_thing(inputed, fromwhere):
            nonlocal zCB, zIC, zSC, zTC
            if inputed == "zCB":
                zCB = int(fromwhere.get())
            if inputed == "zIC":
                try: zIC = int(fromwhere.get())
                except: zIC = fromwhere.get()
            if inputed == "zSC":
                zSC = int(fromwhere.get())
            if inputed == "zTC":
                zTC = int(fromwhere.get())
            cbxPS.set("Manual")

        def save_zA(inputed, fromwhere, whereget):
            nonlocal zAH, zAR, zAS, zDC
            if inputed == "zAH": zAH = fromwhere.index(whereget.get())
            if inputed == "zAR": zAR = fromwhere.index(whereget.get())
            if inputed == "zAS": zAS = fromwhere.index(whereget.get())
            if inputed == "zDC": zDC = fromwhere.index(whereget.get())
            cbxPS.set("Manual")

        def apcalc2(data, have, mr, r):
            appeal = findall('[0-9]+', data)
            a1, a0 = int(appeal[1]), int(appeal[0])
            if have == 1: answer = a0 + int(r) * (a1 - a0) / int(mr)
            elif have == 0: answer = a1
            return int(answer)

        def set_leader_manual(inputed_list):
            nonlocal sldm_container
            lb_SLloading = Label(cv_extd, text="Now Loading...")
            lb_SLloading.place(x=0, y=75, width=568, height=50)

            sldm_container.destroy()
            sldm_container = Frame(ext_root)
            sldm_canvas = Canvas(sldm_container, width=550, height=400)
            scrollbar = Scrollbar(sldm_container, command=sldm_canvas.yview)
            scrollable_frame = Frame(sldm_canvas)

            scrollable_frame.bind("<Configure>", lambda e: sldm_canvas.configure(scrollregion=sldm_canvas.bbox("all")))

            sldm_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            sldm_canvas.configure(yscrollcommand=scrollbar.set)

            sldm_container.grid(row=2, column=0)
            sldm_canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            ext_root.update()
            rowcount = 0

            printgo = [i.get() for i in cbnlist[0:5]]
            printrank = list()
            if printgo[1] == 1: printrank.append("SSR+")
            if printgo[2] == 1: printrank.append("SR+")
            if printgo[3] == 1: printrank.append("R+")
            if printgo[4] == 1: printrank.append("N+")

            def set_leader_manual_print(inputed_infos, inputed_row):
                if cbnlist[5].get() == 1 and str(inputed_infos[0]) in total_anni:
                    pass
                else:
                    if inputed_infos[2] not in printrank: return
                    if str(inputed_infos[0]) in total_anni: return
                if printgo[0] == 1 and total_all.get(str(inputed_infos[0])) == None: return
                infoframe = Frame(scrollable_frame, width=550, height=50)
                infoframe.grid(row=inputed_row, column=0)
                photoinfo = iconext(int(inputed_infos[0]), inputed_infos[1], 48)
                lb_photoinfo = Label(infoframe, image=photoinfo)
                lb_photoinfo.image = photoinfo
                lb_photoinfo.place(x=0, y=0, width=50, height=50)
                
                btn_SLconfig = Button(infoframe, text="Select", command=lambda: NTlist[notebook.index('current')].load_target(inputed_infos))
                btn_SLconfig.place(x=50, y=0, width=49, height=24)

                lb_idolhave = Label(infoframe, text="--", borderwidth=2, relief="groove", bg="white")
                lb_idolhave.place(x=100, y=0, width=50, height=25)
                if total_all.get(str(inputed_infos[0])) != None: lb_idolhave.config(text="Have")

                lb_idolrare = Label(infoframe, text=inputed_infos[2], borderwidth=2, relief="groove", bg="white")
                lb_idolrare.place(x=150, y=0, width=50, height=25)

                lb_idolnumber = Label(infoframe, text="".join(["Max★", str(inputed_infos[3])]), borderwidth=2, relief="groove", bg="white")
                lb_idolnumber.place(x=200, y=0, width=50, height=25)

                idolinfo_text = " ".join(["Vo:", inputed_infos[4].replace(" ", ""), "Da:",
                    inputed_infos[5].replace(" ", ""), "Vi:", inputed_infos[6].replace(" ", "")])
                lb_idolinfo = Label(infoframe, text=idolinfo_text, borderwidth=2, relief="groove", bg="white")
                lb_idolinfo.place(x=250, y=0, width=300, height=25)
                
                lb_idolcenter = Label(infoframe, borderwidth=2, relief="groove", bg="white")
                lb_idolcenter.place(x=50, y=25, width=250, height=25)
                
                lb_idolskill = Label(infoframe, borderwidth=2, relief="groove", bg="white")
                lb_idolskill.place(x=300, y=25, width=250, height=25)
                
                for i in range(len(cglist)):
                    if inputed_infos[7] in cglist[i]:
                        lb_idolcenter.config(text=cgtext[i])
                        break
                for i in range(len(sklist)):
                    if inputed_infos[8] in sklist[i]:
                        lb_idolskill.config(text=sktext[i])
                        break

                ext_root.update()

            for infos in inputed_list: # idnumber, photocode, rare, maxrank, vocal, dance, visual, center
                set_leader_manual_print(infos, rowcount)
                rowcount = rowcount + 1

            lb_SLloading.destroy()
            ext_root.update()

        def set_leader():
            SL_cmd = ["""select idnumber, photocode, rare, maxrank, vocal, dance, visual, centerid, skillid
                from IdolDB natural inner join PhotoCodeDB natural inner join CenterDB natural inner join SkillDB
                natural inner join CenterStorage where """]
            if cbx_SLidol.get() != "All Idols": SL_cmd = SL_cmd + ['''name like "%''', cbx_SLidol.get(), '''" and ''']
            if cgtext.index(cbx_SLcenter.get()) == 0: cg = tuple([i for j in cglist for i in j])
            else: cg = tuple([0]+cglist[cgtext.index(cbx_SLcenter.get())])
            if sktext.index(cbx_SLskill.get()) == 0: sk = tuple([i for j in sklist for i in j])
            else: sk = tuple([100]+sklist[sktext.index(cbx_SLskill.get())])
            SL_cmd = SL_cmd + [f'''centerid in {cg} and skillid in {sk}''']
            SL = cur1.execute(''.join(SL_cmd)).fetchall()
            set_leader_manual(SL)

        cv_extu = Label(ext_root, borderwidth=2, relief="groove")
        cv_extu.grid(row=0, column=0)

        txCB = Label(cv_extu, text="Using Idols")
        txCB.grid(row=0, column=0, sticky=E+W)

        CBvalues = [10*i for i in range(2, 8)]
        cbxCB = ttk.Combobox(cv_extu, width=6, height=6, values=CBvalues, state="readonly")
        cbxCB.grid(row=0, column=1)
        cbxCB.set(zCB)
        cbxCB.bind("<<ComboboxSelected>>", lambda unused_option: save_thing("zCB", cbxCB))
        
        txIC = Label(cv_extu, text="Ideal Calc")
        txIC.grid(row=0, column=2, sticky=E+W)

        ICvalues = ["All", 1000, 2000, 3000, 5000, 10000, 20000, 30000, 50000, 100000]
        cbxIC = ttk.Combobox(cv_extu, width=6, height=10, values=ICvalues, state="readonly")
        cbxIC.grid(row=0, column=3)
        cbxIC.set(zIC)
        cbxIC.bind("<<ComboboxSelected>>", lambda unused_option: save_thing("zIC", cbxIC))

        txSC = Label(cv_extu, text="Score Calc")
        txSC.grid(row=0, column=4, sticky=E+W)

        SCvalues = [10, 20, 30, 50, 80, 100, 150, 200]
        cbxSC = ttk.Combobox(cv_extu, width=6, height=8, values=SCvalues, state="readonly")
        cbxSC.grid(row=0, column=5)
        cbxSC.set(zSC)
        cbxSC.bind("<<ComboboxSelected>>", lambda unused_option: save_thing("zSC", cbxSC))

        txTC = Label(cv_extu, text="Time of Calc")
        txTC.grid(row=0, column=6, sticky=E+W)

        TCvalues = [1000, 2000, 3000, 5000, 10000, 20000, 30000, 50000, 100000]
        cbxTC = ttk.Combobox(cv_extu, width=6, height=9, values=TCvalues, state="readonly")
        cbxTC.grid(row=0, column=7)
        cbxTC.set(zTC)
        cbxTC.bind("<<ComboboxSelected>>", lambda unused_option: save_thing("zTC", cbxTC))

        lb_AH = Label(cv_extu, text="All Idols")
        lb_AH.grid(row=1, column=0, sticky=E+W)

        AHvalues = ["Disable", "Enable"]
        cbx_AH = ttk.Combobox(cv_extu, width=6, height=2, values=AHvalues, state="readonly")
        cbx_AH.grid(row=1, column=1)
        cbx_AH.set(AHvalues[zAH])
        cbx_AH.bind("<<ComboboxSelected>>", lambda unused_option: save_zA("zAH", AHvalues, cbx_AH))

        lb_AR = Label(cv_extu, text=" All Star Rank ")
        lb_AR.grid(row=1, column=2, sticky=E+W)

        ARvalues = ["Default", "★0", "★MAX"]
        cbx_AR = ttk.Combobox(cv_extu, width=6, height=3, values=ARvalues, state="readonly")
        cbx_AR.grid(row=1, column=3)
        cbx_AR.set(ARvalues[zAR])
        cbx_AR.bind("<<ComboboxSelected>>", lambda unused_option: save_zA("zAR", ARvalues, cbx_AR))

        lb_AS = Label(cv_extu, text=" All Skill Level ")
        lb_AS.grid(row=1, column=4, sticky=E+W)

        ASvalues = ["Default", "Lv1", "LvMAX"]
        cbx_AS = ttk.Combobox(cv_extu, width=6, height=3, values=ASvalues, state="readonly")
        cbx_AS.grid(row=1, column=5)
        cbx_AS.set(ASvalues[zAS])
        cbx_AS.bind("<<ComboboxSelected>>", lambda unused_option: save_zA("zAS", ASvalues, cbx_AS))

        lb_SL = Label(cv_extu, text="Deep Calc")
        lb_SL.grid(row=1, column=6, sticky=E+W)

        DCvalues = ["Disable", "Enable"]
        cbx_DC = ttk.Combobox(cv_extu, width=6, height=2, values=DCvalues, state="readonly")
        cbx_DC.grid(row=1, column=7)
        cbx_DC.set(DCvalues[zDC])
        cbx_DC.bind("<<ComboboxSelected>>", lambda unused_option: save_zA("zDC", DCvalues, cbx_DC))
        
        cv_extd = Frame(ext_root, width=572, height=129, borderwidth=2, relief="groove")
        cv_extd.grid(row=1, column=0)
        
        ##### Notebook - Manual Selection Area #####
        
        notebook = ttk.Notebook(cv_extd)
        notebook.place(x=0, y=0, width=568, height=75)
        notebook.bind("<<NotebookTabChanged>>", lambda e: NTlist[notebook.index('current')].print_target())

        class NotebookFrame:
            def __init__(self, target):
                self.target = target
            
            def make_frame(self, name, notebook):
                self.NTframe = Frame(cv_extd)
                notebook.add(self.NTframe, text=f"         {name}         ")
                
                self.lb_SLphoto = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
                self.lb_SLphoto.place(x=0, y=0, width=50, height=50)

                self.btn_SLreset = Button(self.NTframe, text="Reset", command=self.reset_data)
                self.btn_SLreset.place(x=50, y=0, width=49, height=24)

                self.lb_SLhave = Label(self.NTframe, text="--", borderwidth=2, relief="groove", bg="white")
                self.lb_SLhave.place(x=100, y=0, width=50, height=25)

                self.lb_SLrare = Label(self.NTframe, text="--", borderwidth=2, relief="groove", bg="white")
                self.lb_SLrare.place(x=150, y=0, width=50, height=25)

                self.lb_SLnumber = Label(self.NTframe, text="--", borderwidth=2, relief="groove", bg="white")
                self.lb_SLnumber.place(x=200, y=0, width=50, height=25)

                self.lb_SLinfo = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
                self.lb_SLinfo.place(x=250, y=0, width=224, height=25)

                self.btn_up = Button(self.NTframe, text="▲", command=lambda: self.target_config(1))
                self.btn_up.place(x=474, y=0, width=30, height=25)

                self.btn_down = Button(self.NTframe, text="▼", command=lambda: self.target_config(-1))
                self.btn_down.place(x=504, y=0, width=30, height=25)

                self.btn_reset = Button(self.NTframe, text="R", command=lambda: self.target_config(0))
                self.btn_reset.place(x=534, y=0, width=30, height=25)

                self.lb_SLcg = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
                self.lb_SLcg.place(x=50, y=25, width=257, height=25)
                
                self.lb_SLsk = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
                self.lb_SLsk.place(x=307, y=25, width=257, height=25)

                self.print_target()
                
            def reset_data(self):
                self.target = 0
                self.lb_SLphoto.config(image='', borderwidth=2, relief="groove")
                self.lb_SLnumber.config(text="--")
                self.lb_SLrare.config(text='--')
                self.lb_SLinfo.config(text='')
                self.lb_SLhave.config(text="--")
                self.lb_SLcg.config(text='')
                self.lb_SLsk.config(text='')
                zMS[notebook.index('current')] = self.target
                ext_root.update()
                
            def print_target(self): # total, idnumber, idoltype, skill, vocal, dance, visual
                if self.target == 0: return
                info = cur1.execute(f'''select rare, photocode, centerid, skillid from IdolDB natural inner join PhotoCodeDB
                    natural inner join CenterDB natural inner join SkillDB natural inner join CenterStorage
                    where idnumber = {self.target[0][1]}''').fetchone()
                photoinfo = iconext(self.target[0][1], info[1], 48)
                self.lb_SLphoto.config(image=photoinfo, relief="flat")
                self.lb_SLphoto.image = photoinfo
                if self.target[1][2] == 1: self.lb_SLhave.config(text="Have")
                self.lb_SLnumber.config(text="".join(["★", str(self.target[1][1])]))
                self.lb_SLinfo.config(text=" ".join(["Vo:", str(self.target[0][4]),
                    "Da:", str(self.target[0][5]), "Vi:", str(self.target[0][6])]))
                self.lb_SLrare.config(text=info[0])
                cgid, skid = int(info[2]), int(info[3])
                for i in range(len(cglist)):
                    if cgid in cglist[i]:
                        self.lb_SLcg.config(text=cgtext[i])
                        break
                for i in range(len(sklist)):
                    if skid in sklist[i]:
                        self.lb_SLsk.config(text=sktext[i])
                        break
                zMS[notebook.index('current')] = self.target
                ext_root.update()
                
            def load_target(self, inputed_infos):
                leaderdata = cur1.execute(f'''select type, vocal, dance, visual, total, maxrank, maxlevel from IdolDB
                    natural inner join SkillDB where idnumber = "{inputed_infos[0]}"''').fetchone()
                idnumber, idoltype, maxrank, skill = str(inputed_infos[0]), int(leaderdata[0]), int(leaderdata[5]), int(leaderdata[6])
                try: haverank, have = total_all[idnumber], 1
                except: haverank, have = maxrank, 0
                vocal = apcalc2(leaderdata[1], have, maxrank, haverank)
                dance = apcalc2(leaderdata[2], have, maxrank, haverank)
                visual = apcalc2(leaderdata[3], have, maxrank, haverank)
                total = apcalc2(leaderdata[4], have, maxrank, haverank)
                self.target = [[total, idnumber, idoltype, skill, vocal, dance, visual], [maxrank, haverank, have], leaderdata[1:5]]
                self.print_target()
                
            def target_config(self, option):
                if self.target == 0: return
                maxrank, haverank, option = int(self.target[1][0]), int(self.target[1][1]), int(option)
                if option == 0: haverank = maxrank
                else: haverank = haverank + option
                if maxrank < haverank or haverank < 0: return
                vocal = apcalc2(self.target[2][0], 1, maxrank, haverank)
                dance = apcalc2(self.target[2][1], 1, maxrank, haverank)
                visual = apcalc2(self.target[2][2], 1, maxrank, haverank)
                total = apcalc2(self.target[2][3], 1, maxrank, haverank)
                self.target[0] = [total, self.target[0][1], self.target[0][2], self.target[0][3], vocal, dance, visual]
                self.target[1] = [maxrank, haverank, self.target[1][2]]
                self.print_target()
        
        NTframeL = NotebookFrame(zMS[0])
        NTframeL.make_frame("Leader", notebook)
        
        NTframeF = NotebookFrame(zMS[1])
        NTframeF.make_frame("Friend", notebook)
        
        NTlist = [NTframeL, NTframeF]
        
        cv_extop = Frame(cv_extd)
        cv_extop.place(x=0, y=75, width=568, height=50)
        
        cv_extl1 = Frame(cv_extop)
        cv_extl1.grid(row=0, column=0)
        
        lb_SLidol = Label(cv_extl1, text=" Idol Name ")
        lb_SLidol.grid(row=0, column=0, sticky=N+S)
        
        SL_idol = cur1.execute('select name from TypeStorage').fetchall()
        SLbyidol = ["All Idols"] + [SL_idol[i][0] for i in range(len(SL_idol))]
        cbx_SLidol = ttk.Combobox(cv_extl1, width=16, height=13, values=SLbyidol, state="readonly")
        cbx_SLidol.grid(row=0, column=1)
        cbx_SLidol.set("All Idols")

        lb_SLct = Label(cv_extl1, text=" Category ")
        lb_SLct.grid(row=0, column=2)
        
        cbntext = ["Have", "SSR", "SR", "R", "N", "Anniv."]
        for i in range(6):
            cbn = Checkbutton(cv_extl1, text=cbntext[i], variable=cbnlist[i])
            cbn.grid(row=0, column=i+3)
            
        cv_extl2 = Frame(cv_extop)
        cv_extl2.grid(row=1, column=0)

        lb_SLcenter = Label(cv_extl2, text=" Center Skill ")
        lb_SLcenter.grid(row=0, column=0, sticky=N+S)

        cbx_SLcenter = ttk.Combobox(cv_extl2, width=20, height=20, values=cgtext, state="readonly")
        cbx_SLcenter.grid(row=0, column=1)
        cbx_SLcenter.set("All Skills")
        
        lb_SLskill = Label(cv_extl2, text=" Idol Skill ")
        lb_SLskill.grid(row=0, column=2, sticky=N+S)

        cbx_SLskill = ttk.Combobox(cv_extl2, width=15, height=13, values=sktext, state="readonly")
        cbx_SLskill.grid(row=0, column=3)
        cbx_SLskill.set("All Skills")
        
        btn_load = Button(cv_extl2, text="Load Info", width=15, command=set_leader)
        btn_load.grid(row=0, column=4, padx=5)

        sldm_container = Frame(ext_root)
        sldm_container.grid(row=2, column=0)

    ##### Definition for mltdkei_main #####

    def open_setting():
        i1a = [cbxST, cbxDI, cbxSN, cbxLT, cbxDM, cbxDT, cbxOB, cbxPS]
        i1b = [bnRUN, bnEX, bnUD, bnUF]
        for j in i1a:
            j.config(state="readonly")
        for j in i1b:
            j.config(state="normal")
        root.update()

    def close_setting():
        i1 = [cbxST, cbxDI, cbxSN, cbxLT, cbxDM, cbxDT, cbxOB, cbxPS, bnRUN, bnEX, bnUD, bnUF]
        for j in i1:
            j.config(state="disabled")
        root.update()

    def mltdkei_main():
        start_time = time()
        close_setting()

        ##### Read Setting #####

        try:
            zST = STvalues.index(cbxST.get()) + 1
            try: zSN = cur2.execute(f"select songid from SongDB where {SongDB_name} = '{str(cbxSN.get())}'").fetchone()[0]
            except: zSN = cur2.execute(f'select songid from SongDB where {SongDB_name} = "{str(cbxSN.get())}"').fetchone()[0]
        except ValueError: # zST Error
            open_setting()
            cbxSN.config(state="disabled")
            root.update()
            msgbox.showwarning("Song Type Error", "Song Type is not selected.")
            return
        except TypeError: # zSN Error
            open_setting()
            msgbox.showwarning("Song Title Error", "Song Title is not selected.")
            return
        zDI = DIvalues.index(cbxDI.get()) + 1
        zLT = LTvalues.index(cbxLT.get())
        zDM = DMvalues.index(cbxDM.get())
        zDT = DTvalues.index(cbxDT.get())
        zOB = OBvalues.index(cbxOB.get())
        nonlocal zCB, zIC, zSC, zTC, zAH, zAR, zAS, zDC, zMS

        if zDI == 6 and zSN != 124:
            open_setting()
            msgbox.showwarning("Difficulty Error", "This difficulty is not compatible with the selected song.")
            return
        if zCB > 50 or zSC > 100 or zTC > 5000:
            response = msgbox.askokcancel("Warning",
                "Proceeding with this setting can be time consuming.\nDo you still want to proceed?")
            if response == 1:
                pass
            else:
                open_setting()
                return

        difull, hlall, hlpr, hlfa, hlan, iclist = dict(), list(), list(), list(), list(), list()

        ##### Make Havelist #####

        try:
            infofile_calc = open(info_name, 'r', encoding='utf-8')
            infodata_calc = infofile_calc.read().split('\n')
            infofile_calc.close()
        except:
            open_setting()
            msgbox.showinfo('Error', 'Info File is damaged or not updated.\nPlease check your file or update DB first.')
            return
        for line in infodata_calc:
            if len(line) == 0: continue
            line = line.split(',')
            if zAH == 0 and line[-3] == '0': continue
            idnumber = line[0]
            rank = int(line[-2])
            if zAS == 0: skill = int(line[-1])
            elif zAS == 1: skill = 1
            elif zAS == 2: skill = int(cur1.execute(f'select maxlevel from SkillDB where idnumber = {int(idnumber)}').fetchone()[0])
            dbdata = cur1.execute(f'select * from IdolDB where idnumber = {int(idnumber)}').fetchone()
            idoltype = int(dbdata[2])
            maxrank = int(dbdata[4])
            vocaldata, dancedata, visualdata, totaldata = dbdata[5:9]

            def apcalc(data, mr, r):
                nonlocal zAR
                appeal = findall('[0-9]+', data)
                a1, a0 = int(appeal[1]), int(appeal[0])
                if zAR == 0: answer = a0 + r * (a1 - a0) / mr
                elif zAR == 1: answer = a0
                elif zAR == 2: answer = a1
                return int(answer)

            vocal = apcalc(vocaldata, maxrank, rank)
            dance = apcalc(dancedata, maxrank, rank)
            visual = apcalc(visualdata, maxrank, rank)
            total = apcalc(totaldata, maxrank, rank)
            idoldata_full = total, idnumber, idoltype, skill, vocal, dance, visual
            idoldata_light = total, idnumber
            difull[idnumber] = idoldata_full
            hlall.append(idoldata_light)
            if idoltype == 1 or idoltype == 4: hlpr.append(idoldata_light)
            if idoltype == 2 or idoltype == 4: hlfa.append(idoldata_light)
            if idoltype == 3 or idoltype == 4: hlan.append(idoldata_light)

        hlall.sort(reverse=True)
        hlpr.sort(reverse=True)
        hlfa.sort(reverse=True)
        hlan.sort(reverse=True)

        if len(difull) < 15:
            open_setting()
            msgbox.showinfo('Error', 'You need at least 15 Idols to analyze.\nPlease check your file or update Idol List first.')
            return

        # Make Support
        temp_splist = list()
        for hidol in hlall:
            hidol = list(hidol)
            fidol = difull.get(hidol[1]) # total, idnumber, idoltype, skill, vocal, dance, visual
            if zST == fidol[2] or zST == 4 or fidol[2] == 4: hidol[0] = hidol[0] + int(hidol[0]*0.3)
            if zLT == 0: pass
            elif zLT == 1: hidol[0] = hidol[0] + int(fidol[4]*1.2)
            elif zLT == 2: hidol[0] = hidol[0] + int(fidol[5]*1.2)
            elif zLT == 3: hidol[0] = hidol[0] + int(fidol[6]*1.2)
            hidol = tuple(hidol)
            temp_splist.append(hidol)
        temp_splist.sort(reverse=True)
        
        zMSd = []
        for i in range(len(zMS)):
            try: zMSd.append(zMS[i][0])
            except: zMSd.append(0)

        tclist2 = MakeUnit.generate_deck(difull, hlall, hlpr, hlfa, hlan, zST, zDM, zDT, zCB, zMSd[0], zDC, IDB_name)
        tclen = len(tclist2)

        if len(tclist2[0]) == 0:
            open_setting()
            msgbox.showinfo('Error', '''Analyzer can't make any deck under this option.\nPlease check your Idol List or use higher "Using Idols" option.''')
            return

        process_make = process_count//2
        
        iclist2 = []
        for i in range(tclen):
            tclist = tclist2[i]
            iclist = []
            for check in [1, 0]:
                if pypy == 0:
                    tclist = [tclist[(i*len(tclist))//process_make:((i+1)*len(tclist))//process_make] for i in range(process_make)]
                    # Bug Appeared. Need to investigate deeper.
                    # Issue #2 - Error on second tclist when card is not enough to make deck
                    for i in range(len(tclist)):
                        if len(tclist[i]) == 1: tclist[i] = tclist[i][0]
                    # Temp Bug Fix Part End
                    tc_queue = Manager().Queue()
                    process_list = []
                    for i in range(process_make):
                        process = Process(target=multi_appeal, args=(i+1, tc_queue, tclist[i], temp_splist, zST, difull, zLT, IDB_name, check, zMSd[1]))
                        process_list.append(process)
                        process.start()
                    for process in process_list:
                        process.join()
                    qsize = tc_queue.qsize()
                    while qsize > 0:
                        iclist = iclist + tc_queue.get()
                        qsize = qsize - 1
                elif pypy == 1:
                    iclist = single_appeal(tclist, temp_splist, zST, difull, zLT, 1, IDB_name, check, zMSd[1])
                if len(iclist) != 0: break
            
            iclist.sort(reverse=True)
            if len(iclist) == 0: print("Warning: IC 0")
            if zIC != "All": iclist = iclist[0:zIC//tclen]
            iclist2.append(iclist)
        
        time_CDA = round(time() - start_time, 2)
        start_time_CIS = time()

        sclist2 = []
        songinfo = cur2.execute(f'select * from SongDB where songid = {zSN}').fetchone()
        songinfo_zSN = cur2.execute(f'select * from {songinfo[4]}').fetchall()[zDI-1]
        songinfo_zDI = cur2.execute(f'select abstime, track, type, bpm, duration, noteid from {songinfo[4] + str(zDI)}').fetchall()
        songinfo_zDI.sort()

        for i in range(tclen):
            iclist = iclist2[i]
            sclist = []
            if pypy == 0:
                iclist = [iclist[(i*len(iclist))//process_make:((i+1)*len(iclist))//process_make] for i in range(process_make)]
                ic_queue = Manager().Queue()
                process_list = []
                for i in range(process_make):
                    process = Process(target=multi_ideal, args=(i+1, iclist[i], ic_queue, songinfo, songinfo_zSN, songinfo_zDI, IDB_name))
                    process_list.append(process)
                    process.start()
                for process in process_list:
                    process.join()
                qsize = ic_queue.qsize()
                while qsize > 0:
                    sclist = sclist + ic_queue.get()
                    qsize = qsize - 1
            elif pypy == 1:
                sclist = single_ideal(iclist, songinfo, songinfo_zSN, songinfo_zDI, 1, IDB_name)
            
            sclist.sort(reverse=True)
            if len(sclist) == 0: print("Warning: SC 0")
            sclist2 = sclist2 + sclist[0:zSC//tclen]
        
        rslist = list()
        sclist = sclist2
        time_CIS = round(time() - start_time_CIS, 2)
        start_time_CS = time()

        sclist = [sclist[(i*len(sclist))//process_make:((i+1)*len(sclist))//process_make] for i in range(process_make)]
        sc_queue = Manager().Queue()
        process_list = []
        for i in range(process_make):
            process = Process(target=multi_calculator, args=(i+1, sclist[i], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB, IDB_name))
            process_list.append(process)
            process.start()
        for process in process_list:
            process.join()

        qsize = sc_queue.qsize()
        while qsize > 0:
            rslist = rslist + sc_queue.get()
            qsize = qsize - 1

        rslist.sort(reverse=True)
        time_CS = round(time() - start_time_CS, 2)
        calc_result = ((zSN, cbxST.get(), zDI, cbxLT.get(), cbxDM.get(), cbxDT.get(), cbxPS.get(), zOB), rslist)
        resultdict[notebook.index(notebook.select())] = calc_result

        open_setting()
        time_total = round(time() - start_time, 2)
        msgbox.showinfo("Analyze Complete",
            "".join(["Appeal Calc Runtime: ", str(time_CDA), "(sec)\n",
            "Ideal Calc Runtime: ", str(time_CIS), "(sec)\n",
            "Score Calc Runtime: ", str(time_CS), "(sec)\n",
            "Total Runtime: ", str(time_total), "(sec)"]))
        try:
            make_btn(1)
        except:
            pass

    ##### Display Definition Area #####

    def rearrange_data(number, order):
        need_to_rearrange = resultdict[number][1]
        for result_set in need_to_rearrange:
            arrange_set = list(result_set)
            arrange_set[0] = arrange_set[1][order]
            arrange_set = tuple(arrange_set)
            need_to_rearrange[need_to_rearrange.index(result_set)] = arrange_set
        need_to_rearrange.sort(reverse=True)
        frontdata = list(resultdict[number][0])
        frontdata[7] = order
        frontdata = tuple(frontdata)
        resultdict[number] = frontdata, need_to_rearrange
        make_btn(1)

    def make_btn(unused_option):
        nonlocal scrollable_frame1
        for widget in scrollable_frame1.winfo_children():
            widget.destroy()
        reset_display()
        try: calc_result = resultdict[notebook.index(notebook.select())]
        except: return
        whichnote = notebook.index(notebook.select())
        NTlist[whichnote].write_notebook(whichnote, calc_result[0])
        rslist = calc_result[1]
        def make_btn_one(in_i):
            nonlocal scrollable_frame1
            btn = Button(scrollable_frame1, text="Deck #"+str(in_i+1), width=9, command=lambda: print_display(rslist[in_i], in_i))
            btn.grid(row=in_i, column=0)
        for i in range(len(rslist)):
            make_btn_one(i)
        print_display(rslist[0], 0)

    def print_display_photo(inputed_label, inputed_info, size):
        photocode = cur1.execute(f'select photocode from PhotoCodeDB where idnumber = {inputed_info}').fetchone()
        photoinfo = iconext(int(inputed_info), photocode[0], size)
        inputed_label.config(image=photoinfo, borderwidth=0, relief="flat")
        inputed_label.image = photoinfo
        root.update()

    def print_display_dot(where):
        chlist = ["light gray" for i in range(len(lpplist))]
        if where != -1: chlist[where] = "blue"
        for i in range(len(lpplist)):
            lpplist[i].change_dot(chlist[i])

    def print_display(need_to_print, deckno):
        reset_display()
        result = need_to_print
        lpDKdeckno.config(text=f"<Deck #{deckno+1}>")
        lpDKtotalappeal.config(text=result[2][0])
        lpDKsortbyscore.config(text=result[0][0])
        lpDKsortby.config(text=OBvalues[result[1].index(result[0])])
        lpDKvocal.config(text=result[2][4])
        lpDKdance.config(text=result[2][5])
        lpDKvisual.config(text=result[2][6])
        for i in range(len(lpplist)):
            lpplist[i].change_print(result[1][i][0], result[1][i][1])
        print_display_dot(result[1].index(result[0]))
        root.update()
        for i in range(5):
            print_display_photo(lpDKlist[i], result[2][1][i][0], 73)
        print_display_photo(lpDKlist[5], result[2][2], 73)
        for i in range(10):
            print_display_photo(lpDKlist[i+6], result[2][3][i], 43)

    def reset_display():
        lpDKdeckno.config(text="<Deck #-->")
        lpDKtotalappeal.config(text="--")
        lpDKsortbyscore.config(text="--")
        lpDKsortby.config(text="-- Score:")
        lpDKvocal.config(text="--")
        lpDKdance.config(text="--")
        lpDKvisual.config(text="--")
        for lpp in lpplist:
            lpp.change_print("--", "--")
        print_display_dot(-1)
        for lpDK in lpDKlist:
            lpDK.config(image="", borderwidth=2, relief="groove")

    ##### Definition for Main GUI #####

    def update_lbPH(unused_option):
        nonlocal lbPH
        try: songphoto = str(cur2.execute(f"select songphoto from SongDB where {SongDB_name} = '{cbxSN.get()}'").fetchone()[0])
        except: songphoto = str(cur2.execute(f'select songphoto from SongDB where {SongDB_name} = "{cbxSN.get()}"').fetchone()[0])
        try:
            pil_img = songdict[int(songphoto)]
        except:
            image_url = "".join(["https://cdn.img-conv.gamerch.com/img.gamerch.com/imasml-theater-wiki/wikidb_thumbnail/",
                songphoto, "/main_sync_200.jpg"])
            my_page = urlopen(image_url)
            my_picture = BytesIO(my_page.read())
            pil_img = Image.open(my_picture)
            songdict[int(songphoto)] = pil_img
        pil_img = pil_img.resize((98, 98))
        photodata = ImageTk.PhotoImage(pil_img)
        lbPH.config(image=photodata, borderwidth=0, relief="flat")
        lbPH.image = photodata

    def update_cbxSN(unused_option):
        nonlocal cbxSN, SNvalues
        STlc = STvalues.index(cbxST.get()) + 1
        SNvalues = list()
        SNlist = cur2.execute(f'select {SongDB_name} from SongDB where type = {STlc}').fetchall()
        SNvalues = [SNlist[i][0] for i in range(0, len(SNlist))]
        cbxSN.config(values=SNvalues, state="readonly")
        cbxSN.set("Select Song Title")
        cbxSN.bind("<<ComboboxSelected>>", update_lbPH)
        root.update()

    def presets(unused_option):
        nonlocal zCB, zIC, zSC, zTC, zAH, zAR, zAS
        howto = cbxPS.get()
        if howto == "Manual":
            return
        elif howto == PSvalues[0]:
            zCB, zIC, zSC, zTC = 20, 2000, 30, 1000
            zAH, zAR, zAS = 0, 0, 0
        elif howto == PSvalues[1]:
            zCB, zIC, zSC, zTC = 30, 5000, 50, 2000
            zAH, zAR, zAS = 0, 0, 0
        elif howto == PSvalues[2]:
            zCB, zIC, zSC, zTC = 50, 10000, 50, 2000
            zAH, zAR, zAS = 0, 0, 0
        elif howto == PSvalues[3]:
            zCB, zIC, zSC, zTC = 50, 10000, 50, 2000
            zAH, zAR, zAS = 0, 2, 2
        elif howto == PSvalues[4]:
            zCB, zIC, zSC, zTC = 50, 10000, 50, 2000
            zAH, zAR, zAS = 1, 2, 2

    ##### Main GUI Area #####

    bbcvUP = Frame(root)
    bbcvUP.grid(row=0, column=0)

    bcvSE = Frame(bbcvUP, width=554, height=154, borderwidth=2, relief="groove", bg="white")
    bcvSE.grid(row=0, column=0)

    lbPH = Label(bcvSE, borderwidth=2, relief="groove", bg="white")
    lbPH.place(x=0, y=0, width=100, height=100)

    cvST = Frame(bcvSE)
    cvST.place(x=100, y=0, width=90, height=50)

    txST = Label(cvST, text="Song Type", borderwidth=2, relief="groove")
    txST.place(x=0, y=0, width=90, height=25)

    STvalues = ["Princess", "Fairy", "Angel", "All"]
    cbxST = ttk.Combobox(cvST, height=4, values=STvalues, state="readonly")
    cbxST.place(x=0, y=25, width=89, height=24)
    cbxST.set("Select")
    cbxST.bind("<<ComboboxSelected>>", update_cbxSN)

    cvDI = Frame(bcvSE)
    cvDI.place(x=100, y=50, width=90, height=50)

    txDI = Label(cvDI, text="Difficulty", borderwidth=2, relief="groove")
    txDI.place(x=0, y=0, width=90, height=25)

    DIvalues = ["2M", "2M+", "4M", "6M", "MM", "OM"]
    cbxDI = ttk.Combobox(cvDI, height=6, values=DIvalues, state="readonly")
    cbxDI.place(x=0, y=25, width=89, height=24)
    cbxDI.set("MM")

    cvSN = Frame(bcvSE)
    cvSN.place(x=190, y=0, width=360, height=50)

    txSN = Label(cvSN, text="Song Title", borderwidth=2, relief="groove")
    txSN.place(x=0, y=0, width=360, height=25)

    SNvalues = ["Select Song Type First"]
    cbxSN = ttk.Combobox(cvSN, height=10, values=SNvalues, state="disabled")
    cbxSN.place(x=0, y=25, width=359, height=24)
    cbxSN.set("Select Song Type First")

    cvLT = Frame(bcvSE)
    cvLT.place(x=190, y=50, width=90, height=50)

    txLT = Label(cvLT, text="Live Type", borderwidth=2, relief="groove")
    txLT.place(x=0, y=0, width=90, height=25)

    LTvalues = ["Normal", "Vo +120%", "Da +120%", "Vi +120%"]
    cbxLT = ttk.Combobox(cvLT, height=4, values=LTvalues, state="readonly")
    cbxLT.place(x=0, y=25, width=89, height=24)
    cbxLT.set("Normal")

    cvDM = Frame(bcvSE)
    cvDM.place(x=280, y=50, width=90, height=50)

    txDM = Label(cvDM, text="Deck Mode", borderwidth=2, relief="groove")
    txDM.place(x=0, y=0, width=90, height=25)

    DMvalues = ["ST+3T", "All(Legacy)", "Songtype", "3Type", "Princess", "Fairy", "Angel"]
    cbxDM = ttk.Combobox(cvDM, height=7, values=DMvalues, state="readonly")
    cbxDM.place(x=0, y=25, width=89, height=24)
    cbxDM.set("ST+3T")

    cvDT = Frame(bcvSE)
    cvDT.place(x=370, y=50, width=90, height=50)

    txDT = Label(cvDT, text="Deck Type", borderwidth=2, relief="groove")
    txDT.place(x=0, y=0, width=90, height=25)

    DTvalues = ["All", "Vocal", "Dance", "Visual"]
    cbxDT = ttk.Combobox(cvDT, height=4, values=DTvalues, state="readonly")
    cbxDT.place(x=0, y=25, width=89, height=24)
    cbxDT.set("All")

    cvOB = Frame(bcvSE)
    cvOB.place(x=460, y=50, width=90, height=50)

    txOB = Label(cvOB, text="Order By", borderwidth=2, relief="groove")
    txOB.place(x=0, y=0, width=90, height=25)

    lpptext = ["Ideal", "Best", "0.1%", "0.5%", "1%", "2%", "5%", "10%", "20%", "50%"]
    OBvalues = [i+" Score" for i in lpptext]
    cbxOB = ttk.Combobox(cvOB, height=10, values=OBvalues, state="readonly")
    cbxOB.place(x=0, y=25, width=89, height=24)
    cbxOB.set("10% Score")

    cvRUN = Frame(bcvSE)
    cvRUN.place(x=0, y=100, width=190, height=50)

    bnRUN = Button(cvRUN, text="Start Analyzer", command=mltdkei_main)
    bnRUN.place(x=0, y=0, width=145, height=50)

    bnHELP = Button(cvRUN, text="Help", command=help_open)
    bnHELP.place(x=145, y=0, width=45, height=50)

    cvEX = Frame(bcvSE)
    cvEX.place(x=190, y=100, width=180, height=50)

    txPS = Label(cvEX, text="Presets", borderwidth=2, relief="groove")
    txPS.place(x=0, y=0, width=90, height=25)

    PSvalues = ["Beginner", "Intermediate", "Ranker", "All Max", "Theoretical"]
    cbxPS = ttk.Combobox(cvEX, height=5, values=PSvalues, state="readonly")
    cbxPS.place(x=0, y=25, width=89, height=24)
    cbxPS.set("Beginner")
    cbxPS.bind("<<ComboboxSelected>>", presets)

    bnEX = Button(cvEX, text="Advanced\nSetting", command=extra_setting)
    bnEX.place(x=90, y=0, width=90, height=50)

    cvUT = Frame(bcvSE)
    cvUT.place(x=370, y=100, width=180, height=50)

    bnUD = Button(cvUT, text="Update DB", command=lambda: UpdateHub.main_hub(IDB_name, MDB_name, info_name))
    bnUD.place(x=0, y=0, width=90, height=50)

    bnUF = Button(cvUT, text="Config\nIdol List", command=lambda: IdolList.main_idollist(iconext, IDB_name, info_name))
    bnUF.place(x=90, y=0, width=90, height=50)

    ##### Notebook Area #####

    bbcvDN = Frame(root, borderwidth=2, relief="groove")
    bbcvDN.grid(row=1, column=0)

    notebook = ttk.Notebook(bbcvDN, width=546, height=50)
    notebook.grid(row=0, column=0, columnspan=2)
    notebook.bind("<<NotebookTabChanged>>", make_btn)

    class NotebookFrame:
        def make_frame(self, cv, notebook, tabno):
            self.NTframe = Frame(cv)
            notebook.add(self.NTframe, text=f"    Tab #{tabno+1}    ")

            self.f_lbPH = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
            self.f_lbPH.place(x=0, y=0, width=50, height=50)

            self.f_lbSN = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
            self.f_lbSN.place(x=50, y=0, width=350, height=25)

            self.f_lbST = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
            self.f_lbST.place(x=400, y=0, width=146, height=25)

            self.f_lbLT = Label(self.NTframe, borderwidth=2, relief="groove", bg="white")
            self.f_lbLT.place(x=50, y=25, width=300, height=25)

            self.f_lbOB = Label(self.NTframe, text="Rearrange By:")
            self.f_lbOB.place(x=350, y=25, width=90, height=25)

            self.f_cbxOB = ttk.Combobox(self.NTframe, height=10, values=OBvalues, state="disabled")
            self.f_cbxOB.place(x=440, y=25, width=105, height=24)

        def write_notebook(self, number, data):
            zSN_data = cur2.execute(f'select * from SongDB where songid = {data[0]}').fetchone()
            SNtext, PHtext = zSN_data[2:4]
            try:
                pil_img = songdict[int(PHtext)]
            except:
                image_url = "".join(["https://cdn.img-conv.gamerch.com/img.gamerch.com/imasml-theater-wiki/wikidb_thumbnail/",
                    PHtext, "/main_sync_200.jpg"])
                my_page = urlopen(image_url)
                my_picture = BytesIO(my_page.read())
                pil_img = Image.open(my_picture)
                songdict[int(PHtext)] = pil_img
                sleep(0.2)
            pil_img = pil_img.resize((48, 48))
            photoinfo = ImageTk.PhotoImage(pil_img)
            self.f_lbPH.config(image=photoinfo, borderwidth=0, relief="flat")
            self.f_lbPH.image = photoinfo
            self.f_lbSN.config(text=SNtext)
            self.f_lbST.config(text=f"{data[1]} / {DIvalues[data[2]-1]}({zSN_data[data[2]+5]})")
            self.f_lbLT.config(text=" / ".join(data[3:7]))
            self.f_cbxOB.config(state="readonly")
            self.f_cbxOB.set(OBvalues[data[7]])
            self.f_cbxOB.bind("<<ComboboxSelected>>", lambda unused_option: rearrange_data(number, OBvalues.index(self.f_cbxOB.get())))

    NTlist = []
    
    for i in range(7):
        NTframe = NotebookFrame()
        NTframe.make_frame(bbcvDN, notebook, i)
        NTlist.append(NTframe)

    ##### Left Button Area #####

    cvYK = Frame(bbcvDN, width=86, height=270, borderwidth=2, relief="groove", bg="white")
    cvYK.grid(row=1, column=0)

    ykbn_container = Frame(cvYK)
    ykbn_canvas = Canvas(ykbn_container, width=70, height=286)
    scrollbar = Scrollbar(ykbn_container, command=ykbn_canvas.yview)
    scrollable_frame1 = Frame(ykbn_canvas)

    scrollable_frame1.bind("<Configure>", lambda e: ykbn_canvas.configure(scrollregion=ykbn_canvas.bbox("all")))

    ykbn_canvas.create_window((0, 0), window=scrollable_frame1, anchor="nw")
    ykbn_canvas.configure(yscrollcommand=scrollbar.set)

    ykbn_container.grid(row=0, column=1, rowspan=3)
    ykbn_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ##### Result Print Area #####

    cvDK = Frame(bbcvDN, width=454, height=294, borderwidth=2, relief="groove", bg="white")
    cvDK.grid(row=1, column=1)

    lpDKdeckno = Label(cvDK, text="<Deck -->", font=font10)
    lpDKdeckno.place(x=0, y=0, width=150, height=25)

    lpDKtotalapl = Label(cvDK, text="Total Appeal:", anchor='e', font=font9b)
    lpDKtotalapl.place(x=150, y=0, width=80, height=25)

    lpDKtotalappeal = Label(cvDK, text="--", anchor='w', font=font12)
    lpDKtotalappeal.place(x=230, y=0, width=70, height=25)

    lpDKsortby = Label(cvDK, text="-- Score:", anchor='e', font=font9b)
    lpDKsortby.place(x=300, y=0, width=75, height=25)

    lpDKsortbyscore = Label(cvDK, text="--", anchor='w', font=font12)
    lpDKsortbyscore.place(x=375, y=0, width=75, height=25)

    lpDKvo = Label(cvDK, text="Vocal:", anchor='e', font=font9b)
    lpDKvo.place(x=0, y=25, width=45, height=25)

    lpDKvocal = Label(cvDK, text="--", anchor='w', font=font10)
    lpDKvocal.place(x=45, y=25, width=105, height=25)

    lpDKda = Label(cvDK, text="Dance:", anchor='e', font=font9b)
    lpDKda.place(x=150, y=25, width=45, height=25)

    lpDKdance = Label(cvDK, text="--", anchor='w', font=font10)
    lpDKdance.place(x=195, y=25, width=105, height=25)

    lpDKvi = Label(cvDK, text="Visual:", anchor='e', font=font9b)
    lpDKvi.place(x=300, y=25, width=45, height=25)

    lpDKvisual = Label(cvDK, text="--", anchor='w', font=font10)
    lpDKvisual.place(x=345, y=25, width=105, height=25)

    cviDK = Frame(cvDK, width=450, height=120)
    cviDK.place(x=0, y=50)
    
    lpDKlist = []
    lpDKx1, lpDKx2 = -75, -45
    
    for i in [75 for j in range(6)]:
        lpDKx1 += i
        lpDKdeck = Label(cviDK, borderwidth=2, relief="groove", bg="white")
        lpDKdeck.place(x=lpDKx1, y=0, width=i, height=i)
        lpDKlist.append(lpDKdeck)
        
    for i in [45 for j in range(10)]:
        lpDKx2 += i
        lpDKdeck = Label(cviDK, borderwidth=2, relief="groove", bg="white")
        lpDKdeck.place(x=lpDKx2, y=75, width=i, height=i)
        lpDKlist.append(lpDKdeck)
        
    lpDKlist[0].config(text="Leader")
    lpDKlist[5].config(text="Friend")

    class PrintScore:
        def place_first(self, framename, text1, x1, y1):
            self.lpDKf = Frame(framename)
            self.lpDKf.place(x=x1, y=y1, width=225, height=20)

            self.lpDKb = Label(self.lpDKf, borderwidth=2, relief="groove", bg="light gray")
            self.lpDKb.place(x=5, y=5, width=10, height=10)

            self.lpDK = Label(self.lpDKf, text=text1, font=font9b)
            self.lpDK.place(x=20, y=0, width=55, height=20)

            self.lpDKscore = Label(self.lpDKf, font=font10)
            self.lpDKscore.place(x=75, y=0, width=75, height=20)

            self.lpDKbefore = Label(self.lpDKf, font=font10)
            self.lpDKbefore.place(x=150, y=0, width=75, height=20)

        def change_print(self, score, before):
            self.lpDKscore.config(text=score)
            self.lpDKbefore.config(text=before)

        def change_dot(self, which):
            self.lpDKb.config(bg=which)

    cvDKd = Frame(cvDK, width=450, height=120)
    cvDKd.place(x=0, y=170)

    lpscore1 = Label(cvDKd, text="Total", font=font9b)
    lpscore1.place(x=75, y=0, width=75, height=20)

    lpbefore1 = Label(cvDKd, text="Before S.A", font=font9b)
    lpbefore1.place(x=150, y=0, width=75, height=20)

    lpscore2 = Label(cvDKd, text="Total", font=font9b)
    lpscore2.place(x=300, y=0, width=75, height=20)

    lpbefore2 = Label(cvDKd, text="Before S.A", font=font9b)
    lpbefore2.place(x=375, y=0, width=75, height=20)
    
    lpplist = []
    lppy = [20, 40, 60, 80, 100]
    
    for i in range(5):
        lpp = PrintScore()
        lpp.place_first(cvDKd, lpptext[i], 0, lppy[i])
        lpplist.append(lpp)
        
    for i in range(5):
        lpp = PrintScore()
        lpp.place_first(cvDKd, lpptext[i+5], 225, lppy[i])
        lpplist.append(lpp)

    root.update()
    main_width = root.winfo_width()
    root.mainloop()
