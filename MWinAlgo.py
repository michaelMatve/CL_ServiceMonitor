
class MWinAlgo:
    def __init__(self, mdrow):
        self.my_drow = mdrow
        self.mon_run = False
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


    def stop(self):
        self.my_drow.write("the program stop to work")

        self.mon_run = False

    def comper(self, fdate, ftime , tdate, ttime):
        self.my_drow.write(f"{fdate} {ftime} comper to {tdate} {ttime}")
