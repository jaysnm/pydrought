# -*- coding: utf-8 -*-
#
#..............................................................................
 #  Name        : time_mgt.py
 #  Application : 
 #  Author      : Carolina Arias Munoz
 #  Created     : 2018-08-29
 #                Packages: matplotlib, cartopy
 #  Purpose     : This module contains generic functionality for extracting data 
 #             from and into postgres using Psycopg2                
#..............................................................................


# ..............................................................................
# IMPORTS
# ..............................................................................
import calendar
import datetime
from datetime import timedelta
import numpy as np

# ..............................................................................
# CLASSES
# ..............................................................................

class Week:

    def __init__(self, year, month, day):

        self._start = self._get_start_date_from_params(year, month, day)
        self._end = self._get_end_date_from_start_date()
        self._imput_date = datetime.datetime(year, month, day)



    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def year(self):
        return self._end.year

    @property
    def week(self):
        return self._imput_date.isocalendar()[1]

    def _get_start_date_from_params(self, year, month, day):
        try:
            input_date = datetime.datetime(year, month, day)
            return input_date - timedelta(days=input_date.weekday())
        except:
            raise Exception('Invalid inputs.')

    def _get_end_date_from_start_date(self):
        return self._start + timedelta(days=6)

    def _to_str(self):
        return '{}-{:02d}'.format(self._end.year, self.week)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __neq__(self, other):
        return self.start != other.start or self.end != other.end

    def __add__(self, other):

        if type(other) == int:
            if other < 0:
                return self - abs(other)

            elif other > 1:
                for i in range(other - 1):
                    self = self + 1

            new = self.end + datetime.timedelta(days=1)
            return Week(new.year, new.month, new.day)

        if type(other) == Week:
            dates_list = [self.start + timedelta(i) for i in range(int((other._start -
                                                                        self.start).days) + 1)]
            weeks_list = []
            for day_date in dates_list:
                week_date = Week(day_date.year, day_date.month,
                                   day_date.day)
                if week_date not in weeks_list:
                    weeks_list.append(week_date)
            return weeks_list

    def __sub__(self, num_dekads):

        if num_dekads < 0:
            return self + abs(num_dekads)

        elif num_dekads > 1:
            for i in range(num_dekads - 1):
                self = self - 1

        new = self.start - datetime.timedelta(days=1)
        return Dekad(new.year, new.month, new.day)

    def __repr__(self):
        return '<Week {} of year {}>'.format(self.week, self.year)

    def __hash__(self):
        return hash(self.__repr__())


