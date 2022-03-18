
from datetime import datetime
from dateutil import parser
"""
Class for api queries
"""
class db:
    """
    Returns all column values between two datetimes
    """
    def db_fetch(column_name: str, start: str, end: str, cur) -> tuple:
        
        start = db.URLtimeToDatetime(start)
        end = db.URLtimeToDatetime(end)
        cur.execute("""SELECT {0} FROM elering_data
        WHERE ts >= %(start)s AND ts <= %(end)s;""".format(column_name),
        {'column_name': column_name, 'start': start, 'end':end })
        return(cur.fetchall())
    """
    Takes time from parsed from URL and returns datetime
    """
    def URLtimeToDatetime(URLtime:str) -> datetime:
        return(parser.isoparse(URLtime))
        