import datetime

def converting_datetime(date):
    """
    Превращает обьект даты в строку, пример - 2023_Apr_17_20h_28m_26s
    """
    return datetime.datetime.strftime(date, '%Y_%b_%d_%Hh_%Mm_%Ss')