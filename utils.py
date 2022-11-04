import math
import datetime

#convert integer and decimal of input to days and minutes
def numberToTime(self, number):
    decimal, integer = math.modf(number)
    workday_minutes = (self.workday_end.hour * 60 + self.workday_end.minute) - (self.workday_start.hour * 60 + self.workday_start.minute)
    returned_minutes = workday_minutes * abs(decimal)
    #was originally using python round() function to round off number of minutes
    #but some of your attached correct result examples in the task seemed to be using floor here so i did as well to match the result
    return math.floor(abs(returned_minutes)), int(integer)

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
        print("Looks like start time is within working hours :)")

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
    return returned_date