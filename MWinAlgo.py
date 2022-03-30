import wmi
from datetime import datetime
import csv
import time
import zlib
import pythoncom
import os


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
        self.check_hacked()
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
        file.close()
        os.system("attrib +h " + "serviceList.csv")


    def check_hacked(self):
        f = open("status_log.txt", 'a')
        f.close()

        check_dict = {}

        f = open("status_log.txt", 'r')
        lines = f.readlines()
        for line in lines:
            if line.split()[0] == "date:":
                pass
            elif line.split()[0] == "new" or line.split()[0] == "services":
                pass
            elif line.split()[0] == "checksum:":
                checksum = str(line.split()[1])
                comp_checksum = self.check_sum(check_dict)
                if checksum != str(comp_checksum):
                    self.my_drow.write("someone changed the status_log !!!!!")
                    self.my_drow.stop()
                    return
                else:
                    check_dict = {}
            else:
                pid = line.split(' - ')[0]
                pname = line.split(' - ')[1][:-1]
                check_dict[str(pid)] = str(pname)

        os.system("attrib +h " + "status_log.txt")



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
        for_checksum = {}

        if not self.services_list:
            f2 = open("status_log.txt", "a")
            f2.write(f"date: {curr_time}\n")
            self.my_drow.write("new services:")
            f2.write("new services:\n")
            for process in f.Win32_Process():
                curr_service[process.ProcessId] = str(process.Name)
                self.my_drow.write(f"{process.ProcessId} {process.Name}")
                f2.write(f"{process.ProcessId} - {process.Name}\n")
                for_checksum[str(process.ProcessId)] = str(process.Name)
            self.services_list.append((curr_time, curr_service))
            checksum = self.check_sum(for_checksum)
            f2.write(f"checksum: {checksum}\n")
            f2.close()
            os.system("attrib +h " + "status_log.txt")

        else:
            last_service = self.services_list[-1][1]
            for process in f.Win32_Process():
                curr_service[process.ProcessId] = process.Name
                if process.Name not in last_service.values():
                    change = True

            for curr_pid in curr_service.keys():
                if curr_service[curr_pid] not in last_service.values():
                    change = True

            if not change:
                self.my_drow.write("nothing has changed!")
            else:
                f2 = open("status_log.txt", "a")
                self.my_drow.write("new services:")
                f2.write(f"date: {curr_time}\n")
                f2.write("new services:\n")
                for curr_pid in curr_service.keys():
                    if curr_service[curr_pid] not in last_service.values():
                        self.my_drow.write(f"{curr_pid} - {curr_service[curr_pid]}")
                        f2.write(f"{curr_pid} - {curr_service[curr_pid]}\n")
                        for_checksum[str(curr_pid)] = str(curr_service[curr_pid])

                self.my_drow.write("services no longer run:")
                f2.write("services no longer run:\n")
                for last_pid in last_service.keys():
                    if last_service[last_pid] not in curr_service.values():
                        self.my_drow.write(f"{last_pid} - {last_service[last_pid]}")
                        f2.write(f"{last_pid} - {last_service[last_pid]}\n")
                        for_checksum[str(last_pid)] = str(last_service[last_pid])
                checksum = self.check_sum(for_checksum)
                f2.write(f"checksum: {checksum}\n")
                f2.close()
                os.system("attrib +h " + "status_log.txt")
            self.services_list.append((curr_time, curr_service))


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
        # print(f"{tup1[0]},{tup1[1]}")
        # writer1 = csv.writer(tup1)

        tup1 = (date, checksum)
        writer.writerow(tup1)
        # print(f"{tup1[0]},{tup1[1]}")
        # writer1 = csv.writer(tup1)

        tup1 = ("pid", "pname")
        writer.writerow(tup1)
        # print(f"{tup1[0]},{tup1[1]}")

        for pid in last_service.keys():
            tup1 = (pid, last_service[pid])
            writer.writerow(tup1)
            # print(f"{tup1[0]},{tup1[1]}")

        f.close()
        os.system("attrib +h " + "serviceList.csv")



    def stop(self):
        self.my_drow.write("the program stop to work")

        self.mon_run = False



    def comper(self, fdate, ftime , tdate, ttime):
        self.load_to_list()
        stringf = f"{fdate} {ftime}"
        stringt = f"{tdate} {ttime}"
        fdate_object = datetime.fromisoformat(stringf)
        tdate_object = datetime.fromisoformat(stringt)
        closest_to_f = self.find_nearest_date(fdate_object)
        closest_to_t = self.find_nearest_date(tdate_object)


        if closest_to_t.timestamp() - closest_to_f.timestamp() > 0:
            recent = closest_to_t
            older = closest_to_f
        else:
            older = closest_to_t
            recent = closest_to_f

        recent_proc = {}
        older_proc = {}
        for tup in self.services_list:
            if str(tup[0]) == str(recent):
                recent_proc = tup[1]
            if str(tup[0]) == str(older):
                older_proc = tup[1]

        self.my_drow.write("new services:")
        for pid in recent_proc:
            if pid not in older_proc or recent_proc[pid] not in older_proc.values():
                self.my_drow.write(f"{pid} - {recent_proc[pid]}")
        self.my_drow.write("old services:")
        for pid in older_proc:
            if pid not in recent_proc or older_proc[pid] not in recent_proc.values():
                self.my_drow.write(f"{pid} - {older_proc[pid]}")



    def find_nearest_date(self, check_date):
        date_list = []
        for i in range(0, len(self.services_list)):
            date_list.append(datetime.fromisoformat(str(self.services_list[i][0])))

        diff_date = {}
        # for date in date_list:
        #     diff_date[abs(check_date.timestamp() - date.timestamp())] = date
        diff_date = {abs(check_date.timestamp()-date.timestamp()):date for date in date_list}
        return diff_date[min(diff_date.keys())]


    def get_sample(self, date, time):
        self.load_to_list()
        string_time = f"{date} {time}"
        date_object = datetime.fromisoformat(string_time)
        closest_to_date = self.find_nearest_date(date_object)

        proc = {}
        for tup in self.services_list:
            if str(tup[0]) == str(closest_to_date):
                proc = tup[1]
        for pid in proc:
            self.my_drow.write(f"{pid} - {proc[pid]}")



