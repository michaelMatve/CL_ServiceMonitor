from tkinter import *
from tkinter.ttk import Progressbar
import threading
from sys import platform
if platform == "win32":
    from MWinAlgo import MWinAlgo
else:
    from MLinAlgo import MLinAlgo



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

        self.lable_fdate = None
        self.lable_ftime =None
        self.lable_tdate = None
        self.lable_ttime = None

        self.from_comper_input = {}
        self.to_comper_input = {}

        self.get_servies_button = None

        self.lable_get_date = None
        self.get_servies_input = {}

        self.lable_get_time = None

        self.button_get_servies = None

        self.frame = None
        self.output = None

    def write(self,write_content):
        self.output.insert(END,write_content+"\n")

    def throwalert(self,write_content):
        thread = threading.Thread(target=self.throwalerthred, args=(write_content,))
        thread.start()

    def throwalerthred(self, write_content):
        wm = Tk()
        wm.title("service monitor 2.0")
        titel_label = Label(wm, text="error:", fg="black", font="none 12 bold")
        titel_label.grid(row=0, column=0, sticky=W)
        error_label = Label(wm, text=write_content, fg="black", font="none 12 bold")
        error_label.grid(row=1, column=0, sticky=W)
        wm.mainloop()

    def writeIN_new_window(self, title_h, write_content):
        thread = threading.Thread(target=self.throwalerthred, args=(title_h, write_content,))
        thread.start()

    def writeIN_new_window_thred(self, title_h, write_content):
        wm = Tk()
        wm.title("service monitor 2.0")
        titel_label = Label(wm, text=title_h, fg="black", font="none 12 bold")
        titel_label.grid(row=0, column=0, sticky=W)
        error_label = Label(wm, text=write_content, fg="black", font="none 12 bold")
        error_label.grid(row=1, column=0, sticky=W)
        wm.mainloop()

    def start(self):
        refresh_time = self.refresh_input.get()
        if (len(refresh_time.split(':')) == 3):
            self.button_start.destroy()
            thread = threading.Thread(target=self.algoM.start, args= (refresh_time,))
            thread.start()
            self.refresh_input.destroy()
            self.draw_start()

        else:
            self.throwalert("bad time insert. \n should be: hh:mm:ss")

    def stop(self):
        self.algoM.stop()
        self.draw_stop()

    def comper(self):
        fdate = self.from_comper_input['date'].get()
        self.from_comper_input['date'].delete(0, END)
        self.from_comper_input['date'].insert(0,"yyyy-mm-dd")
        ftime = self.from_comper_input['time'].get()
        self.from_comper_input['time'].delete(0, END)
        self.from_comper_input['time'].insert(0,"hh:mm:ss")

        tdate = self.to_comper_input['date'].get()
        self.to_comper_input['date'].delete(0, END)
        self.to_comper_input['date'].insert(0,"yyyy-mm-dd")
        ttime = self.to_comper_input['time'].get()
        self.to_comper_input['time'].delete(0, END)
        self.to_comper_input['time'].insert(0,"hh:mm:ss")
        if (len(ttime.split(':')) == 3) and (len(tdate.split('-')) == 3) and (len(ftime.split(':')) == 3) and (len(fdate.split('-')) == 3):
            self.algoM.comper(fdate,ftime,tdate,ttime)
        else:
            self.throwalert("bad insert. \n time should be: hh:mm:ss \n and date should be: yyyy-mm-dd")

    def servies_by_dateandtime(self):
        gdate = self.get_servies_input['date'].get()
        self.get_servies_input['date'].delete(0, END)
        self.get_servies_input['date'].insert(0, "yyyy-mm-dd")
        gtime = self.get_servies_input['time'].get()
        self.get_servies_input['time'].delete(0, END)
        self.get_servies_input['time'].insert(0, "hh:mm:ss")
        if (len(gtime.split(':')) == 3) and (len(gdate.split('-')) == 3):
            self.algoM.get_sample(gdate,gtime)
        else:
            self.throwalert("bad insert. \n time should be: hh:mm:ss \n and date should be: yyyy-mm-dd")

    def draw_stop(self):
        self.button_stop.destroy()

        self.button_start = Button(self.window, text="start", command=self.start)
        self.button_start.grid(row=1, column=0, sticky=W)

        self.refresh_input = Entry(self.window, background="gray", fg="black")
        self.refresh_input.insert(0, "00:00:02")
        self.refresh_input.grid(row=1, column=1, sticky=W)

        self.from_comper_label.destroy()

        self.lable_fdate.destroy()
        self.from_comper_input['date'].destroy()

        self.lable_ftime.destroy()
        self.from_comper_input['time'].destroy()

        self.to_comper_label.destroy()

        self.lable_tdate.destroy()
        self.to_comper_input['date'].destroy()

        self.lable_ttime.destroy()
        self.to_comper_input['time'].destroy()

        self.button_comper.destroy()

        self.get_servies_button.destroy()

        self.lable_get_date.destroy()
        self.get_servies_input['date'].destroy()

        self.lable_get_time.destroy()
        self.get_servies_input['time'].destroy()

        self.button_get_servies.destroy()

    def draw_start(self):

        self.button_stop = Button(self.window, text="stop", command=self.stop)
        self.button_stop.grid(row=1, column=0, sticky=W)

        self.from_comper_label = Label(self.window, text="from:", fg="black", font="none 12 bold")
        self.from_comper_label.grid(row=2, column=0, sticky=W)

        self.lable_fdate = Label(self.window, text="date:", fg="black", font="none 12 bold")
        self.lable_fdate.grid(row=3, column=0, sticky=W)
        self.from_comper_input['date'] = Entry(self.window, background="gray", fg="black")
        self.from_comper_input['date'].insert(0, "yyyy-mm-dd")
        self.from_comper_input['date'].grid(row=3, column=1, sticky=W)

        self.lable_ftime = Label(self.window, text="time:", fg="black", font="none 12 bold")
        self.lable_ftime.grid(row=3, column=2, sticky=W)
        self.from_comper_input['time'] = Entry(self.window, background="gray", fg="black")
        self.from_comper_input['time'].insert(0, "hh:mm:ss")
        self.from_comper_input['time'].grid(row=3, column=3, sticky=W)

        self.to_comper_label = Label(self.window, text="to :", fg="black", font="none 12 bold")
        self.to_comper_label.grid(row=4, column=0, sticky=W)

        self.lable_tdate = Label(self.window, text="date:", fg="black", font="none 12 bold")
        self.lable_tdate.grid(row=5, column=0, sticky=W)
        self.to_comper_input['date'] = Entry(self.window, background="gray", fg="black")
        self.to_comper_input['date'].insert(0, "yyyy-mm-dd")
        self.to_comper_input['date'].grid(row=5, column=1, sticky=W)

        self.lable_ttime = Label(self.window, text="time:", fg="black", font="none 12 bold")
        self.lable_ttime.grid(row=5, column=2, sticky=W)
        self.to_comper_input['time'] = Entry(self.window, background="gray", fg="black")
        self.to_comper_input['time'].insert(0, "hh:mm:ss")
        self.to_comper_input['time'].grid(row=5, column=3, sticky=W)

        self.button_comper = Button(self.window, text="comper", command=self.comper)
        self.button_comper.grid(row=6, column=0, sticky=W)

        self.get_servies_button = Label(self.window, text="get servies from date/time:", fg="black", font="none 12 bold")
        self.get_servies_button.grid(row=7, column=0, sticky=W)

        self.lable_get_date = Label(self.window, text="date:", fg="black", font="none 12 bold")
        self.lable_get_date.grid(row=8, column=0, sticky=W)
        self.get_servies_input['date'] = Entry(self.window, background="gray", fg="black")
        self.get_servies_input['date'].insert(0, "yyyy-mm-dd")
        self.get_servies_input['date'].grid(row=8, column=1, sticky=W)

        self.lable_get_time = Label(self.window, text="time:", fg="black", font="none 12 bold")
        self.lable_get_time.grid(row=8, column=2, sticky=W)
        self.get_servies_input['time'] = Entry(self.window, background="gray", fg="black")
        self.get_servies_input['time'].insert(0, "hh:mm:ss")
        self.get_servies_input['time'].grid(row=8, column=3, sticky=W)

        self.button_get_servies = Button(self.window, text="get serviec", command=self.servies_by_dateandtime)
        self.button_get_servies.grid(row=9, column=0, sticky=W)

    def draw(self):
        self.window = Tk()
        self.window.title("service monitor 2.0")

        self.button_start = Button(self.window, text="start", command=self.start)
        self.button_start.grid(row=1, column=0, sticky=W)

        self.refresh_input = Entry(self.window, background="gray", fg="black")
        self.refresh_input.insert(0, "00:00:02")
        self.refresh_input.grid(row=1, column=1, sticky=W)

        self.frame = Frame(self.window)

        scroller = Scrollbar(self.frame)
        scroller.pack(side=RIGHT, fill=Y)
        
        self.output = Text(self.frame,yscrollcommand = scroller.set, wrap="none", background="gray" )
        self.output.pack(expand=True, side=LEFT)

        scroller.config(command = self.output.yview)


        self.frame.grid(row=10, column=0, columnspan=4, sticky=W)

        self.window.mainloop()