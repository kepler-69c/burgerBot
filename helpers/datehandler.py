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


def convert_date(date: str) -> datetime.date:
    return datetime.datetime.strptime(date, "%Y%m%d").date()


def is_quiet_date(date: datetime.date, quiet_days: list[str]) -> bool:
    # empty or no quiet days
    if not quiet_days:
        return False

    try:
        for period in quiet_days:
            if "/" in period: # date range
                start_date, end_date = map(convert_date, period.split('/'))
                if start_date <= date <= end_date:
                    return True
            else: # single date
                if convert_date(period) == date:
                    return True
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")

    return False
