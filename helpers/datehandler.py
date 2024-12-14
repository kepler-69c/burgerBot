import datetime

def today() -> datetime.date:
    return datetime.date.today()

def is_weekend() -> bool:
    return today().weekday() in [5, 6]

def next_weekday() -> (int, datetime.date, datetime.date):
    """
    if day in {monday-friday} return current day; else return next monday
    """
    today = today()
    weekday = today.weekday()
    requestDayStart = today
    requestDayEnd = today

    if weekday < 5:
        requestDayEnd = today + datetime.timedelta(days=7)
    else:
        daysUntilMonday = 7 - weekday
        requestDayStart = today + datetime.timedelta(days=daysUntilMonday)
        requestDayEnd = requestDayStart + datetime.timedelta(days=7)
        weekday = 0

    return weekday, requestDayStart, requestDayEnd