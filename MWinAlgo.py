import wmi
from datetime import datetime
import csv
import time
import zlib
from cryptography.fernet import Fernet


class MWinAlgo:
    def __init__(self, mdrow):
        self.my_drow = mdrow
        self.mon_run = False
        self.services_list = [] # [(date, {pid : pname})]
        # list for all the servies< (time : dict<pid : name )>>

    def start(self, refresh_time):
        self.my_drow.write("the program start to work")
        #load the file ".monitor.log" to the list

        self.mon_run = True
        #while(mon_run)
        # dict now_servies= <pid:name>
        #comper to the last
        #write changes
        #checksum ->w_check = checksum(dict now_sercies)
        #write inscrept(time +""+ check+"" +dict(now_sercies))
        #wait(refresh_time)
        i = 0
        while(i < 2):
            self.compare_services() # compare between services - prints to user, and write in status_log
            self.write_to_servicelist() # write into serviceList the last sample of services according to date and checksum
            time.sleep(2)
            i+=1



    # def check_hacked(self):


        # while(self.mon_run):


    def check_sum(self, dict_to_encrypt):
        checksum = 0
        for pname in dict_to_encrypt.items():
            c1 = 1
            for a in pname:
                c1 = zlib.adler32(bytes(repr(a), 'utf-8'), c1)
            checksum = checksum ^ c1
        print(checksum)
        return checksum

    def compare_services(self):
        curr_time = datetime.now()
        curr_service = {}
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
            checksum = self.check_sum(curr_service)
            f2.write(f"checksum: {checksum}\n")
            f2.close()
            self.services_list.append((curr_time, curr_service))
        else:
            last_service = self.services_list[-1][1]
            for process in f.Win32_Process():
                curr_service[process.ProcessId] = process.Name
                if process.ProcessId not in last_service:
                    change = True

            for curr_pid in curr_service.keys():
                if curr_pid not in last_service:
                    change = True

            if not change:
                self.my_drow.write("nothing has changed!:")
            else:
                f2 = open("status_log.txt", "a")
                self.my_drow.write("new services:")
                f2.write(f"date: {curr_time}\n")
                f2.write("new services:\n")
                for curr_pid in curr_service.keys():
                    if curr_pid not in last_service:
                        self.my_drow.write(f"{curr_pid} - {curr_service[curr_pid]}")
                        f2.write(f"{curr_pid} - {curr_service[curr_pid]}\n")

                self.my_drow.write("services no longer run:")
                f2.write("services no longer run:\n")
                for last_pid in last_service.keys():
                    if last_pid not in curr_service:
                        self.my_drow.write(f"{last_pid} - {last_service[last_pid]}")
                        f2.write(f"{last_pid} - {last_service[last_pid]}\n")
                checksum = self.check_sum(curr_service)
                f2.write(f"checksum: {checksum}\n")
                f2.close()

        self.services_list.append((curr_time,curr_service))

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
        # writer1 = csv.writer(tup1)

        tup1 = (date, checksum)
        writer.writerow(tup1)
        # writer1 = csv.writer(tup1)

        tup1 = ("pid", "pname")
        writer.writerow(tup1)

        for pid in last_service.keys():
            tup1 = (pid, last_service[pid])
            writer.writerow(tup1)

        f.close()



    def stop(self):
        self.my_drow.write("the program stop to work")

        self.mon_run = False

    def comper(self, fdate, ftime , tdate, ttime):
        self.my_drow.write(f"{fdate} {ftime} comper to {tdate} {ttime}")
