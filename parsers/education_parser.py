from datetime import datetime
from dateutil import parser
import numpy as np

DEGREES = ['b', 'm', 'a', 'c', 'd', 'p', 's', 'h', 'e', 'g', 'i', 'f', 't', 'l', 'n']


def convert_lower_case(data):
    return np.char.lower(data)


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data


def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    return str(data)


def get_last_education_time(educations):
    edu_times = []

    for edu in educations:
        edu_times += edu.get('time')

    edu_times = [et for et in edu_times if et != 'notKnown']
    latest_education_time = max(edu_times, default=None)

    return latest_education_time


def get_highest_degree_level(educations):
    degrees = set()

    for edu in educations:
        degrees.add(preprocess(edu.get('degree')[:1]))

    return ''.join(sorted(degrees))


def get_proxy_for_degree(educations):
    degree_proxy = []

    degrees = get_highest_degree_level(educations)
    return [(deg in degrees) for deg in DEGREES]


def time_since_last_education(educations):
    try:

        stime = get_last_education_time(educations)
        t1 = parser.parse(stime)

        s2 = datetime.today().strftime("%Y-%m-%d")
        t2 = parser.parse(s2)
        timedelta = t2 - t1
        return timedelta.days
    except Exception as e:
        # For now catching all exceptions
        # Before sending to production catch specific exception
        return None
