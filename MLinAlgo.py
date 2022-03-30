from datetime import datetime
import csv
import time
import zlib
import psutil


class MLinAlgo:
    def __init__(self, mdrow):
        self.my_drow = mdrow
        self.mon_run = False
        self.services_list = []

    def start(self, refresh_time):
        self.my_drow.write("the program start to work")
        new_time = refresh_time.split(":")
        new_time = ((int(new_time[0]) * 60) + int(new_time[1])) * 60 + int(new_time[2])
        self.load_to_list()
        self.check_hacked()
        while (self.mon_run):
            self.load_to_list()
            self.check_hacked()
            self.compare_services()  # compare between services - prints to user, and write in status_log
            self.write_to_servicelist()  # write into serviceList the last sample of services according to date and checksum
            time.sleep(new_time)

    def load_to_list(self):
        f = open(".serviceList.csv", 'a')
        f.close()

        with open(".serviceList.csv", 'r') as file:
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
                            self.my_drow.throwalert(f"someone change servies_file !!!!!!!!!!!!!!!!!!!!!!!!\n in date: {date}")
                            self.my_drow.stop()
                            return
                    flag_exist = True
                else:
                    self.services_list[-1][1][int(line[0])] = line[1]

            if checksum is not None:
                if int(self.check_sum(self.services_list[-1][1])) != int(checksum):
                    self.my_drow.throwalert(f"someone change servies_file !!!!!!!!!!!!!!!!!!!!!!!!\n in date: {date}")
                    self.my_drow.stop()
                    return
            self.mon_run = True

    def check_hacked(self):
        f = open(".status_log.txt", 'a')
        f.close()

        check_dict_new = {}
        check_dict_old = {}
        flag = False
        date = None
        f = open(".status_log.txt", 'r')
        lines = f.readlines()
        for line in lines:
            if line.split()[0] == "date:":
                date = line
                pass
            elif line.split()[0] == "new":
                flag = True
                pass
            elif line.split()[0] == "services":
                flag = False
                pass
            elif line.split()[0] == "checksum:":
                checksum = str(line.split()[1])
                comp_checksum1 = self.check_sum(check_dict_new)
                comp_checksum2 = self.check_sum(check_dict_old)
                total_checksum = comp_checksum1 + comp_checksum2
                if checksum != str(total_checksum):
                    self.my_drow.throwalert(f"someone changed the status_log !!!!!\n {date}")
                    self.my_drow.stop()
                    return
                else:
                    check_dict_new = {}
                    check_dict_old = {}
            elif flag:
                pid = line.split(' - ')[0]
                pname = line.split(' - ')[1][:-1]
                check_dict_new[str(pid)] = str(pname)
            elif not flag:
                pid = line.split(' - ')[0]
                pname = line.split(' - ')[1][:-1]
                check_dict_old[str(pid)] = str(pname)

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
        change = False
        for_checksum_new = {}
        for_checksum_old = {}

        self.my_drow.write(f"{curr_time} :")
        if not self.services_list:
            f2 = open(".status_log.txt", "a")
            f2.write(f"date: {curr_time}\n")
            self.my_drow.write("new services:")
            f2.write("new services:\n")
            for proc in psutil.process_iter():
                curr_service[proc.pid] = str(proc.name())
                self.my_drow.write(f"{proc.pid} {proc.name()}")
                f2.write(f"{str(proc.pid)} - {str(proc.name())}\n")
                for_checksum_new[str(proc.pid)] = str(proc.name())
            self.services_list.append((curr_time, curr_service))
            checksum = self.check_sum(for_checksum_new)
            f2.write(f"checksum: {checksum}\n")
            f2.close()

        else:
            last_service = self.services_list[-1][1]
            for proc in psutil.process_iter():
                curr_service[proc.pid] = str(proc.name())
                if proc.name() not in last_service.values():
                    change = True

            for last_pid in last_service.keys():
                if last_service[last_pid] not in curr_service.values():
                    change = True

            if not change:
                self.my_drow.write("nothing has changed!:")
            else:
                f2 = open(".status_log.txt", "a")
                self.my_drow.write("new services:")
                f2.write(f"date: {curr_time}\n")
                f2.write("new services:\n")
                for curr_pid in curr_service.keys():
                    if curr_service[curr_pid] not in last_service.values():
                        self.my_drow.write(f"{curr_pid} - {curr_service[curr_pid]}")
                        f2.write(f"{curr_pid} - {curr_service[curr_pid]}\n")
                        for_checksum_new[str(curr_pid)] = str(curr_service[curr_pid])

                self.my_drow.write("services no longer run:")
                f2.write("services no longer run:\n")
                for last_pid in last_service.keys():
                    if last_service[last_pid] not in curr_service.values():
                        self.my_drow.write(f"{last_pid} - {last_service[last_pid]}")
                        f2.write(f"{last_pid} - {last_service[last_pid]}\n")
                        for_checksum_old[str(last_pid)] = str(last_service[last_pid])
                checksum = self.check_sum(for_checksum_new)
                checksum2 = self.check_sum(for_checksum_old)
                total = int(checksum) + int(checksum2)
                f2.write(f"checksum: {str(total)}\n")
                f2.close()
            self.services_list.append((curr_time, curr_service))

    def write_to_servicelist(self):
        # file look like :
        # date, checksum
        # actualdate, calc_checksum
        # pid, pname
        # actual_pid, pname

        date = self.services_list[-1][0]
        last_service = self.services_list[-1][1]
        checksum = self.check_sum(last_service)

        f = open(".serviceList.csv", "a", newline="")
        # f1 = open("serviceList_enc.csv", "a", newline="")
        writer = csv.writer(f)
        # writer1 = csv.writer(f1)

        tup1 = ("date", "checksum")
        writer.writerow(tup1)
        # print(tup1[0],tup1[1])
        # writer1 = csv.writer(tup1)

        tup1 = (date, checksum)
        writer.writerow(tup1)
        # print(tup1[0],tup1[1])
        # writer1 = csv.writer(tup1)

        tup1 = ("pid", "pname")
        writer.writerow(tup1)
        # print(tup1[0],tup1[1])

        for pid in last_service.keys():
            tup1 = (pid, last_service[pid])
            writer.writerow(tup1)
            # print(tup1[0],tup1[1])

        f.close()

    def stop(self):
        self.my_drow.write("the program stop to work")

        self.mon_run = False

    def comper(self, fdate, ftime, tdate, ttime):
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

        title = f"{recent} \ncompare to \n{older} :\n closest time to what was given original\n "

        recent_proc = {}
        older_proc = {}
        for tup in self.services_list:
            if str(tup[0]) == str(recent):
                recent_proc = tup[1]
            if str(tup[0]) == str(older):
                older_proc = tup[1]
        text = "new services: \n"
        # self.my_drow.write("new services:")
        for pid in recent_proc:
            if pid not in older_proc or recent_proc[pid] not in older_proc.values():
                text +=f"{pid} - {recent_proc[pid]} \n"
                # self.my_drow.write(f"{pid} - {recent_proc[pid]}")
        # self.my_drow.write("old services:")
        text += "old services: \n"
        for pid in older_proc:
            if pid not in recent_proc or older_proc[pid] not in recent_proc.values():
                text += f"{pid} - {older_proc[pid]} \n"
                # self.my_drow.write(f"{pid} - {older_proc[pid]}")
        self.my_drow.writeIN_new_window(title,text)


    def find_nearest_date(self, check_date):
        date_list = []
        for i in range(0, len(self.services_list)):
            date_list.append(datetime.fromisoformat(str(self.services_list[i][0])))

        diff_date = {}
        # for date in date_list:
        #     diff_date[abs(check_date.timestamp() - date.timestamp())] = date
        diff_date = {abs(check_date.timestamp() - date.timestamp()): date for date in date_list}
        return diff_date[min(diff_date.keys())]
    
    
    
    def get_sample(self, date, time):
        self.load_to_list()
        string_time = f"{date} {time}"
        date_object = datetime.fromisoformat(string_time)
        closest_to_date = self.find_nearest_date(date_object)
        title = f"the servies from {closest_to_date}:\n we take the closest date for what asked\n"
        proc = {}
        text = ""
        for tup in self.services_list:
            if str(tup[0]) == str(closest_to_date):
                proc = tup[1]
        for pid in proc:
            text+= f"{pid} - {proc[pid]}\n"
            # self.my_drow.write(f"{pid} - {proc[pid]}")
        self.my_drow.writeIN_new_window(title,text)
