import pytest
import workday_calendar
import datetime

@pytest.fixture
def calendar():
    myCalendar = workday_calendar.Calendar("08:00", "16:00")
    return myCalendar

def test_workday_start(calendar):
    assert calendar.workday_start == datetime.datetime.strptime("08:00", "%H:%M").time()

def test_workday_end(calendar):
    assert calendar.workday_end == datetime.datetime.strptime("16:00", "%H:%M").time()

def test_change_workday_start(calendar):
    calendar.setStart("07:00")
    assert calendar.workday_start == datetime.datetime.strptime("07:00", "%H:%M").time()

def test_change_workday_end(calendar):
    calendar.setEnd("15:00")
    assert calendar.workday_end == datetime.datetime.strptime("15:00", "%H:%M").time()

def test_addHoliday(calendar):
    calendar.addHoliday("08/11/2022")
    assert "08/11/2022" in calendar.unique_holidays

def test_addRecurringHoliday(calendar):
    calendar.addRecurringHoliday("22/10")
    assert "22/10" in calendar.recurring_holidays

@pytest.fixture
def calendar_with_holidays():
    myCalendar = workday_calendar.Calendar("08:00", "16:00")
    myCalendar.addHoliday("27/5/2004")
    myCalendar.addRecurringHoliday("17/5")
    return myCalendar

def test_add_workdays(calendar_with_holidays):
    assert calendar_with_holidays.addWorkDays("24/5/2004 19:03", 44.723656) == datetime.datetime.strptime("27-07-2004 13:47", "%d-%m-%Y %H:%M")

def test_subtract_workdays(calendar_with_holidays):
    assert calendar_with_holidays.addWorkDays("24/5/2004 19:03", -6.7470217) == datetime.datetime.strptime("13-05-2004 10:02", "%d-%m-%Y %H:%M")