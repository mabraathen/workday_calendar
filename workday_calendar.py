import datetime
import holidays
import math

########################################################################
#TODO
#
#tester
#lage tekst ui for bruker (sørge for at input blir sjekka og gjort riktig format)
#
#
########################################################################



class Calendar:

    def __init__(self, workday_start, workday_end):
        self.workday_start = datetime.datetime.strptime(workday_start, "%H:%M").time()
        self.workday_end = datetime.datetime.strptime(workday_end, "%H:%M").time()
        self.recurring_holidays = []
        self.unique_holidays = []

    #main method for adding workdays from input
    def addWorkDays(self, datetime_start, workdays):
        datetime_start = datetime.datetime.strptime(datetime_start, "%d/%m/%Y %H:%M")
        minutes, days = self.numberToTime(workdays)
        final_datetime = datetime.datetime(2000, 1, 1, 1, 1)
        if workdays > 0:
            final_datetime = self.addDays(datetime_start, minutes, days)
        elif workdays < 0:
            final_datetime = self.subtractDays(datetime_start, minutes, days)
        else:
            print("Error, workdays must not be 0!")

        return final_datetime

    #convert integer and decimal of input to days and minutes
    def numberToTime(self, number):
        decimal, integer = math.modf(number)
        workday_minutes = (self.workday_end.hour * 60 + self.workday_end.minute) - (self.workday_start.hour * 60 + self.workday_start.minute)
        returned_minutes = workday_minutes * abs(decimal)
        #was originally using python round() function to round off number of minutes
        #but some of your attached correct result examples in the task seemed to be using floor here so i did as well to match the result
        return math.floor(abs(returned_minutes)), int(integer)

    #method for adding days from starting time
    def addDays(self, datetime_start, minutes, days):
        returned_date = datetime_start
        returned_date_time = datetime.time(returned_date.hour, returned_date.minute)
        #check if the given start time is within workday hours, and move it if it isn't
        if returned_date_time < self.workday_start:
            returned_date = returned_date.replace(hour=self.workday_start.hour, minute=self.workday_start.minute)
        elif returned_date_time > self.workday_end:
            returned_date = returned_date.replace(hour=self.workday_start.hour, minute=self.workday_start.minute)
            returned_date += datetime.timedelta(days=1)
        else:
            print("Looks like start time is within working time :)")

        #add minutes to the given start time, and check if its still within workday hours
        #if not, move it to the next day
        returned_date_time = datetime.time(returned_date.hour, returned_date.minute)
        minutes_left = (self.workday_end.hour * 60 + self.workday_end.minute) - (returned_date_time.hour * 60 + returned_date_time.minute)
        if minutes_left < minutes:
            returned_date = returned_date.replace(hour=self.workday_start.hour, minute=self.workday_start.minute)
            returned_date += datetime.timedelta(days=1)
            returned_date += datetime.timedelta(minutes=(minutes-minutes_left))
        else:
            returned_date += datetime.timedelta(minutes=minutes)
        
        #add all days, and make sure to account for if a day is a workday or not
        for i in range(abs(days)):
            returned_date = self.isWorkday(returned_date, 1)
            returned_date += datetime.timedelta(days=1)
        return returned_date

    #method for subtracting days from starting time
    def subtractDays(self, datetime_start, minutes, days):
        returned_date = datetime_start
        returned_date_time = datetime.time(returned_date.hour, returned_date.minute)
        #check if the given start time is within workday hours, and move it if it isn't
        if returned_date_time < self.workday_start:
            returned_date = returned_date.replace(hour=self.workday_end.hour, minute=self.workday_end.minute)
            returned_date -= datetime.timedelta(days=1)
        elif returned_date_time > self.workday_end:
            returned_date = returned_date.replace(hour=self.workday_end.hour, minute=self.workday_end.minute)
        else:
            print("Looks like start time is within working time :)")

        #subtract minutes to the given start time, and check if its still within workday hours
        #if not, move it to the previous day
        returned_date_time = datetime.time(returned_date.hour, returned_date.minute)
        minutes_left = (returned_date_time.hour * 60 + returned_date_time.minute) - (self.workday_start.hour * 60 + self.workday_start.minute)
        if minutes_left < minutes:
            returned_date = returned_date.replace(hour=self.workday_end.hour, minute=self.workday_end.minute)
            returned_date -= datetime.timedelta(days=1)
            returned_date -= datetime.timedelta(minutes=(minutes-minutes_left))
        else:
            returned_date -= datetime.timedelta(minutes=minutes)
        
        #add all days, and make sure to account for if a day is a workday or not
        for i in range(abs(days)):
            returned_date -= datetime.timedelta(days=1)
            returned_date = self.isWorkday(returned_date, -1)
            print(returned_date)
        return returned_date

    #method to check if a day is a workday or not
    #a workday is a day that is not a unique holiday, recurring holiday or on a weekend
    #if a certain day turns out to not be a workday, we skip it and move on
    def isWorkday(self, date, operator):
        #need to do checks untill all 3 passes, for edge cases where weekends and holidays may be adjacent
        checks = [0, 0, 0]
        while sum(checks) < 3:
            date, checks[2] = self.isWeekend(date, operator)
            date, checks[0] = self.isUniqueHoliday(date, operator)
            date, checks[1] = self.isRecurringHoliday(date, operator)
        return date

    #checks if input date is on a holiday, and moves returned date either after or before said holiday, depending on if we are subtracting or adding days
    def isRecurringHoliday(self, date, operator):
        new_date = date
        holiday = True
        passed_check = 1
        while(holiday):
            date_string = new_date.strftime("%d/%m")
            if date_string not in self.recurring_holidays:
                holiday = False
            else:
                passed_check = 0
                if operator > 0:
                    new_date += datetime.timedelta(days=1)
                else:
                    new_date -= datetime.timedelta(days=1)
        return new_date, passed_check

    #same as isRecurringHoliday, just checks the single holidays instead
    def isUniqueHoliday(self, date, operator):
        new_date = date
        holiday = True
        passed_check = 1
        while(holiday):
            date_string = new_date.strftime("%d/%m/%Y")
            if date_string not in self.unique_holidays:
                holiday = False
            else:
                passed_check = 0
                if operator > 0:
                    new_date += datetime.timedelta(days=1)
                else:
                    new_date -= datetime.timedelta(days=1)
        return new_date, passed_check

    #checks if input date is in a weekend, and moves returned date either after or before weekend, depending on if we are subtracting or adding days
    def isWeekend(self, date, operator):
        new_date = date
        weekend = True
        passed_check = 1
        while(weekend):
            if operator > 0:
                if new_date.weekday() == 5:
                    passed_check = 0
                    new_date += datetime.timedelta(days=2)
                elif new_date.weekday() == 6:
                    passed_check = 0
                    new_date += datetime.timedelta(days=1)
                else:
                    weekend = False
            else:
                if new_date.weekday() == 5:
                    passed_check = 0
                    new_date -= datetime.timedelta(days=1)
                elif new_date.weekday() == 6:
                    passed_check = 0
                    new_date -= datetime.timedelta(days=2)
                else:
                    weekend = False
        return new_date, passed_check

    #adds a new sinle holiday to the calendar
    def addHoliday(self, date):
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        date = date.strftime("%d/%m/%Y")
        self.unique_holidays.append(date)

    #adds a new recurring holiday to the calendar
    def addRecurringHoliday(self, date):
        date = datetime.datetime.strptime(date, "%d/%m").date()
        date = date.strftime("%d/%m")
        self.recurring_holidays.append(date)

    def setStart(self, start):
        self.workday_start = datetime.datetime.strptime(start, "%H:%M").time()
    
    def getStart(self):
        return self.workday_start

    def setEnd(self, end):
        self.workday_end = datetime.datetime.strptime(end, "%H:%M").time()
    
    def getEnd(self):
        return self.workday_end

if __name__ == "__main__":
    #example creating of the calendar, and setting up example work hours, format HH:mm
    myCalendar = Calendar("08:00", "16:00")

    #single holiday example
    myCalendar.addHoliday("27/5/2004")

    #recurring holiday example
    myCalendar.addRecurringHoliday("17/5")

    #example task
    print("final result: ", myCalendar.addWorkDays("24/5/2004 07:03", -6.7470217))