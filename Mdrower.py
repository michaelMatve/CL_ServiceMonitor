from tkinter import *
from tkinter.ttk import Progressbar
import threading
from MWinAlgo import MWinAlgo
from MLinAlgo import MLinAlgo
from sys import platform


class Mdrower:
    def __init__(self):
        if platform == "win32":
            print('win')
            self.algoM = MWinAlgo(self)
        else:
            print('lin')
            self.algoM = MLinAlgo(self)
        self.window = None
        self.button_start = None
        self.refresh_input = None
        self.button_stop =None
        self.button_comper =None
        self.from_comper_label = None
        self.to_comper_label = None
        self.from_comper_input = {}
        self.to_comper_input = {}
        self.frame = None
        self.output = None

    def write(self,write_content):
        self.output.insert(END,write_content+"\n")

    def start(self):
        self.button_start.destroy()
        refresh_time = self.refresh_input.get()
        thread = threading.Thread(target=self.algoM.start, args= (refresh_time,))
        thread.start()
        self.refresh_input.destroy()
        self.button_stop = Button(self.window, text="stop", command=self.stop)
        self.button_stop.grid(row=1, column=0, sticky=W)

    def stop(self):
        self.button_stop.destroy()
        self.algoM.stop()

        self.button_start = Button(self.window, text="start", command=self.start)
        self.button_start.grid(row=1, column=0, sticky=W)

        self.refresh_input = Entry(self.window, background="gray", fg="black")
        self.refresh_input.insert(0, "00:00:02")
        self.refresh_input.grid(row=1, column=1, sticky=W)

    def comper(self):
        fdate = self.from_comper_input['date'].get()
        self.from_comper_input['date'].delete(0, END)
        self.from_comper_input['date'].insert(0,"XXXX-XX-XX")
        ftime = self.from_comper_input['time'].get()
        self.from_comper_input['time'].delete(0, END)
        self.from_comper_input['time'].insert(0,"XX:XX:XX")

        tdate = self.to_comper_input['date'].get()
        self.to_comper_input['date'].delete(0, END)
        self.to_comper_input['date'].insert(0,"XXXX-XX-XX")
        ttime = self.to_comper_input['time'].get()
        self.to_comper_input['time'].delete(0, END)
        self.to_comper_input['time'].insert(0,"XX:XX:XX")

        self.algoM.comper(fdate,ftime,tdate,ttime)

    def draw(self):
        self.window = Tk()
        self.window.title("service monitor 2.0")

        self.button_start = Button(self.window, text="start", command=self.start)
        self.button_start.grid(row=1, column=0, sticky=W)

        self.refresh_input = Entry(self.window, background="gray", fg="black")
        self.refresh_input.insert(0, "00:00:02")
        self.refresh_input.grid(row=1, column=1, sticky=W)

        self.frame = Frame(self.window)
        self.output = Text(self.frame, wrap=WORD, background="gray")
        self.output.pack(expand=True, side=LEFT)

        scroller = Scrollbar(self.frame)
        scroller.pack(side=RIGHT, fill = BOTH)

        self.frame.grid(row=7, column=0, columnspan=4, sticky=W)

        self.from_comper_label = Label(self.window, text="from:", fg="black", font="none 12 bold")
        self.from_comper_label.grid(row=2, column=0, sticky=W)

        lable_fdate = Label(self.window, text="date:", fg="black", font="none 12 bold")
        lable_fdate .grid(row=3, column=0, sticky=W)
        self.from_comper_input['date']= Entry(self.window,background="gray",fg="black")
        self.from_comper_input['date'].insert(0,"yyyy-mm-dd")
        self.from_comper_input['date'].grid(row=3, column=1, sticky=W)

        lable_ftime = Label(self.window, text="time:", fg="black", font="none 12 bold")
        lable_ftime .grid(row=3, column=2, sticky=W)
        self.from_comper_input['time'] = Entry(self.window, background="gray", fg="black")
        self.from_comper_input['time'].insert(0, "hh:mm:ss")
        self.from_comper_input['time'].grid(row=3, column=3, sticky=W)

        self.to_comper_label = Label(self.window, text="to :", fg="black", font="none 12 bold")
        self.to_comper_label.grid(row=4, column=0, sticky=W)

        lable_tdate = Label(self.window, text="date:", fg="black", font="none 12 bold")
        lable_tdate.grid(row=5, column=0, sticky=W)
        self.to_comper_input['date']= Entry(self.window,background="gray",fg="black")
        self.to_comper_input['date'].insert(0,"yyyy-mm-dd")
        self.to_comper_input['date'].grid(row=5, column=1, sticky=W)

        lable_ftime = Label(self.window, text="time:", fg="black", font="none 12 bold")
        lable_ftime .grid(row=5, column=2, sticky=W)
        self.to_comper_input['time'] = Entry(self.window, background="gray", fg="black")
        self.to_comper_input['time'].insert(0, "hh:mm:ss")
        self.to_comper_input['time'].grid(row=5, column=3, sticky=W)

        self.button_comper = Button(self.window, text="comper", command=self.comper)
        self.button_comper.grid(row=6, column=0, sticky=W)
        self.window.mainloop()