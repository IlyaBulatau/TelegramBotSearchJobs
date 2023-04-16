import datetime

def converting_datetime(date):
    return datetime.datetime.strftime(date, '%Y_%b_%d_%Hh_%Mm_%Ss')