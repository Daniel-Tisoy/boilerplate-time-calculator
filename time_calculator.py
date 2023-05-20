def get_new_hour(total_min, weekday=None):
    """
    get minutes and turns into

    disclaimer: test are in the add_time function

    """
    result = ""  # this will be the final string

    total_min = int(total_min)

    # get hours without limit of days
    min_to_hour = total_min // 60
    # get days from hours
    hour_to_day = min_to_hour // 24
    # get readeable hour in 24 format
    hour_24 = min_to_hour % 24
    # get minutes
    minutes = total_min % 60

    # get 12 format hour
    hour_12 = convert_12_hour([hour_24, minutes])
    # get the weekday
    if weekday is not None:
        weekday = get_weekday(hour_to_day, weekday)
    # make the string (n days later)
    n_days_later = None
    if hour_to_day == 1:
        n_days_later = "(next day)"
    elif hour_to_day > 1:
        n_days_later = "({} days later)".format(hour_to_day)

    def hour_day_string(hour, dayweek):
        if dayweek is None:
            return hour
        else:
            return f"{hour}, {dayweek}"

    # format the day week and hours
    result = hour_day_string(hour_12, weekday)
    if hour_to_day == 0:
        return result
    else:
        return f"{result} {n_days_later}"


def convert_12_hour(hour_24):
    """
    get a list with hour and minute in 24 hour format and turns
    into a 12 hour string

    >>> convert_12_hour(["14", "34"])
    '2:34 PM'
    """
    # extract into easy readeable variables
    hour = int(hour_24[0])
    minute = int(hour_24[1])
    # here just modify special cases when turning into 12 hour format
    meridiem = "AM"
    if hour == 0:
        hour += 12
    elif hour == 12:
        meridiem = "PM"
    elif hour >= 13:
        hour -= 12
        meridiem = "PM"

    # if the minutes are betwen 0 - 9
    if minute <= 9:
        minute = f"0{minute}"

    # generate the string
    hour_string = "{}:{} {}".format(hour, minute, meridiem)
    return hour_string


def get_weekday(num_days, weekday):
    """
    get number of days and a weekday and returns the corresponding
    weekday adding the number days

    >>> get_weekday(9, "tueSday")
    'Thursday'
    >>> get_weekday(24, "Sunday")
    'Wednesday'
    """
    week = [
        "sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
    ]
    weekday = weekday.lower()
    i = 0
    # find the weekday index in week
    while i <= 6:
        if week[i] == weekday:
            weekday = i
            break
        i += 1
    # if you divide by 7 your getting the number of weeks
    # so the module will return the days in the week
    new_weekday = (weekday + num_days) % 7
    return week[new_weekday].capitalize()


def format_24_hour(time, meridiem):
    """
    get 12 hour format and return a 24 hour format

    >>> format_24_hour(["3", "00"], "PM")
    ['15', '00']
    >>> format_24_hour(["11", "40"], "AM")
    ['11', '40']
    """
    hour = int(time[0])
    afernoon_hours = hour >= 1 and meridiem == "PM"

    if hour == 12 and meridiem == "AM":
        hour -= 12
    elif afernoon_hours:
        hour += 12

    # return the modified hour
    time[0] = str(hour)
    return time


def time_to_minutes(time):
    """
    get the time in a list with hour an minutes and converts it to minutes

    >>> time_to_minutes(["2", "30"])
    150
    """
    # time[0] is the hour
    # time[1] are minutes
    return int(time[0]) * 60 + int(time[1])


def add_time(start, duration, weekday=None):
    """
    add time to the starting hour
    >>> add_time("11:43 AM", "00:20")
    '12:03 PM'
    >>> add_time("11:43 PM", "24:20", "tueSday")
    '12:03 AM, Thursday (2 days later)'
    >>> add_time("10:10 PM", "3:30")
    '1:40 AM (next day)'
    >>> add_time("6:30 PM", "205:12")
    '7:42 AM (9 days later)'
    """
    hour = start[:5].strip()  # get the hour
    meridiem = start[-2:]  # gets the AM or PM

    # convert hours to minutes
    hour_list = hour.split(":")
    dur_list = duration.split(":")
    # get the 24 hour format
    hour_to_24 = format_24_hour(hour_list, meridiem)
    # convert the list to a single number which is the hour in minutes
    hour_to_min = time_to_minutes(hour_to_24)
    dur_to_min = time_to_minutes(dur_list)
    total_min = hour_to_min + dur_to_min

    return get_new_hour(total_min, weekday)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
