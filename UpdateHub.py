# Python Module #
from tkinter import *
import tkinter.ttk as ttk
import requests
import sqlite3
from bs4 import BeautifulSoup
from re import findall
from os.path import getmtime
from urllib.request import urlopen
from time import sleep, strftime, localtime
# UpdateHub for above ver.3.95 21/07/02
# This program uses data from matsurihi.me for making idoldata database.
# The file update may be delayed since it is done manually. Please wait until it is made.

def update_info(cls_name, IDB_name, info_name, matsuri_url):
    conn1 = sqlite3.connect(IDB_name)
    cur1 = conn1.cursor()
    namedict, extract_end = dict(), list()

    webdata = urlopen(matsuri_url)
    soup = BeautifulSoup(webdata, 'html.parser')
    soupdata = soup.find_all("a", class_="card-select")
    for i in soupdata:
        extract_end.append(str(i['href']))
    extract_end.sort(reverse=True)
    extract_end = int(extract_end[0].split('/')[-1]) + 1

    cur1.execute('select idnumber from IdolDB order by idnumber asc')
    if IDB_name == 'mltdkei_idoldata.sqlite': end_of_db = int(cur1.fetchall()[-1][0])
    elif IDB_name == 'mltdkei_idoldata_kr.sqlite': end_of_db = int(cur1.fetchall()[-4][0])

    try:
        infofile = open(info_name, 'r', encoding='utf-8')
        infodata = infofile.read().split('\n')[:-1]
        infofile.close()
        txt_last = int(infodata[-1].split(',')[0]) + 1
    except:
        infodata = []
        txt_last = 1

    if txt_last == extract_end or txt_last > end_of_db:
        cls_name.config_info(f"Checking {info_name} Updates... No Updates Found.")
        return

    sleep(1)
    webcount = 0
    cls_name.config_info("Retrieving New Data from Web...")
    idgroup = [i for i in range(txt_last, extract_end)]
    if txt_last == 1 and IDB_name == 'mltdkei_idoldata_kr.sqlite': idgroup = [9001, 9002, 9003] + idgroup
    cls_name.config_pbr(webcount, extract_end-txt_last, extract_end-txt_last)
    cls_name.add_info2()

    for idnumber in idgroup:
        webcount += 1
        if idnumber == 1064 or idnumber == 1065:
            cls_name.update_pbr(webcount, webcount)
            continue
        webdata1 = urlopen(matsuri_url+str(idnumber))
        soup1 = BeautifulSoup(webdata1, 'html.parser')
        name = soup1.find("h1").get_text()
        namedict[idnumber] = name
        cls_name.update_pbr(webcount, webcount)
        cls_name.config_info2(name)
        sleep(0.5)

    ilist = cur1.execute('select idnumber, rare from IdolDB').fetchall()
    for i in ilist:
        if len(i) == 0 or int(i[0]) < txt_last: continue
        # IDNumber,Rare,Name,Have,Rank,SkillLevel
        try: infodata.append(f'{i[0]},{i[1]},{namedict[int(i[0])]},0,0,1')
        except: continue
    infodata.append('')
    infofile = open(info_name, 'w', encoding='utf-8')
    infofile.write('\n'.join(infodata))
    infofile.close()
    cls_name.config_info(f"{info_name} Update Completed.")

