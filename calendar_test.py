import pytest
import workday_calendar
import datetime

@pytest.fixture
def calendar():
    myCalendar = workday_calendar.Calendar("08:00", "16:00")
    return myCalendar

def test_initial_workday_start(calendar):
    assert calendar.workday_start == datetime.datetime.strptime("08:00", "%H:%M").time()

def test_initial_workday_end(calendar):
    assert calendar.workday_end == datetime.datetime.strptime("16:00", "%H:%M").time()

@pytest.mark.parametrize("start, end, holidays, recurring_holiday", [
    ("08:00", "16:00", "27/2/2022", "26/3"),
    ("07:00", "15:00", "22/10/2022", "24/5"),
])

def test_change_workday_start(calendar, start, end, holidays, recurring_holiday):
    calendar.setStart(start)
    assert calendar.workday_start == datetime.datetime.strptime(start, "%H:%M").time()

@pytest.mark.parametrize("end", [
    ("16:00"),
    ("15:00"),
])

def test_change_workday_end(calendar, end):
    calendar.setEnd(end)
    assert calendar.workday_end == datetime.datetime.strptime(end, "%H:%M").time()

@pytest.mark.parametrize("holiday", [
    ("27/02/2022"),
    ("14/07/2022"),
])

def test_addHoliday(calendar, holiday):
    calendar.addHoliday(holiday)
    assert holiday in calendar.unique_holidays

@pytest.mark.parametrize("recurring_holiday", [
    ("21/11"),
    ("22/12"),
])

def test_addRecurringHoliday(calendar, recurring_holiday):
    calendar.addRecurringHoliday(recurring_holiday)
    assert recurring_holiday in calendar.recurring_holidays

@pytest.fixture
def calendar_with_holidays(calendar):
    calendar.addHoliday("27/5/2004")
    calendar.addRecurringHoliday("17/5")
    return calendar

@pytest.mark.parametrize("start_time, workdays, expected", [
    ("24/5/2004 19:03", 44.723656, "27-07-2004 13:47"),
    ("24/5/2004 18:03", -6.7470217, "13-05-2004 10:02"),
])

def test_add_workdays(calendar_with_holidays, start_time, workdays, expected):
    assert calendar_with_holidays.addWorkDays(start_time, workdays) == datetime.datetime.strptime(expected, "%d-%m-%Y %H:%M")