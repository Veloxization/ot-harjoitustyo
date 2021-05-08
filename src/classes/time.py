import datetime

class Time:
    """The class that works more in the background, making sure the time works
    realistically and correct.

    Attributes:
        start_time: The time when the scenario starts. Always at 18:00. The day
                    is arbitrarily set to 1st of January 1900.
        final_index: The time index when the scenario ends (when the body is
                        reported).
        final_time: The time when the scenario ends.
    """
    def __init__(self,final_index):
        """Constructor that creates a new Time object.

        Args:
            final_index: The time index when the scenario ends.
        """

        # The night starts at 6 PM on an arbitrary day
        self.start_time = datetime.datetime(1900,1,1,hour=18, minute=0)
        self.final_index = final_index
        self.final_time = self.start_time + datetime.timedelta(minutes=final_index * 10)

    def index_to_time(self,index):
        """Converts a time index into a datetime object.

        Args:
            index: The time index to convert.
        """

        # Lists don't have negative indices!
        if index < 0:
            index = 0
        delta = datetime.timedelta(minutes=index * 10)
        # Index cannot go over final index!
        if index < self.final_index:
            return self.start_time + delta
        return self.final_time

    def time_to_index(self,time):
        """Converts a datetime object into a time index.

        Args:
            time: The datetime object being converted.
        """

        delta = time - self.start_time
        index = delta // datetime.timedelta(minutes=10)
        # Index can't go over final_index!
        if index > self.final_index:
            return self.final_index
        return index

    def index_to_string(self,index):
        """Converts a time index into a readable time.

        Args:
            index: The time index to convert.
        """

        time = self.index_to_time(index)
        return time.strftime("%H:%M")

    def time_to_string(self,time):
        """Converts a datetime object into a readable time.

        Args:
            time: The datetime object to convert.
        """

        return time.strftime("%H:%M")

    def string_to_time(self,string):
        """Converts a time string into a datetime object.

        Args:
            string: The string to convert.
        """

        # Return None if converting to string fails
        try:
            time = datetime.datetime.strptime(string, "%H:%M")
        except:
            return None
        if time < self.start_time:
            time += datetime.timedelta(days=1)
        return time

    def string_to_index(self,string):
        """Converts a time string into a time index.

        Args:
            string: The string to convert.
        """
        # Return None if converting to string fails
        try:
            time = datetime.datetime.strptime(string, "%H:%M")
        except:
            return None
        if time < self.start_time:
            time += datetime.timedelta(days=1)
        return self.time_to_index(time)
