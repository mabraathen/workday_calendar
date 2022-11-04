import datetime
import utils

class Calendar:
    def __init__(self, workday_start, workday_end):
        self.workday_start = datetime.datetime.strptime(workday_start, "%H:%M").time()
        self.workday_end = datetime.datetime.strptime(workday_end, "%H:%M").time()
        self.recurring_holidays = []
        self.unique_holidays = []

    #main method for adding workdays from input
    def addWorkDays(self, datetime_start, workdays):
        datetime_start = datetime.datetime.strptime(datetime_start, "%d/%m/%Y %H:%M")
        minutes, days = utils.numberToTime(self, workdays)
        final_datetime = datetime.datetime(2000, 1, 1, 1, 1)
        if workdays > 0:
            final_datetime = utils.addDays(self, datetime_start, minutes, days)
        elif workdays < 0:
            final_datetime = utils.subtractDays(self, datetime_start, minutes, days)
        else:
            print("Error, workdays must not be 0!")
        return final_datetime

    #method to check if a day is a workday or not
    #a workday is a day that is not a unique holiday, recurring holiday or on a weekend
    #if a certain day turns out to not be a workday, we skip it and move on
    def isWorkday(self, date, operator):
        #need to do checks untill all 3 passes, for edge cases where weekends and holidays may be adjacent
        checks = [0, 0, 0]
        while sum(checks) < 3:
            date, checks[2] = utils.isWeekend(self, date, operator)
            date, checks[0] = utils.isUniqueHoliday(self, date, operator)
            date, checks[1] = utils.isRecurringHoliday(self, date, operator)
        return date

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
    #example creating of the calendar, and setting up example work hours, format "hours:minutes"
    myCalendar = Calendar("08:00", "16:00")
    #single holiday example, format "day/month/year"
    myCalendar.addHoliday("27/5/2004")
    #recurring holiday example, format "day/month"
    myCalendar.addRecurringHoliday("17/5")
    #example task, inputs are specified point in time with format "day/month/year hours:minutes" and with an amount of working days to said specified time (does not need to be an integer and can be negative)
    print("final result: ", myCalendar.addWorkDays("24/5/2004 07:03", -6.7470217))