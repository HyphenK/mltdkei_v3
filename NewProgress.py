from tkinter import *
import tkinter.ttk as ttk
# NewProgress for for above ver.4.19 21/08/02

def disable_func(): # Disable Window's Delete Key
    pass

class NewProgress: # Progress Bar Window
    def __init__(self):
        self.npr_root = Tk()
        self.npr_root.title("Progress Window")
        self.npr_root.geometry("200x50")
        self.npr_root.resizable(False, False)
        self.npr_root.protocol("WM_DELETE_WINDOW", disable_func)

        self.lb_running = Label(self.npr_root, borderwidth=2, relief="groove")
        self.lb_running.place(x=0, y=0, width=50, height=50)

        self.pbar_varnp = IntVar()
        self.pbr_running = ttk.Progressbar(self.npr_root, variable=self.pbar_varnp)
        self.pbr_running.place(x=50, y=0, width=149, height=24)

        self.lb_runningleft = Label(self.npr_root, text=0, borderwidth=2, relief="groove", bg="white")
        self.lb_runningleft.place(x=50, y=25, width=70, height=25)

        self.lb_runningmiddle = Label(self.npr_root, text="/")
        self.lb_runningmiddle.place(x=120, y=25, width=10, height=25)

        self.lb_runningright = Label(self.npr_root, text=0, borderwidth=2, relief="groove", bg="white")
        self.lb_runningright.place(x=130, y=25, width=70, height=25)

    def workid(self, id1, id2):
        if id1 == 1: self.text1 = "Appeal\nCalc"
        elif id1 == 2: self.text1 = "Ideal\nCalc"
        elif id1 == 3: self.text1 = "Score\nCalc"
        self.text = " ".join([self.text1, str(id2)])
        self.lb_running.config(text=self.text)
        if id1 == 3:
            self.pbar_varnpm = IntVar()
            self.pbr_runningm = ttk.Progressbar(self.npr_root, variable=self.pbar_varnpm, maximum=100)
            self.pbr_runningm.place(x=50, y=15, width=149, height=9)
        self.npr_root.update()

    def configmax(self, max, pbr):
        self.pbr_running.config(maximum=pbr)
        self.lb_runningright.config(text=max)
        self.npr_root.update()

    def configleft(self, left, var1):
        self.pbar_varnp.set(var1)
        self.lb_runningleft.config(text=left)
        self.npr_root.update()

    def configmiddle(self, middle):
        self.pbar_varnpm.set(middle)
        self.npr_root.update()
        
    def closewindow(self):
        self.npr_root.destroy()
