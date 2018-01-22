from django import template
import datetime as dt
from datetime import datetime, timezone


register = template.Library()

@register.filter(name='time_elasped')
def time_elapsed(value):
    # time = datetime.combine(date.today(), dt.datetime.strptime('09:30', '%H:%M').time()) - datetime.combine(date.today(), value)
    #now = dt.datetime.now()
    now = datetime.now(timezone.utc)
    print(now)
    time = now - value
    print(time)
    time = str(time)
    position = time.find('day') - 1
    if position != -2:
        if int(time[0:position]) < 365:
            if int(time[0:position]) > 1:
                return time[0:position] + ' days ago'
            else:
                return time[0:position] + ' day ago'
        else:
            time = int(time[0:position]) / 365
            if round(time) > 1:
                return str(round(time)) + ' years ago'
            else:
                return str(round(time)) + ' year ago'

    else:
        position = time.find(':')
        hour = time[0:position]
        minute = time[position + 1:position + 3]
        second = time[position + 4:position + 6]
        if int(hour) != 0:
            if int(minute) >= 30:
                return str(int(hour) + 1) + ' hours ago'
            else:
                if int(hour) > 1:
                    return hour + ' hours ago'
                else:
                    return hour + ' hour ago'

        else:
            if int(minute) != 0:
                if int(second) >= 30:
                    return str(int(minute) + 1) + ' minutes ago'
                else:
                    return str(minute) + ' minutes ago'

            else:
                if int(second) >= 30:
                    return '1 minute ago'
                else:
                    return '0 minutes ago'
    # round value
    # if under 1 minute, display by seconds. if under 1 hour display by minutes. If under one day, display by hours.
    # if over one day display by days. Round.
    # First calculate year difference. Month, day, hour, minute.
    return time