class Dekad:

    def __init__(self, year, month, day):

        self._year = year
        self._month = month
        self._day = day

    @property
    def start(self):
        return self._get_start_date_from_params(self._year, self._month,
                                                self._day)

    @property
    def end(self):
        return self._get_end_date_from_start_date(self.start)

    @property
    def year(self):
        return self.start.year

    @property
    def month(self):
        return self.start.month

    @property
    def first_day(self):
        return self.start.day

    @property
    def day(self):
        return self.start.day

    @property
    def last_day(self):
        return self.end.day

    @property
    def number(self):
        if self.start.day == 1:
            return self.start.month + 2 * (self.start.month - 1)
        if self.start.day == 11:
            return (self.start.month * 2) + (self.start.month - 1)
        if self.start.day == 21:
            return self.start.month * 3

    def _get_dekad_number(self, start_datetime):
        if start_datetime.day == 1:
            return start_datetime.month + 2 * (start_datetime.month - 1)
        if start_datetime.day == 11:
            return (start_datetime.month * 2) + (start_datetime.month - 1)
        if start_datetime.day == 21:
            return start_datetime.month * 3

    def _get_start_date_from_params(self, year, month, day):
        try:
            input_date = datetime.datetime(year, month, day)
            if input_date.day < 11:
                start_day = 1
            elif input_date.day < 21:
                start_day = 11
            else:
                start_day = 21

            return datetime.datetime(year, month, start_day)

        except:
            raise Exception('Invalid inputs.')

    def _get_end_date_from_start_date(self, start_datetime):

        if start_datetime.day == 21:
            last_day = self._get_last_day_of_month(start_datetime)
        elif start_datetime.day == 11:
            last_day = 20
        elif start_datetime.day == 1:
            last_day = 10
        else:
            raise Exception('Dekad start day should be 1, 11, or 21')

        return datetime.datetime(start_datetime.year, start_datetime.month, last_day)

    def _get_last_day_of_month(self, dt):
        return calendar.monthrange(dt.year, dt.month)[1]

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __neq__(self, other):
        return self.start != other.start or self.end != other.end

    def __add__(self, other):

        if type(other) == int:
            if other < 0:
                return self - abs(other)

            elif other > 1:
                for i in range(other - 1):
                    self = self + 1

            new = self.end + datetime.timedelta(days=1)
            return Dekad(new.year, new.month, new.day)

        if type(other) == Dekad:
            dates_list = [self.start + timedelta(i) for i in range(int((other.start -
                                                                        self.start).days) + 1)]
            dekads_list = []
            for day_date in dates_list:
                dekad_date = Dekad(day_date.year, day_date.month,
                                   day_date.day)
                if dekad_date not in dekads_list:
                    dekads_list.append(dekad_date)
            return dekads_list

    def __sub__(self, num_dekads):

        if num_dekads < 0:
            return self + abs(num_dekads)

        elif num_dekads > 1:
            for i in range(num_dekads - 1):
                self = self - 1

        new = self.start - datetime.timedelta(days=1)
        return Dekad(new.year, new.month, new.day)

    def __repr__(self):
        return '<Dekad {0:04d}-{1:02d}-{2:02d}>'.format(self.start.year, self.start.month, self.start.day)

    def __hash__(self):
        return hash(self.__repr__())

# ..............................................................................
# FUNCTIONS
# ..............................................................................


def filter_dekads_by_id(dekads_list, dekad_id):

    def filter_function(element):
        return element.number == dekad_id

    return filter(filter_function, dekads_list)


def filter_dekads_by_years(dekads_list, years_list):

    def filter_function(element):
        return element.year in years_list

    return filter(filter_function, dekads_list)


def get_date_from_file_name(data_file_name):
    dic = {'WB':'', 'DWD':''}
    for i, j in iter(dic.items()):
        data_file_name = data_file_name.replace(i, j)
    data_date_year = int(data_file_name[0:4])
    data_date_month = int(data_file_name[4:6])
    data_date_day = int(data_file_name[6:8])
    data_date = datetime.date(data_date_year, data_date_month, data_date_day)
    return data_date


def get_date_from_file_name_plusone(data_file_name):
    dic = {'WB':'', 'DWD':''}
    for i, j in iter(dic.items()):
        data_file_name = data_file_name.replace(i, j)
    data_date_year = int(data_file_name[1:5])
    data_date_month = int(data_file_name[5:7])
    data_date_day = int(data_file_name[7:9])
    data_date = datetime.date(data_date_year, data_date_month, data_date_day)
    return data_date

   
def get_dekad(data_date):
    """assign current dekad to a date"""        
    if data_date.day < 11:
        dekad = '01'
    elif data_date.day > 10 and data_date.day < 21:
        dekad = '11' 
    elif data_date.day > 20:
        dekad = '21' 
    return dekad


def get_dekad_ordinalday(data_date):
    """set day of the dekad"""
    """i.e. dekad 11 = [11,12,13,14,15,16,17,18,19,20]
            dekad 11 = [1st,2nd,3rd,4th,....] """
    if data_date.day < 11:
        dekad_ordinalday = data_date.day
    elif data_date.day > 10 and data_date.day < 21:
        dekad_ordinalday = data_date.day - 10
    elif data_date.day > 20:
        dekad_ordinalday = data_date.day - 20
    return dekad_ordinalday


