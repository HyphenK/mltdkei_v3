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
import UpdateHubE
import IdolList
import MakeUnit

conn1 = sqlite3.connect('mltdkei_idoldata.sqlite')
cur1 = conn1.cursor()
conn2 = sqlite3.connect('mltdkei_songdata.sqlite')
cur2 = conn2.cursor()

def multi_appeal(work_id, result, tclist, temp_splist, zST, difull, zLT):
    temp_result = AppealCalc.appeal_calculator(tclist, temp_splist, zST, difull, zLT, work_id)
    result.put(temp_result)
    return

def multi_ideal(work_id, ntcalc, result, songinfo, songinfo_zSN, songinfo_zDI):
    temp_result = SimulateCalc.calculator(ntcalc, True, 1, songinfo, songinfo_zSN, songinfo_zDI, work_id)
    result.put(temp_result)
    return

def multi_calculator(work_id, ntcalc, result, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB):
    temp_result = [(fair1[zOB], fair1, fair2) for fair1, fair2 in SimulateCalc.calculator(ntcalc, False, zTC, songinfo, songinfo_zSN, songinfo_zDI, work_id)]
    result.put(temp_result)
    return

if __name__ == '__main__':
    root = Tk()
    root.title("MLTD Deck Analyzer 3.0")
    freeze_support()

    matsuri_url = "https://mltd.matsurihi.me/cards/"
    matsuri_storage = "https://storage.matsurihi.me/mltd/icon_l/"
    github_url = "https://raw.githubusercontent.com/HyphenK/mltdkei_v3/main/"
    photodict, songdict, resultdict = dict(), dict(), dict()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
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
    zSL1, zSL2, zAH, zAR, zAS = 0, 0, 0, 0, 0

    def extra_setting():
        try:
            infofile_sldm = open('mltdkei_info.txt', 'r', encoding='utf-8')
            infodata_sldm = infofile_sldm.read().split('\n')
            infofile_sldm.close()
        except:
            msgbox.showinfo('Error', 'Info File is damaged or not updated.\nPlease check your file or update DB first.')
            return
        ext_root = Toplevel()
        ext_root.title("MLTD Deck Analyzer Advanced Setting")
        ext_root.geometry("+60+25")
        ext_root.resizable(False, False)

        total_all = dict()
        annis, total_anni = ("BRAND NEW PERFORMANCE", "UNI-ONAIR", "CHALLENGE FOR GLOW-RY DAYS"), list()

        for idolinfo in infodata_sldm: # 1,N+,天海春香,0,0,1
            if idolinfo == '': continue
            idolinfo = idolinfo.split(',')
            if idolinfo[3] == '1':
                total_all[idolinfo[0]] = idolinfo[4]
            for anni in annis:
                if anni in idolinfo[2]:
                    total_anni.append(idolinfo[0])

        global zCB, zIC, zSC, zTC
        global zSL1, zSL2, zAH, zAR, zAS
        cbnhave, cbnssr, cbnsr, cbnr, cbnn, cbnanni = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
        cbnssr.set(1)

        def save_thing(inputed, fromwhere):
            inputed = int(fromwhere.get())
            cbxPS.set("Manual")

        def save_zA(inputed, fromwhere, whereget):
            inputed = fromwhere.index(whereget.get())
            cbxPS.set("Manual")

        def save_zSL1(unused_option):
            global zSL1
            zSL1 = SLvalues.index(cbx_SL.get())
            if zSL1 == 0:
                cbx_SLidol.config(state="disabled")
                cbx_SLcenter.config(state="disabled")
            elif zSL1 == 1:
                cbx_SLidol.config(state="readonly")
                cbx_SLcenter.config(state="readonly")
            cbxPS.set("Manual")
            ext_root.update()

        def apcalc2(data, have, mr, r):
            appeal = findall('[0-9]+', data)
            a1, a0 = int(appeal[1]), int(appeal[0])
            if have == 1: answer = a0 + int(r) * (a1 - a0) / int(mr)
            elif have == 0: answer = a1
            return int(answer)

        def print_center(inputed_zSL2): # total, idnumber, idoltype, skill, vocal, dance, visual
            info = cur1.execute(f'''select rare, photocode, center from IdolDB natural inner join PhotoCodeDB
                natural inner join CenterDB natural inner join CenterStorage where idnumber = {inputed_zSL2[0][1]}''').fetchone()
            photoinfo = iconext(inputed_zSL2[0][1], info[1], 48)
            lb_SLphoto.config(image=photoinfo)
            lb_SLphoto.image = photoinfo
            if inputed_zSL2[1][2] == 1: lb_SLhave.config(text="Have")
            lb_SLnumber.config(text="".join(["★", str(inputed_zSL2[1][1])]))
            lb_SLinfo.config(text=" ".join(["Vo:", str(inputed_zSL2[0][4]),
                "Da:", str(inputed_zSL2[0][5]), "Vi:", str(inputed_zSL2[0][6])]))
            lb_SLrare.config(text=info[0])
            lb_SLcenteri.config(text=info[2])
            ext_root.update()

        def set_leader_manual(inputed_list):
            lb_SLloading = Label(cv_extd, text="Now Loading...")
            lb_SLloading.place(x=0, y=50, width=568, height=75)

            try: sldm_container.destroy()
            except: pass
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

            printgo = cbnhave.get(), cbnssr.get(), cbnsr.get(), cbnr.get(), cbnn.get()
            printrank = list()
            if printgo[1] == 1: printrank.append("SSR+")
            if printgo[2] == 1: printrank.append("SR+")
            if printgo[3] == 1: printrank.append("R+")
            if printgo[4] == 1: printrank.append("N+")

            def set_leader_manual_print(inputed_infos, inputed_row):
                if cbnanni.get() == 1 and str(inputed_infos[0]) in total_anni:
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

                def save_zSL2():
                    global zSL2
                    leaderdata = cur1.execute(f'''select type, vocal, dance, visual, total, maxrank, maxlevel from IdolDB
                        natural inner join SkillDB where idnumber = "{inputed_infos[0]}"''').fetchone()
                    idnumber, idoltype, maxrank, skill = str(inputed_infos[0]), int(leaderdata[0]), int(leaderdata[5]), int(leaderdata[6])
                    try:
                        haverank = total_all[idnumber]
                        have = 1
                    except:
                        haverank = maxrank
                        have = 0
                    vocal = apcalc2(leaderdata[1], have, maxrank, haverank)
                    dance = apcalc2(leaderdata[2], have, maxrank, haverank)
                    visual = apcalc2(leaderdata[3], have, maxrank, haverank)
                    total = apcalc2(leaderdata[4], have, maxrank, haverank)
                    zSL2 = [[total, idnumber, idoltype, skill, vocal, dance, visual], [maxrank, haverank, have], leaderdata[1:5]]
                    print_center(zSL2)

                btn_SLconfig = Button(infoframe, text="Select", command=save_zSL2)
                btn_SLconfig.place(x=50, y=0, width=49, height=24)

                lb_idolhave = Label(infoframe, text="--", borderwidth=2, relief="groove", bg="white")
                lb_idolhave.place(x=100, y=0, width=50, height=25)
                if total_all.get(str(inputed_infos[0])) != None: lb_idolhave.config(text="Have")

                lb_idolrare = Label(infoframe, text=inputed_infos[2], borderwidth=2, relief="groove", bg="white")
                lb_idolrare.place(x=150, y=0, width=50, height=25)

                lb_idolnumber = Label(infoframe, text="".join(["Max★", str(inputed_infos[3])]), borderwidth=2, relief="groove", bg="white")
                lb_idolnumber.place(x=200, y=0, width=50, height=25)

                idolinfo_text = " ".join(["Vo:", inputed_infos[4].replace(" ", ""), "Da:", inputed_infos[5].replace(" ", ""), "Vi:", inputed_infos[6].replace(" ", "")])
                lb_idolinfo = Label(infoframe, text=idolinfo_text, borderwidth=2, relief="groove", bg="white")
                lb_idolinfo.place(x=250, y=0, width=300, height=25)

                lb_idolcenter = Label(infoframe, text=inputed_infos[7], borderwidth=2, relief="groove", bg="white")
                lb_idolcenter.place(x=50, y=25, width=500, height=25)

                ext_root.update()

            for infos in inputed_list: # idnumber, photocode, rare, maxrank, vocal, dance, visual, center
                set_leader_manual_print(infos, rowcount)
                rowcount = rowcount + 1

            lb_SLloading.destroy()
            ext_root.update()

        def set_leader_byidol(unused_option):
            SLbyidollist = cur1.execute(f'''select idnumber, photocode, rare, maxrank, vocal, dance, visual, center
                from IdolDB natural inner join PhotoCodeDB natural inner join CenterDB
                natural inner join CenterStorage where name like "%{cbx_SLidol.get()}"''').fetchall()
            set_leader_manual(SLbyidollist)

        def set_leader_bycenter(unused_option):
            SLbycenterlist = cur1.execute(f'''select idnumber, photocode, rare, maxrank, vocal, dance, visual, center
            from IdolDB natural inner join PhotoCodeDB natural inner join CenterDB
                natural inner join CenterStorage where center = "{cbx_SLcenter.get()}"''').fetchall()
            set_leader_manual(SLbycenterlist)

        def leader_reset():
            global zSL2
            zSL2 = 0
            lb_SLphoto.config(image='')
            lb_SLnumber.config(text="--")
            lb_SLrare.config(text='--')
            lb_SLinfo.config(text='')
            lb_SLhave.config(text="--")
            lb_SLcenteri.config(text='')
            ext_root.update()

        def leader_config(option):
            global zSL2
            if zSL2 == 0: return
            maxrank, haverank, option = int(zSL2[1][0]), int(zSL2[1][1]), int(option)
            if option == 0: haverank = maxrank
            else: haverank = haverank + option
            if maxrank < haverank or haverank < 0: return
            vocal = apcalc2(zSL2[2][0], 1, maxrank, haverank)
            dance = apcalc2(zSL2[2][1], 1, maxrank, haverank)
            visual = apcalc2(zSL2[2][2], 1, maxrank, haverank)
            total = apcalc2(zSL2[2][3], 1, maxrank, haverank)
            zSL2[0] = [total, zSL2[0][1], zSL2[0][2], zSL2[0][3], vocal, dance, visual]
            zSL2[1] = [maxrank, haverank, zSL2[1][2]]
            print_center(zSL2)

        cv_extu = Label(ext_root, borderwidth=2, relief="groove")
        cv_extu.grid(row=0, column=0)

        txCB = Label(cv_extu, text="Combination")
        txCB.grid(row=0, column=0, sticky=E+W)

        txIC = Label(cv_extu, text="Ideal Calc")
        txIC.grid(row=0, column=1, sticky=E+W)

        txSC = Label(cv_extu, text="Score Calc")
        txSC.grid(row=0, column=2, sticky=E+W)

        txTC = Label(cv_extu, text="Time of Calc")
        txTC.grid(row=0, column=3, sticky=E+W)

        CBvalues = [5*i for i in range(2, 16)]
        cbxCB = ttk.Combobox(cv_extu, width=17, height=9, values=CBvalues, state="readonly")
        cbxCB.grid(row=1, column=0)
        cbxCB.set(zCB)
        cbxCB.bind("<<ComboboxSelected>>", lambda unused_option: save_thing(zCB, CBvalues))

        ICvalues = [500*i for i in range(1, 21)]
        cbxIC = ttk.Combobox(cv_extu, width=17, height=10, values=ICvalues, state="readonly")
        cbxIC.grid(row=1, column=1)
        cbxIC.set(zIC)
        cbxIC.bind("<<ComboboxSelected>>", lambda unused_option: save_thing(zIC, ICvalues))

        SCvalues = [5*i for i in range(2, 21)]
        cbxSC = ttk.Combobox(cv_extu, width=17, height=10, values=SCvalues, state="readonly")
        cbxSC.grid(row=1, column=2)
        cbxSC.set(zSC)
        cbxSC.bind("<<ComboboxSelected>>", lambda unused_option: save_thing(zSC, SCvalues))

        TCvalues = [500*i for i in range(1, 11)]
        cbxTC = ttk.Combobox(cv_extu, width=17, height=10, values=TCvalues, state="readonly")
        cbxTC.grid(row=1, column=3)
        cbxTC.set(zTC)
        cbxTC.bind("<<ComboboxSelected>>", lambda unused_option: save_thing(zTC, TCvalues))

        lb_AH = Label(cv_extu, text="Calc With All Idol")
        lb_AH.grid(row=2, column=0, sticky=E+W)

        lb_AR = Label(cv_extu, text="Set Star Rank as")
        lb_AR.grid(row=2, column=1, sticky=E+W)

        lb_AS = Label(cv_extu, text="Set Skill Level as")
        lb_AS.grid(row=2, column=2, sticky=E+W)

        lb_SL = Label(cv_extu, text="Manual Leader Select")
        lb_SL.grid(row=2, column=3, sticky=E+W)

        AHvalues = ["Disable", "Enable"]
        cbx_AH = ttk.Combobox(cv_extu, width=17, height=2, values=AHvalues, state="readonly")
        cbx_AH.grid(row=3, column=0)
        cbx_AH.set(AHvalues[zAH])
        cbx_AH.bind("<<ComboboxSelected>>", lambda unused_option: save_zA(zAH, AHvalues, cbx_AH))

        ARvalues = ["Default", "★0", "★MAX"]
        cbx_AR = ttk.Combobox(cv_extu, width=17, height=3, values=ARvalues, state="readonly")
        cbx_AR.grid(row=3, column=1)
        cbx_AR.set(ARvalues[zAR])
        cbx_AR.bind("<<ComboboxSelected>>", lambda unused_option: save_zA(zAR, ARvalues, cbx_AR))

        ASvalues = ["Default", "Lv1", "LvMAX"]
        cbx_AS = ttk.Combobox(cv_extu, width=17, height=3, values=ASvalues, state="readonly")
        cbx_AS.grid(row=3, column=2)
        cbx_AS.set(ASvalues[zAS])
        cbx_AS.bind("<<ComboboxSelected>>", lambda unused_option: save_zA(zAS, ASvalues, cbx_AS))

        SLvalues = ["Disable", "Enable"]
        cbx_SL = ttk.Combobox(cv_extu, width=17, height=2, values=SLvalues, state="readonly")
        cbx_SL.grid(row=3, column=3)
        cbx_SL.set(SLvalues[zSL1])
        cbx_SL.bind("<<ComboboxSelected>>", save_zSL1)

        cv_extd = Frame(ext_root, width=572, height=129, borderwidth=2, relief="groove")
        cv_extd.grid(row=1, column=0)

        lb_SLphoto = Label(cv_extd, borderwidth=2, relief="groove", bg="white")
        lb_SLphoto.place(x=0, y=0, width=50, height=50)

        btn_SLreset = Button(cv_extd, text="Reset", command=leader_reset)
        btn_SLreset.place(x=50, y=0, width=49, height=24)

        lb_SLhave = Label(cv_extd, text="--", borderwidth=2, relief="groove", bg="white")
        lb_SLhave.place(x=100, y=0, width=50, height=25)

        lb_SLrare = Label(cv_extd, text="--", borderwidth=2, relief="groove", bg="white")
        lb_SLrare.place(x=150, y=0, width=50, height=25)

        lb_SLnumber = Label(cv_extd, text="--", borderwidth=2, relief="groove", bg="white")
        lb_SLnumber.place(x=200, y=0, width=50, height=25)

        lb_SLinfo = Label(cv_extd, borderwidth=2, relief="groove", bg="white")
        lb_SLinfo.place(x=250, y=0, width=228, height=25)

        btn_up = Button(cv_extd, text="▲", command=lambda: leader_config(1))
        btn_up.place(x=478, y=0, width=30, height=25)

        btn_down = Button(cv_extd, text="▼", command=lambda: leader_config(-1))
        btn_down.place(x=508, y=0, width=30, height=25)

        btn_reset = Button(cv_extd, text="R", command=lambda: leader_config(0))
        btn_reset.place(x=538, y=0, width=30, height=25)

        lb_SLcenteri = Label(cv_extd, borderwidth=2, relief="groove", bg="white")
        lb_SLcenteri.place(x=50, y=25, width=518, height=25)

        if zSL2 != 0: print_center(zSL2)

        lb_SLoption = Label(cv_extd, text="Option")
        lb_SLoption.place(x=0, y=50, width=110, height=25)

        cv_cbn = Frame(cv_extd)
        cv_cbn.place(x=110, y=50, width=458, height=25)

        cbn_have = Checkbutton(cv_cbn, text="Have", variable=cbnhave)
        cbn_have.grid(row=0, column=0)

        cbn_ssr = Checkbutton(cv_cbn, text="SSR", variable=cbnssr)
        cbn_ssr.grid(row=0, column=1)

        cbn_sr = Checkbutton(cv_cbn, text="SR", variable=cbnsr)
        cbn_sr.grid(row=0, column=2)

        cbn_r = Checkbutton(cv_cbn, text="R", variable=cbnr)
        cbn_r.grid(row=0, column=3)

        cbn_n = Checkbutton(cv_cbn, text="N", variable=cbnn)
        cbn_n.grid(row=0, column=4)

        cbn_anni = Checkbutton(cv_cbn, text="Anniversary", variable=cbnanni)
        cbn_anni.grid(row=0, column=5)

        lb_SLidol = Label(cv_extd, text="Select by Idol")
        lb_SLidol.place(x=0, y=75, width=110, height=25)

        lb_SLcenter = Label(cv_extd, text="Select by Center Skill")
        lb_SLcenter.place(x=110, y=75, width=458, height=25)

        SL_idol = cur1.execute('select name from TypeStorage').fetchall()
        SLbyidol = [SL_idol[i][0] for i in range(0, len(SL_idol))]
        cbx_SLidol = ttk.Combobox(cv_extd, height=13, values=SLbyidol, state="readonly")
        if zSL1 == 0: cbx_SLidol.config(state="disabled")
        cbx_SLidol.place(x=0, y=100, width=109, height=24)
        cbx_SLidol.set("Select")
        cbx_SLidol.bind("<<ComboboxSelected>>", set_leader_byidol)

        SL_center = cur1.execute('select center from CenterStorage').fetchall()
        SLbycenter = [SL_center[i][0] for i in range(0, len(SL_center))]
        cbx_SLcenter = ttk.Combobox(cv_extd, height=13, values=SLbycenter, state="readonly")
        if zSL1 == 0: cbx_SLcenter.config(state="disabled")
        cbx_SLcenter.place(x=110, y=100, width=457, height=24)
        cbx_SLcenter.set("Select")
        cbx_SLcenter.bind("<<ComboboxSelected>>", set_leader_bycenter)

    ##### Definition for mltdkei_main #####

    def open_setting():
        cbxST.config(state="readonly")
        cbxDI.config(state="readonly")
        cbxSN.config(state="readonly")
        cbxLT.config(state="readonly")
        cbxDM.config(state="readonly")
        cbxDT.config(state="readonly")
        cbxOB.config(state="readonly")
        cbxPS.config(state="readonly")
        bnRUN.config(state="normal")
        bnEX.config(state="normal")
        bnUD.config(state="normal")
        bnUF.config(state="normal")
        root.update()

    def close_setting():
        cbxST.config(state="disabled")
        cbxDI.config(state="disabled")
        cbxSN.config(state="disabled")
        cbxLT.config(state="disabled")
        cbxDM.config(state="disabled")
        cbxDT.config(state="disabled")
        cbxOB.config(state="disabled")
        cbxPS.config(state="disabled")
        bnRUN.config(state="disabled")
        bnEX.config(state="disabled")
        bnUD.config(state="disabled")
        bnUF.config(state="disabled")
        root.update()

    def mltdkei_main():
        start_time = time()
        close_setting()

        ##### Read Setting #####

        try:
            zST = STvalues.index(cbxST.get()) + 1
            zSN = cur2.execute('''select songid from SongDB
                where name_jp = "%s"''' % str(cbxSN.get())).fetchone()[0]
        except ValueError: # zST Error
            open_setting()
            cbxSN.config(state="disabled")
            msgbox.showwarning("Song Type Error", "Song Type is not selected.")
            root.update()
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
        global zCB, zIC, zSC, zTC
        global zSL1, zSL2, zAH, zAR, zAS

        if zDI == 6 and zSN != 124:
            open_setting()
            msgbox.showwarning("Difficulty Error", "This difficulty is not compatible with the selected song.")
            return
        if zCB > 40 or zSC > 100 or zTC > 3000:
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
            infofile_calc = open('mltdkei_info.txt', 'r', encoding='utf-8')
            infodata_calc = infofile_calc.read().split('\n')
            infofile_calc.close()
        except:
            open_setting()
            msgbox.showinfo('Error', 'Info File is damaged or not updated.\nPlease check your file or update DB first.')
            return
        for line in infodata_calc:
            if len(line) == 0: continue
            line = line.split(',')
            if zAH == 0 and line[3] == '0': continue
            idnumber = line[0]
            rank = int(line[4])
            if zAS == 0: skill = int(line[5])
            elif zAS == 1: skill = 1
            elif zAS == 2: skill = int(cur1.execute(f'select maxlevel from SkillDB where idnumber = {int(idnumber)}').fetchone()[0])
            dbdata = cur1.execute(f'select * from IdolDB where idnumber = {int(idnumber)}').fetchone()
            idoltype = int(dbdata[2])
            maxrank = int(dbdata[4])
            vocaldata, dancedata, visualdata, totaldata = dbdata[5:9]

            def apcalc(data, mr, r):
                global zAR
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
            if zLT == 0: pass
            elif zLT == 1: hidol[0] = hidol[0] + int(fidol[4]*1.2)
            elif zLT == 2: hidol[0] = hidol[0] + int(fidol[5]*1.2)
            elif zLT == 3: hidol[0] = hidol[0] + int(fidol[6]*1.2)
            if zST == fidol[2] or zST == 4: hidol[0] = hidol[0] + int(hidol[0]*0.3)
            hidol = tuple(hidol)
            temp_splist.append(hidol)
        temp_splist.sort(reverse=True)

        tclist = MakeUnit.generate_deck(difull, hlall, hlpr, hlfa, hlan, zST, zDM, zDT, zCB, zSL1, zSL2)

        if len(tclist) == 0:
            open_setting()
            msgbox.showinfo('Error', '''Analyzer can't make any deck under this option.\nPlease check your file or update Idol List first.''')
            return

        process_make = process_count//2
        if process_make > 10:
            process_make = 10

        tclist = [tclist[(i*len(tclist))//process_make:((i+1)*len(tclist))//process_make] for i in range(process_make)]
        tc_queue = Manager().Queue()
        process1 = Process(target=multi_appeal, args=(1, tc_queue, tclist[0], temp_splist, zST, difull, zLT))
        if process_make >= 2: process2 = Process(target=multi_appeal, args=(2, tc_queue, tclist[1], temp_splist, zST, difull, zLT))
        if process_make >= 3: process3 = Process(target=multi_appeal, args=(3, tc_queue, tclist[2], temp_splist, zST, difull, zLT))
        if process_make >= 4: process4 = Process(target=multi_appeal, args=(4, tc_queue, tclist[3], temp_splist, zST, difull, zLT))
        if process_make >= 5: process5 = Process(target=multi_appeal, args=(5, tc_queue, tclist[4], temp_splist, zST, difull, zLT))
        if process_make >= 6: process6 = Process(target=multi_appeal, args=(6, tc_queue, tclist[5], temp_splist, zST, difull, zLT))
        if process_make >= 7: process7 = Process(target=multi_appeal, args=(7, tc_queue, tclist[6], temp_splist, zST, difull, zLT))
        if process_make >= 8: process8 = Process(target=multi_appeal, args=(8, tc_queue, tclist[7], temp_splist, zST, difull, zLT))
        if process_make >= 9: process9 = Process(target=multi_appeal, args=(9, tc_queue, tclist[8], temp_splist, zST, difull, zLT))
        if process_make >= 10: process10 = Process(target=multi_appeal, args=(10, tc_queue, tclist[9], temp_splist, zST, difull, zLT))
        try:
            process1.start()
            process2.start()
            process3.start()
            process4.start()
            process5.start()
            process6.start()
            process7.start()
            process8.start()
            process9.start()
            process10.start()
        except:
            pass
        try:
            process1.join()
            process2.join()
            process3.join()
            process4.join()
            process5.join()
            process6.join()
            process7.join()
            process8.join()
            process9.join()
            process10.join()
        except:
            pass

        qsize = tc_queue.qsize()
        while qsize > 0:
            iclist = iclist + tc_queue.get()
            qsize = qsize - 1

        iclist.sort(reverse=True)
        iclist = iclist[0:zIC]
        time_CDA = round(time() - start_time, 2)
        start_time_CIS = time()

        sclist = list()
        songinfo = cur2.execute(f'select * from SongDB where songid = {zSN}').fetchone()
        songinfo_zSN = cur2.execute(f'select * from {songinfo[4]}').fetchall()[zDI-1]
        songinfo_zDI = cur2.execute(f'select abstime, track, type, bpm, duration from {songinfo[4] + str(zDI)}').fetchall()
        songinfo_zDI.sort()

        iclist = [iclist[(i*len(iclist))//process_make:((i+1)*len(iclist))//process_make] for i in range(process_make)]
        ic_queue = Manager().Queue()
        process1 = Process(target=multi_ideal, args=(1, iclist[0], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 2: process2 = Process(target=multi_ideal, args=(2, iclist[1], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 3: process3 = Process(target=multi_ideal, args=(3, iclist[2], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 4: process4 = Process(target=multi_ideal, args=(4, iclist[3], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 5: process5 = Process(target=multi_ideal, args=(5, iclist[4], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 6: process6 = Process(target=multi_ideal, args=(6, iclist[5], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 7: process7 = Process(target=multi_ideal, args=(7, iclist[6], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 8: process8 = Process(target=multi_ideal, args=(8, iclist[7], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 9: process9 = Process(target=multi_ideal, args=(9, iclist[8], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        if process_make >= 10: process10 = Process(target=multi_ideal, args=(10, iclist[9], ic_queue, songinfo, songinfo_zSN, songinfo_zDI))
        try:
            process1.start()
            process2.start()
            process3.start()
            process4.start()
            process5.start()
            process6.start()
            process7.start()
            process8.start()
            process9.start()
            process10.start()
        except:
            pass
        try:
            process1.join()
            process2.join()
            process3.join()
            process4.join()
            process5.join()
            process6.join()
            process7.join()
            process8.join()
            process9.join()
            process10.join()
        except:
            pass

        qsize = ic_queue.qsize()
        while qsize > 0:
            sclist = sclist + ic_queue.get()
            qsize = qsize - 1

        sclist.sort(reverse=True)
        sclist = sclist[0:zSC]
        rslist = list()
        time_CIS = round(time() - start_time_CIS, 2)
        start_time_CS = time()

        sclist = [sclist[(i*len(sclist))//process_make:((i+1)*len(sclist))//process_make] for i in range(process_make)]
        sc_queue = Manager().Queue()
        process1 = Process(target=multi_calculator, args=(1, sclist[0], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 2: process2 = Process(target=multi_calculator, args=(2, sclist[1], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 3: process3 = Process(target=multi_calculator, args=(3, sclist[2], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 4: process4 = Process(target=multi_calculator, args=(4, sclist[3], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 5: process5 = Process(target=multi_calculator, args=(5, sclist[4], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 6: process6 = Process(target=multi_calculator, args=(6, sclist[5], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 7: process7 = Process(target=multi_calculator, args=(7, sclist[6], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 8: process8 = Process(target=multi_calculator, args=(8, sclist[7], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 9: process9 = Process(target=multi_calculator, args=(9, sclist[8], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        if process_make >= 10: process10 = Process(target=multi_calculator, args=(10, sclist[9], sc_queue, songinfo, songinfo_zSN, songinfo_zDI, zTC, zOB))
        try:
            process1.start()
            process2.start()
            process3.start()
            process4.start()
            process5.start()
            process6.start()
            process7.start()
            process8.start()
            process9.start()
            process10.start()
        except:
            pass
        try:
            process1.join()
            process2.join()
            process3.join()
            process4.join()
            process5.join()
            process6.join()
            process7.join()
            process8.join()
            process9.join()
            process10.join()
        except:
            pass

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
        global scrollable_frame1
        for widget in scrollable_frame1.winfo_children():
            widget.destroy()
        root.update()
        reset_display()
        try: calc_result = resultdict[notebook.index(notebook.select())]
        except: return
        whichnote = notebook.index(notebook.select())
        if whichnote == 0: NTframe0.write_notebook(whichnote, calc_result[0])
        elif whichnote == 1: NTframe1.write_notebook(whichnote, calc_result[0])
        elif whichnote == 2: NTframe2.write_notebook(whichnote, calc_result[0])
        elif whichnote == 3: NTframe3.write_notebook(whichnote, calc_result[0])
        elif whichnote == 4: NTframe4.write_notebook(whichnote, calc_result[0])
        elif whichnote == 5: NTframe5.write_notebook(whichnote, calc_result[0])
        elif whichnote == 6: NTframe6.write_notebook(whichnote, calc_result[0])
        rslist = calc_result[1]
        def make_btn_one(in_i):
            global scrollable_frame1
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
        chlist = ["light gray" for i in range(8)]
        if where != -1: chlist[where] = "blue"
        lpideal.change_dot(chlist[0])
        lppoint.change_dot(chlist[1])
        lp1p.change_dot(chlist[2])
        lp2p.change_dot(chlist[3])
        lp5p.change_dot(chlist[4])
        lp10p.change_dot(chlist[5])
        lp20p.change_dot(chlist[6])
        lp50p.change_dot(chlist[7])
        root.update()

    def print_display(need_to_print, deckno):
        result = need_to_print
        lpDKdeckno.config(text=f"<Deck #{deckno+1}>")
        lpDKtotalappeal.config(text=result[2][0])
        lpDKsortbyscore.config(text=result[0][0])
        lpDKsortby.config(text=OBvalues[result[1].index(result[0])])
        lpDKvocal.config(text=result[2][4])
        lpDKdance.config(text=result[2][5])
        lpDKvisual.config(text=result[2][6])
        lpideal.change_print(result[1][0][0], result[1][0][1])
        lppoint.change_print(result[1][1][0], result[1][1][1])
        lp1p.change_print(result[1][2][0], result[1][2][1])
        lp2p.change_print(result[1][3][0], result[1][3][1])
        lp5p.change_print(result[1][4][0], result[1][4][1])
        lp10p.change_print(result[1][5][0], result[1][5][1])
        lp20p.change_print(result[1][6][0], result[1][6][1])
        lp50p.change_print(result[1][7][0], result[1][7][1])
        print_display_dot(result[1].index(result[0]))
        lpDKdeck0.config(image="", borderwidth=2, relief="groove")
        lpDKdeck1.config(image="", borderwidth=2, relief="groove")
        lpDKdeck2.config(image="", borderwidth=2, relief="groove")
        lpDKdeck3.config(image="", borderwidth=2, relief="groove")
        lpDKdeck4.config(image="", borderwidth=2, relief="groove")
        lpDKdeck5.config(image="", borderwidth=2, relief="groove")
        lpDKdeck6.config(image="", borderwidth=2, relief="groove")
        lpDKdeck7.config(image="", borderwidth=2, relief="groove")
        lpDKdeck8.config(image="", borderwidth=2, relief="groove")
        lpDKdeck9.config(image="", borderwidth=2, relief="groove")
        lpDKdeck10.config(image="", borderwidth=2, relief="groove")
        lpDKdeck11.config(image="", borderwidth=2, relief="groove")
        lpDKdeck12.config(image="", borderwidth=2, relief="groove")
        lpDKdeck13.config(image="", borderwidth=2, relief="groove")
        lpDKdeck14.config(image="", borderwidth=2, relief="groove")
        lpDKdeck15.config(image="", borderwidth=2, relief="groove")
        root.update()
        print_display_photo(lpDKdeck0, result[2][1][0][0], 73)
        print_display_photo(lpDKdeck1, result[2][1][1][0], 73)
        print_display_photo(lpDKdeck2, result[2][1][2][0], 73)
        print_display_photo(lpDKdeck3, result[2][1][3][0], 73)
        print_display_photo(lpDKdeck4, result[2][1][4][0], 73)
        print_display_photo(lpDKdeck5, result[2][2], 73)
        print_display_photo(lpDKdeck6, result[2][3][0], 43)
        print_display_photo(lpDKdeck7, result[2][3][1], 43)
        print_display_photo(lpDKdeck8, result[2][3][2], 43)
        print_display_photo(lpDKdeck9, result[2][3][3], 43)
        print_display_photo(lpDKdeck10, result[2][3][4], 43)
        print_display_photo(lpDKdeck11, result[2][3][5], 43)
        print_display_photo(lpDKdeck12, result[2][3][6], 43)
        print_display_photo(lpDKdeck13, result[2][3][7], 43)
        print_display_photo(lpDKdeck14, result[2][3][8], 43)
        print_display_photo(lpDKdeck15, result[2][3][9], 43)

    def reset_display():
        lpDKdeckno.config(text="<Deck #-->")
        lpDKtotalappeal.config(text="--")
        lpDKsortbyscore.config(text="--")
        lpDKsortby.config(text="-- Score:")
        lpDKvocal.config(text="--")
        lpDKdance.config(text="--")
        lpDKvisual.config(text="--")
        lpideal.change_print("--", "--")
        lppoint.change_print("--", "--")
        lp1p.change_print("--", "--")
        lp2p.change_print("--", "--")
        lp5p.change_print("--", "--")
        lp10p.change_print("--", "--")
        lp20p.change_print("--", "--")
        lp50p.change_print("--", "--")
        print_display_dot(-1)
        lpDKdeck0.config(image="", borderwidth=2, relief="groove")
        lpDKdeck1.config(image="", borderwidth=2, relief="groove")
        lpDKdeck2.config(image="", borderwidth=2, relief="groove")
        lpDKdeck3.config(image="", borderwidth=2, relief="groove")
        lpDKdeck4.config(image="", borderwidth=2, relief="groove")
        lpDKdeck5.config(image="", borderwidth=2, relief="groove")
        lpDKdeck6.config(image="", borderwidth=2, relief="groove")
        lpDKdeck7.config(image="", borderwidth=2, relief="groove")
        lpDKdeck8.config(image="", borderwidth=2, relief="groove")
        lpDKdeck9.config(image="", borderwidth=2, relief="groove")
        lpDKdeck10.config(image="", borderwidth=2, relief="groove")
        lpDKdeck11.config(image="", borderwidth=2, relief="groove")
        lpDKdeck12.config(image="", borderwidth=2, relief="groove")
        lpDKdeck13.config(image="", borderwidth=2, relief="groove")
        lpDKdeck14.config(image="", borderwidth=2, relief="groove")
        lpDKdeck15.config(image="", borderwidth=2, relief="groove")
        root.update()

    ##### Definition for Main GUI #####

    def update_lbPH(unused_option):
        global lbPH
        songphoto = str(cur2.execute(f'''select songphoto from SongDB where name_jp="{cbxSN.get()}"''').fetchone()[0])
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
        global cbxSN, SNvalues
        STlc = STvalues.index(cbxST.get()) + 1
        SNvalues = list()
        SNlist = cur2.execute(f'select name_jp from SongDB where type={STlc}').fetchall()
        SNvalues = [SNlist[i][0] for i in range(0, len(SNlist))]
        cbxSN.config(values=SNvalues, state="readonly")
        cbxSN.set("Select Song Title")
        cbxSN.bind("<<ComboboxSelected>>", update_lbPH)
        root.update()

    def help_open():
        readme_url = 'https://github.com/HyphenK/mltdkei/blob/main/README.md'
        webbrowser.open(readme_url, new=1)

    def presets(unused_option):
        global zCB, zIC, zSC, zTC
        global zAH, zAR, zAS
        howto = cbxPS.get()
        if howto == "Manual":
            return
        elif howto == PSvalues[0]:
            zCB, zIC, zSC, zTC = 20, 2000, 30, 1000
            zAH, zAR, zAS = 0, 0, 0
        elif howto == PSvalues[1]:
            zCB, zIC, zSC, zTC = 10, 500, 10, 500
            zAH, zAR, zAS = 0, 0, 0
        elif howto == PSvalues[2]:
            zCB, zIC, zSC, zTC = 30, 5000, 50, 2000
            zAH, zAR, zAS = 0, 0, 0
        elif howto == PSvalues[3]:
            zCB, zIC, zSC, zTC = 30, 5000, 50, 2000
            zAH, zAR, zAS = 0, 2, 2
        elif howto == PSvalues[4]:
            zCB, zIC, zSC, zTC = 30, 5000, 50, 2000
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

    DMvalues = ["All", "Songtype", "3Type", "Princess", "Fairy", "Angel", "Princess+", "Fairy+", "Angel+", "All+"]
    cbxDM = ttk.Combobox(cvDM, height=6, values=DMvalues, state="readonly")
    cbxDM.place(x=0, y=25, width=89, height=24)
    cbxDM.set("All")

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

    OBvalues = ["Ideal Score", "0.1% Score", "1% Score", "2% Score", "5% Score", "10% Score", "20% Score", "50% Score"]
    cbxOB = ttk.Combobox(cvOB, height=8, values=OBvalues, state="readonly")
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

    PSvalues = ["Default", "Light", "Accurate", "All Max", "Theoretical"]
    cbxPS = ttk.Combobox(cvEX, height=5, values=PSvalues, state="readonly")
    cbxPS.place(x=0, y=25, width=89, height=24)
    cbxPS.set("Default")
    cbxPS.bind("<<ComboboxSelected>>", presets)

    bnEX = Button(cvEX, text="Advanced\nSetting", command=extra_setting)
    bnEX.place(x=90, y=0, width=90, height=50)

    cvUT = Frame(bcvSE)
    cvUT.place(x=370, y=100, width=180, height=50)

    bnUD = Button(cvUT, text="Update DB", command=UpdateHubE.main_hub)
    bnUD.place(x=0, y=0, width=90, height=50)

    bnUF = Button(cvUT, text="Config\nIdol List", command=lambda: IdolList.main_idollist(iconext))
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

            self.f_cbxOB = ttk.Combobox(self.NTframe, height=8, values=OBvalues, state="disabled")
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
            root.update()

    NTframe0 = NotebookFrame()
    NTframe0.make_frame(bbcvDN, notebook, 0)

    NTframe1 = NotebookFrame()
    NTframe1.make_frame(bbcvDN, notebook, 1)

    NTframe2 = NotebookFrame()
    NTframe2.make_frame(bbcvDN, notebook, 2)

    NTframe3 = NotebookFrame()
    NTframe3.make_frame(bbcvDN, notebook, 3)

    NTframe4 = NotebookFrame()
    NTframe4.make_frame(bbcvDN, notebook, 4)

    NTframe5 = NotebookFrame()
    NTframe5.make_frame(bbcvDN, notebook, 5)

    NTframe6 = NotebookFrame()
    NTframe6.make_frame(bbcvDN, notebook, 6)

    ##### Left Button Area #####

    cvYK = Frame(bbcvDN, width=86, height=270, borderwidth=2, relief="groove", bg="white")
    cvYK.grid(row=1, column=0)

    ykbn_container = Frame(cvYK)
    ykbn_canvas = Canvas(ykbn_container, width=70, height=266)
    scrollbar = Scrollbar(ykbn_container, command=ykbn_canvas.yview)
    scrollable_frame1 = Frame(ykbn_canvas)

    scrollable_frame1.bind("<Configure>", lambda e: ykbn_canvas.configure(scrollregion=ykbn_canvas.bbox("all")))

    ykbn_canvas.create_window((0, 0), window=scrollable_frame1, anchor="nw")
    ykbn_canvas.configure(yscrollcommand=scrollbar.set)

    ykbn_container.grid(row=0, column=1, rowspan=3)
    ykbn_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ##### Result Print Area #####

    cvDK = Frame(bbcvDN, width=454, height=274, borderwidth=2, relief="groove", bg="white")
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

    lpDKdeck0 = Label(cviDK, text="Leader", borderwidth=2, relief="groove", bg="white")
    lpDKdeck0.place(x=0, y=0, width=75, height=75)

    lpDKdeck1 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck1.place(x=75, y=0, width=75, height=75)

    lpDKdeck2 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck2.place(x=150, y=0, width=75, height=75)

    lpDKdeck3 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck3.place(x=225, y=0, width=75, height=75)

    lpDKdeck4 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck4.place(x=300, y=0, width=75, height=75)

    lpDKdeck5 = Label(cviDK, text="Friend", borderwidth=2, relief="groove", bg="white")
    lpDKdeck5.place(x=375, y=0, width=75, height=75)

    lpDKdeck6 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck6.place(x=0, y=75, width=45, height=45)

    lpDKdeck7 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck7.place(x=45, y=75, width=45, height=45)

    lpDKdeck8 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck8.place(x=90, y=75, width=45, height=45)

    lpDKdeck9 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck9.place(x=135, y=75, width=45, height=45)

    lpDKdeck10 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck10.place(x=180, y=75, width=45, height=45)

    lpDKdeck11 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck11.place(x=225, y=75, width=45, height=45)

    lpDKdeck12 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck12.place(x=270, y=75, width=45, height=45)

    lpDKdeck13 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck13.place(x=315, y=75, width=45, height=45)

    lpDKdeck14 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck14.place(x=360, y=75, width=45, height=45)

    lpDKdeck15 = Label(cviDK, borderwidth=2, relief="groove", bg="white")
    lpDKdeck15.place(x=405, y=75, width=45, height=45)

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
            root.update()

        def change_dot(self, which):
            self.lpDKb.config(bg=which)

    cvDKd = Frame(cvDK, width=450, height=100)
    cvDKd.place(x=0, y=170)

    lpscore1 = Label(cvDKd, text="Total", font=font9b)
    lpscore1.place(x=75, y=0, width=75, height=20)

    lpbefore1 = Label(cvDKd, text="Before S.A", font=font9b)
    lpbefore1.place(x=150, y=0, width=75, height=20)

    lpscore2 = Label(cvDKd, text="Total", font=font9b)
    lpscore2.place(x=300, y=0, width=75, height=20)

    lpbefore2 = Label(cvDKd, text="Before S.A", font=font9b)
    lpbefore2.place(x=375, y=0, width=75, height=20)

    lpideal = PrintScore()
    lpideal.place_first(cvDKd, "Ideal", 0, 20)

    lppoint = PrintScore()
    lppoint.place_first(cvDKd, "0.1%", 0, 40)

    lp1p = PrintScore()
    lp1p.place_first(cvDKd, "1%", 0, 60)

    lp2p = PrintScore()
    lp2p.place_first(cvDKd, "2%", 0, 80)

    lp5p = PrintScore()
    lp5p.place_first(cvDKd, "5%", 225, 20)

    lp10p = PrintScore()
    lp10p.place_first(cvDKd, "10%", 225, 40)

    lp20p = PrintScore()
    lp20p.place_first(cvDKd, "20%", 225, 60)

    lp50p = PrintScore()
    lp50p.place_first(cvDKd, "50%", 225, 80)

    version = "3.0"
    versioncheck = urlopen(github_url+"version_check").read().decode('utf-8')
    versioncheck = findall('Version (.+)\n', versioncheck)[0]
    if version != versioncheck: msgbox.showinfo("Update Avaliable",
        f"New version is avaliable.\nCurrent Version: {version}\nNew Version: {versioncheck}")

    root.mainloop()
