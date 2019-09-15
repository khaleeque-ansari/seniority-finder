from datetime import datetime
from dateutil import parser


def get_time_difference(s1, s2):
    t1 = parser.parse(s1)

    if s2 in ['Present', 'current', 'Current', 'Till Date']:
        s2 = datetime.today().strftime("%Y-%m-%d")

    t2 = parser.parse(s2)
    timedelta = t2 - t1
    return timedelta


def get_longest_tenure(experiences):
    exp_times = []

    for exp in experiences:
        try:
            t1, t2 = exp.get('time')
            timedelta = get_time_difference(t1, t2)
            exp_times.append(timedelta.days)
        except Exception as e:
            print(e)

    return max(exp_times, default=0), sum(exp_times)
