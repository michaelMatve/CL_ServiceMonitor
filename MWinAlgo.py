import wmi
from datetime import datetime
import csv
import time
import zlib
from cryptography.fernet import Fernet
import pythoncom


class MWinAlgo:
    def __init__(self, mdrow):
        self.my_drow = mdrow
        self.mon_run = False
        self.services_list = [] # [(date, {pid : pname})]
        # list for all the servies< (time : dict<pid : name )>>

    def start(self, refresh_time):
        self.my_drow.write("the program start to work")
        new_time = refresh_time.split(":")
        new_time = ((int(new_time[0]) * 60) + int(new_time[1]))*60 + int(new_time[2])
        self.load_to_list()
        while(self.mon_run):
            self.compare_services() # compare between services - prints to user, and write in status_log
            self.write_to_servicelist() # write into serviceList the last sample of services according to date and checksum
            time.sleep(new_time)



    def load_to_list(self):
        f = open("serviceList.csv", 'a')
        f.close()

        with open("serviceList.csv", 'r') as file:
            reader = csv.reader(file)
            flag_exist = False
            checksum = None
            date = None
            for line in reader:
                if line == ['pid', 'pname']:
                    pass
                elif flag_exist:
                    date = line[0]
                    checksum = line[1]
                    self.services_list.append((date, {}))
                    flag_exist = False
                elif line == ['date', 'checksum']:
                    if checksum != None:
                        if int(self.check_sum(self.services_list[-1][1])) != int(checksum):
                            print(checksum)
                            print(self.check_sum(self.services_list[-1][1]))
                            for process in self.services_list[-1][1].keys():
                                print(f"{process},{self.services_list[-1][1][process]}")
                            self.my_drow.write("someone change yuour files1111111 !!!!!!!!!!!!!!!!!!!!!!!!")
                            self.my_drow.stop()
                            return
                    flag_exist = True
                else:
                    self.services_list[-1][1][int(line[0])]=line[1]

            if checksum is not None:
                if int(self.check_sum(self.services_list[-1][1])) != int(checksum):
                    self.my_drow.write("someone change yuour files !!!!!!!!!!!!!!!!!!!!!!!!")
                    self.my_drow.stop()
                    return
            self.mon_run = True


    # def check_hacked(self):


        # while(self.mon_run):


    def check_sum(self, dict_to_encrypt):
        checksum = 0
        for pname in dict_to_encrypt.items():
            c1 = 1
            for a in pname:
                c1 = zlib.adler32(bytes(repr(a), 'utf-8'), c1)
            checksum = checksum ^ c1
        return checksum

    def compare_services(self):
        curr_time = datetime.now()
        curr_service = {}
        pythoncom.CoInitialize()
        f = wmi.WMI()
        change = False

        if not self.services_list:
            f2 = open("status_log.txt", "a")
            f2.write(f"date: {curr_time}\n")
            self.my_drow.write("new services:")
            f2.write("new services:\n")
            for process in f.Win32_Process():
                curr_service[process.ProcessId] = process.Name
                self.my_drow.write(f"{process.ProcessId} {process.Name}")
                f2.write(f"{process.ProcessId} - {process.Name}\n")
            self.services_list.append((curr_time, curr_service))
            checksum = self.check_sum(self.services_list[-1][1])
            f2.write(f"checksum: {checksum}\n")
            f2.close()

        else:
            last_service = self.services_list[-1][1]
            for process in f.Win32_Process():
                curr_service[process.ProcessId] = process.Name
                if process.ProcessId not in last_service or process.Name not in last_service.values():
                    change = True

            for curr_pid in curr_service.keys():
                if curr_pid not in last_service or curr_service[curr_pid] not in last_service.values():
                    change = True

            if not change:
                self.my_drow.write("nothing has changed!:")
            else:
                f2 = open("status_log.txt", "a")
                self.my_drow.write("new services:")
                f2.write(f"date: {curr_time}\n")
                f2.write("new services:\n")
                for curr_pid in curr_service.keys():
                    if curr_pid not in last_service or curr_service[curr_pid] not in last_service.values():
                        self.my_drow.write(f"{curr_pid} - {curr_service[curr_pid]}")
                        f2.write(f"{curr_pid} - {curr_service[curr_pid]}\n")

                self.my_drow.write("services no longer run:")
                f2.write("services no longer run:\n")
                for last_pid in last_service.keys():
                    if last_pid not in curr_service or last_service[last_pid] not in curr_service.values():
                        self.my_drow.write(f"{last_pid} - {last_service[last_pid]}")
                        f2.write(f"{last_pid} - {last_service[last_pid]}\n")
                checksum = self.check_sum(curr_service)
                f2.write(f"checksum: {checksum}\n")
                f2.close()


    def write_to_servicelist(self):
        # file look like :
        # date, checksum
        # actualdate, calc_checksum
        # pid, pname
        #actual_pid, pname

        date = self.services_list[-1][0]
        last_service = self.services_list[-1][1]
        checksum = self.check_sum(last_service)

        f = open("serviceList.csv", "a", newline="")
        # f1 = open("serviceList_enc.csv", "a", newline="")
        writer = csv.writer(f)
        # writer1 = csv.writer(f1)

        tup1 = ("date", "checksum")
        writer.writerow(tup1)
        print(f"{tup1[0]},{tup1[1]}")
        # writer1 = csv.writer(tup1)

        tup1 = (date, checksum)
        writer.writerow(tup1)
        print(f"{tup1[0]},{tup1[1]}")
        # writer1 = csv.writer(tup1)

        tup1 = ("pid", "pname")
        writer.writerow(tup1)
        print(f"{tup1[0]},{tup1[1]}")

        for pid in last_service.keys():
            tup1 = (pid, last_service[pid])
            writer.writerow(tup1)
            print(f"{tup1[0]},{tup1[1]}")

        f.close()



    def stop(self):
        self.my_drow.write("the program stop to work")

        self.mon_run = False

    def comper(self, fdate, ftime , tdate, ttime):
        self.my_drow.write(f"{fdate} {ftime} comper to {tdate} {ttime}")
