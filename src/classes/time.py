import datetime

class Time:
    def __init__(self,final_index):
        # The night starts at 6 PM on an arbitrary day
        self.start_time = datetime.datetime(1900,1,1,hour=18, minute=0)
        self.final_index = final_index
        self.final_time = self.start_time + datetime.timedelta(minutes=final_index * 10)

    def index_to_time(self,index):
        # Lists don't have negative indices!
        if index < 0: index = 0
        delta = datetime.timedelta(minutes=index * 10)
        time = self.start_time + delta
        # Index cannot go over final index!
        if index < self.final_index:
            return self.start_time + delta
        else:
            return self.final_time

    def time_to_index(self,time):
        delta = time - self.start_time
        index = delta // datetime.timedelta(minutes=10)
        # Index can't go over final_index!
        if index > self.final_index:
            return self.final_index
        else:
            return index

    def index_to_string(self,index):
        time = self.index_to_time(index)
        return time.strftime("%H:%M")

    def time_to_string(self,time):
        return time.strftime("%H:%M")

    def string_to_time(self,string):
        # Return None if converting to string fails
        try:
            time = datetime.datetime.strptime(string, "%H:%M")
        except:
            return None
        if time < self.start_time:
            time += datetime.timedelta(days=1)
        return time

    def string_to_index(self,string):
        # Return None if converting to string fails
        try:
            time = datetime.datetime.strptime(string, "%H:%M")
        except:
            return None
        if time < self.start_time:
            time += datetime.timedelta(days=1)
        return self.time_to_index(time)
