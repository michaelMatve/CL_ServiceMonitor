


class MLinAlgo:
    def __init__(self, mdrow):
        self.my_drow = mdrow

    def start(self,refresh_time):
        self.my_drow.write("the program start to work")

    def stop(self):
        self.my_drow.write("the program stop to work")

    def comper(self, fdate, ftime , tdate, ttime):
        self.my_drow.write(f"{fdate} {ftime} comper to {tdate} {ttime}")