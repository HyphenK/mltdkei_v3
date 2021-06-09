# Python Module #
from tkinter import *
import tkinter.ttk as ttk
import requests
import webbrowser
from re import findall
from urllib.request import urlopen

version = "[3.0] 21/06/09"

uhb_root = Tk()
uhb_root.title("MLTD Deck Analyzer EXE version Update Tool")

github_url = "https://raw.githubusercontent.com/HyphenK/mltdkei_v3/main_kr/"
github_url_exe = "https://raw.githubusercontent.com/HyphenK/mltdkei_v3/exe_kr/"

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

    def config_button(self, cmd):
        self.btn_U.config(command=cmd)

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

version_data = urlopen(github_url+"version_check").read().decode('utf-8')
program_ver = findall('UpdateExe (.+)\n', version_data)[0]
exe_ver = findall('ExeFile (.+)\n', version_data)[0]

fr_pg = Frame(uhb_root)
fr_pg.grid(row=0, column=0)

lb_kind = LB4()
lb_kind.place_all(fr_pg, 1, "＼", "Latest", "Current", "Update")

def core_update():
    readme_url = 'https://github.com/HyphenK/mltdkei_v3'
    webbrowser.open(readme_url, new=1)

lb_core = LB4()
lb_core.place_all(fr_pg, 2, "Program", program_ver, version, 0)
lb_core.config_button(core_update)

def update_exe():
    UMDB = PbrSide()
    UMDB.config_info("Updating EXE file...")
    download_file = "mltdkei_v30E_kr.exe"
    response = requests.get(github_url_exe+"mltdkei_v30E_kr.exe", stream=True)
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
        UMDB.config_info("Updating EXE file... ERROR. Please Try Again.")
    else: UMDB.config_info("Updating EXE file... Complete.")
    exe_file = open("exe_version", "w")
    exe_file.write(exe_ver)
    exe_file.close()

exe_file = open("exe_version")
exe_version = exe_file.read().strip()
exe_file.close()

lb_exe = LB4()
lb_exe.place_all(fr_pg, 3, "EXE File", exe_ver, exe_version, 0)
lb_exe.config_button(update_exe)

fr_pbr = Frame(uhb_root)
fr_pbr.grid(row=2, column=0)

uhb_root.mainloop()