def main_hub(IDB_name, MDB_name, info_name):
    uhb_root = Toplevel()
    uhb_root.title("MLTD Deck Analyzer DB Update Tool")

    if IDB_name == 'mltdkei_idoldata.sqlite': matsuri_url = "https://mltd.matsurihi.me/cards/"
    elif IDB_name == 'mltdkei_idoldata_kr.sqlite': matsuri_url = "https://mltd.matsurihi.me/ko/cards/"
    github_url = "https://raw.githubusercontent.com/HyphenK/mltdkei_v3/v40_main/"

    class LB4:
        def update_check(self, t2, t3, t4):
            self.lb_U.config(text="Loading")
            if t4 == 0:
                if t2 == t3: self.lb_U.config(text="Up to date")
                else: self.lb_U.config(text="Need Update")
            elif t4 == 1:
                if t2 < t3: self.lb_U.config(text="Up to date")
                elif t2 == t3: pass
                else: self.lb_U.config(text="Need Update")

        def place_all(self, where, r, t1, t2, t3, t4):
            self.lb_1 = Label(where, text=t1, width=12, borderwidth=2, relief="groove")
            self.lb_1.grid(row=r, column=0, sticky=E+W, ipady=3)

            self.lb_L = Label(where, text=t2, width=15, borderwidth=2, relief="groove")
            self.lb_L.grid(row=r, column=1, sticky=E+W, ipady=3)

            self.lb_C = Label(where, text=t3, width=15, borderwidth=2, relief="groove")
            self.lb_C.grid(row=r, column=2, sticky=E+W, ipady=3)

            if t4 == 0 or t4 == 1:
                self.lb_U = Label(where, width=12, borderwidth=2, relief="groove")
                self.lb_U.grid(row=r, column=3, sticky=E+W, ipady=3)
                self.update_check(t2, t3, t4)
                self.btn_U = Button(where, text="Update", width=12)
                self.btn_U.grid(row=r, column=4, sticky=E+W)
            else:
                self.lb_U = Label(where, text=t4, width=24, borderwidth=2, relief="groove")
                self.lb_U.grid(row=r, column=3, columnspan=2, sticky=E+W, ipady=3)

        def config_date(self, t2, t3, t4):
            self.lb_L.config(text=t2)
            self.lb_C.config(text=t3)
            self.update_check(t2, t3, t4)

        def config_button(self, cmd):
            self.btn_U.config(command=cmd)

        def oc_button(self, cmd):
            if cmd == 1: self.btn_U.config(state="normal")
            elif cmd == 2: self.btn_U.config(state="disabled")

    class PbrSide:
        def __init__(self):
            for widget in fr_pbr.winfo_children():
                widget.destroy()

            self.pbar_var = IntVar()

            self.lb_left = Label(fr_pbr, width=10, borderwidth=2, relief="groove", bg="white")
            self.lb_left.grid(row=0, column=0, ipady=3)

            self.lb_middle = Label(fr_pbr, text="/")
            self.lb_middle.grid(row=0, column=1, ipady=3)

            self.lb_right = Label(fr_pbr, width=10, borderwidth=2, relief="groove", bg="white")
            self.lb_right.grid(row=0, column=2, ipady=3)

            self.pbar = ttk.Progressbar(fr_pbr, length=330, maximum=100, variable=self.pbar_var)
            self.pbar.grid(row=0, column=3, ipady=2)

            self.lb_info = Label(fr_pbr, width=70, borderwidth=2, relief="groove", bg="white")
            self.lb_info.grid(row=1, column=0, columnspan=4, ipady=3)

            uhb_root.update()

        def config_info(self, info):
            self.lb_info.config(text=info)
            uhb_root.update()

        def config_pbr(self, left, right, max):
            self.lb_left.config(text=left)
            self.lb_right.config(text=right)
            self.pbar.config(maximum=max)
            self.pbar_var.set(0)
            uhb_root.update()

        def update_pbr(self, left, var):
            self.lb_left.config(text=left)
            self.pbar_var.set(var)
            uhb_root.update()

        def add_info2(self):
            self.lb_info2 = Label(fr_pbr, width=70, borderwidth=2, relief="groove", bg="white")
            self.lb_info2.grid(row=2, column=0, columnspan=4, ipady=3)
            uhb_root.update()

        def config_info2(self, info):
            self.lb_info2.config(text=info)
            uhb_root.update()

    fr_db = Frame(uhb_root)
    fr_db.grid(row=1, column=0)

    lb_db = Label(fr_db, text="<Database Update>", borderwidth=2, relief="groove")
    lb_db.grid(row=0, column=0, columnspan=5, sticky=E+W, ipady=3)

    lb_kind = LB4()
    lb_kind.place_all(fr_db, 1, "＼", "Latest", "File", "Update")

    def oc_button(i):
        lb_music.oc_button(i)
        lb_card.oc_button(i)
        uhb_root.update()

    def update_music_db():
        oc_button(2)
        UMDB = PbrSide()
        UMDB.config_info("Updating Music DB...")
        download_file = MDB_name
        response = requests.get(github_url+download_file, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024*512 #0.5 MiB
        UMDB.config_pbr("0MB", f"{round(total_size_in_bytes/1024/1024, 1)}MB", total_size_in_bytes//block_size+1)
        vard, dlsize = 0, 0
        with open(download_file, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                vard, dlsize = vard + 1, round(dlsize+len(data)/1024/1024, 1)
                UMDB.update_pbr(f"{dlsize}MB", vard)
        if total_size_in_bytes != 0 and vard != total_size_in_bytes//block_size+1:
            UMDB.config_info("Updating Music DB... ERROR. Please Try Again.")
        else: UMDB.config_info("Updating Music DB... Complete.")
        oc_button(1)

    lb_music = LB4()
    lb_music.place_all(fr_db, 2, "Music", "Loading", "Loading", 1)
    lb_music.config_button(update_music_db)

    def update_card_db():
        oc_button(2)
        UCDB1 = PbrSide()
        UCDB1.config_info("Updating Idol DB...")
        download_file = IDB_name
        response = requests.get(github_url+download_file, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024*512 #0.5 MiB
        UCDB1.config_pbr("0MB", f"{round(total_size_in_bytes/1024/1024, 1)}MB", total_size_in_bytes//block_size+1)
        vard, dlsize = 0, 0
        with open(download_file, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                vard, dlsize = vard + 1, round(dlsize+len(data)/1024/1024, 1)
                UCDB1.update_pbr(f"{dlsize}MB", vard)
        if total_size_in_bytes != 0 and vard != total_size_in_bytes//block_size+1:
            UCDB1.config_info("Updating Idol DB... ERROR. Please Try Again.")
        else: UCDB1.config_info("Updating Idol DB... Complete.")
        sleep(2)
        UCDB2 = PbrSide()
        UCDB2.config_info(f"Checking {info_name} Updates...")
        update_info(UCDB2, IDB_name, info_name, matsuri_url)
        oc_button(1)

    lb_card = LB4()
    lb_card.place_all(fr_db, 3, "Card", "Loading", "Loading", 1)
    lb_card.config_button(update_card_db)

    fr_pbr = Frame(uhb_root)
    fr_pbr.grid(row=2, column=0)

    uhb_root.update()

    version_data = urlopen(github_url+"version_check").read().decode('utf-8')
    songdata = findall('SongData\(.+\) (.+)\n', version_data)
    idoldata = findall('IdolData\(.+\) (.+)\n', version_data)
    if IDB_name == 'mltdkei_idoldata.sqlite':
        songdata = songdata[0]
        idoldata = idoldata[0]
    elif IDB_name == 'mltdkei_idoldata_kr.sqlite':
        songdata = songdata[1]
        idoldata = idoldata[1]

    file_music = strftime('%Y/%m/%d %H:%M', localtime(getmtime(MDB_name)))
    file_card = strftime('%Y/%m/%d %H:%M', localtime(getmtime(IDB_name)))
    ingame_music = songdata
    ingame_card = idoldata
    lb_music.config_date(ingame_music, file_music, 1)
    lb_card.config_date(ingame_card, file_card, 1)

    uhb_root.mainloop()