def set_last_YYMMDK(data_date):
    """assign current and previuos dekad to a date"""        
    if data_date.day < 11:
        last_dekad = 21
        last_month = data_date.month - 1
        last_year = data_date.year
        if data_date.month == 1:
            last_dekad = 21
            last_month = 12
            last_year = data_date.year - 1
    elif data_date.day > 10 and data_date.day < 21:
        last_dekad = 1
        last_month = data_date.month
        last_year = data_date.year
    elif data_date.day > 20:
        last_dekad = 11
        last_month = data_date.month
        last_year = data_date.year  
    return last_year,last_month,last_dekad


def set_next_YYMMDK(data_date):
    """assign current and previuos dekad to a date"""      
    if data_date.day < 11:
        next_dekad = 11
        next_month = data_date.month
        next_year = data_date.year 
    if data_date.day > 10 and data_date.day < 21:
        next_dekad = 21
        next_month = data_date.month
        next_year = data_date.year
    if data_date.day > 20:
        next_dekad = 1
        if data_date.month == 12:
            next_year = data_date.year + 1
            next_month = 1
        else:
            next_year = data_date.year 
            next_month = data_date.month + 1
    return next_year,next_month,next_dekad


def get_check_date(today,time_delta):
    check_days = timedelta(days = time_delta)
    check_date = today - check_days
    check_date = (str(check_date.year)+"-"
                  +str(check_date.month).zfill(2)+"-"
                  +str(check_date.day).zfill(2))
#    logger1.info("Checking data since "+check_date+"")
    return check_date


def get_dekad_date(day_date):
    if day_date.day < 11:
        start_day = 1
    elif day_date.day < 21:
        start_day = 11
    else:
        start_day = 21      
    return datetime.date(day_date.year, day_date.month, start_day)


def generate_times_dekad(dekad_date):
    """Calculate next dekad date to calculate the end of the current dekad
    Note: dekad date is always the end of the dekad"""    
    next_year,next_month,next_dekad = set_next_YYMMDK(dekad_date)
    next_dekad_date = datetime.date(next_year, next_month, next_dekad)
#    """Calculate the end of the current dekad"""
#    end_dekad_date = next_dekad_date - timedelta(days = 1)
    """Setting the dates of the dekad days"""
#    dekad_days = np.arange(str(dekad_date), str(next_dekad_date), dtype='datetime64[D]')
#    dekad_days = np.arange(dekad_date, next_dekad_date, timedelta(days=1))
    dekad_days = [dekad_date + datetime.timedelta(days=x) for x in range(0, (next_dekad_date-dekad_date).days)]
    return dekad_days


def get_dekad_days(dekad_date):
    """Calculate next dekad date to calculate the end of the current dekad
    Note: dekad date is always the begining of the dekad"""    
    next_dekad_date = set_next_YYMMDK(dekad_date)
    
    """Calculate the end of the current dekad"""
    end_dekad_date = next_dekad_date - timedelta(days = 1)
       
    """Setting the dates of the dekad days"""
    dekad_days = np.arange(str(dekad_date), str(end_dekad_date), dtype='datetime64[D]')
    return dekad_days


def create_dekads_list(start_date, end_date):
    """Creates a list of dekads in datetime format

    Parameters
    ----------
    start_date
        type: datetime
    end_date
        type: datetime
    Returns
    -------
    list of datetime objects
    type: list

    """
    daily_dates = [start_date + timedelta(i) for i in 
                   range(int ((end_date - start_date).days)+1)]
    dekads_list = []
    for day_date in daily_dates: 
        dekad_date = get_dekad_date(day_date)
        if dekad_date not in dekads_list:
            dekads_list.append(dekad_date)
    return dekads_list


def get_dates(start_date, end_date):
    """Creates a list of daily dates between two dates given as string

    Parameters
    ----------
    start_date
        start date in the format YYYY-MM-DD
        type: string
    end_date
        end date in the format YYYY-MM-DD
        type: string
    Returns
    -------
    list of datetime objects
    type: list

    """
    dates = [start_date + datetime.timedelta(days=x) for x in
             range(0, (end_date - start_date).days)]
    return dates


def get_years(dates):
    """Creates a list of years between two dates given as string

    Parameters
    ----------
    start_date
        start date in the format YYYY-MM-DD
        type: string
    end_date
        end date in the format YYYY-MM-DD
        type: string
    Returns
    -------
    list of datetime objects
    type: list of ints

    """

    years = {}
    for date in dates:
        year = date.year
        if year not in years.keys():
            years[year] = {}
    for year in years.keys():
        dates_list = []
        for date in dates:
            if date.year == year:
                dates_list.append(date)
        years[year] = dates_list
    return years


def get_months(start_date, end_date):
    """Creates a list of month dates between two dates given as string
    day corresponds to the first day of the month = 1
    Parameters
    ----------
    start_date
        start date in the format YYYY-MM-DD
        type: string
    end_date
        end date in the format YYYY-MM-DD
        type: string
    Returns
    -------
    list of datetime objects
    type: list of ints

    """
    dates = get_dates(start_date, end_date)
    months_dates = []
    for date in dates:
        year = date.year
        month = date.month
        day = 1
        month_date = datetime.datetime(year, month, day)
        if month_date not in months_dates:
            months_dates.append(month_date)
    return months_dates


def get_dates_list(start_date, end_date, frequency):
    """Creates a list of month dates between two dates given as string
    day corresponds to the first day of the month = 1
    Parameters
    ----------
    start_date
        start date in the format YYYY-MM-DD
        type: string
    end_date
        end date in the format YYYY-MM-DD
        type: string
    frequency
        weekly 'w', monthly 'm', daily 'd', dekadly 't'
    Returns
    -------
    list of datetime objects
    type: list
    """
    start_date = datetime.datetime(int(start_date.split('-')[0]),
                                   int(start_date.split('-')[1]),
                                   int(start_date.split('-')[2]))
    end_date = datetime.datetime(int(end_date.split('-')[0]),
                                 int(end_date.split('-')[1]),
                                 int(end_date.split('-')[2]))
    if frequency == "w":
        start_week = Week(start_date.year, start_date.month, start_date.day)
        end_week = Week(end_date.year, end_date.month, end_date.day)
        return start_week + end_week
    if frequency == "m":
        return get_months(start_date, end_date)
    if frequency == "t":
        start_dekad = Dekad(start_date.year, start_date.month, start_date.day)
        end_dekad = Dekad(end_date.year, end_date.month, end_date.day)
        return start_dekad + end_dekad
    if frequency == "d":
        return get_dates(start_date, end_date)
    if frequency == "md":
        return get_months(start_date, end_date)


def get_last_timestamp(timestamp, frequency):
    """Creates a list of month dates between two dates given as string
    day corresponds to the first day of the month = 1
    Parameters
    ----------
    start_date
        start date in the format YYYY-MM-DD
        type: string
    end_date
        end date in the format YYYY-MM-DD
        type: string
    frequency
        weekly 'w', monthly 'm', daily 'd', dekadly 't'
    Returns
    -------
    list of datetime objects
    type: list
    """

    if frequency == "w":
        current_week = Week(timestamp.year, timestamp.month, timestamp.day)
        return current_week - 1
    if frequency == "m":
        return get_months(start_date, end_date)
    if frequency == "t":
        start_dekad = Dekad(start_date.year, start_date.month, start_date.day)
        end_dekad = Dekad(end_date.year, end_date.month, end_date.day)
        return start_dekad + end_dekad
    if frequency == "d":
        return get_dates(start_date, end_date)