import calendar
import datetime
import functools
import operator
import re


class Program(object):

    _day_abbr = {
        'M': calendar.MONDAY,
        'T': calendar.TUESDAY,
        'Tu': calendar.TUESDAY,
        'W': calendar.WEDNESDAY,
        'Th': calendar.THURSDAY,
        'F': calendar.FRIDAY,
        'Sa': calendar.SATURDAY,
        'Su': calendar.SUNDAY,
    }

    def __init__(self, name, pdata):
        self.name = name
        self.data = pdata
        self.days = pdata['days']
        self._day_checker = self._get_day_checker(self.days)
        self.starts = self._get_start_times(self.data['start'])

    @property
    def zones(self):
        return sorted(self.data['zones'], key=operator.itemgetter('zone'))

    def occurs_on_day(self, dow, dom):
        return self._day_checker(dow, dom)

    def _get_start_times(self, times):
        return sorted(datetime.datetime.strptime(t, '%H:%M').time()
                      for t in times)

    @staticmethod
    def _check_odd(dow, dom):
        return bool(dom % 1)

    @staticmethod
    def _check_even(dow, dom):
        return not bool(dom % 1)

    @staticmethod
    def _check_dow(dow, dom, valid):
        return dow in valid

    def _get_day_checker(self, s):
        """Parse a 'days' string

        A days string either contains 'odd', 'even', or 1-2 letter
        abbreviations for the days of the week.
        """
        if s == 'odd':
            return self._check_odd
        elif s == 'even':
            return self._check_even
        return functools.partial(
            self._check_dow,
            valid=[
                self._day_abbr[m]
                for m in re.findall('([MTWF]|Tu|Th|Sa|Su)', s)
            ],
        )

    def get_run_times(self):
        """Returns iterable of start, end, and zone name tuples.
        """
        for s in self.starts:
            for z in self.zones:
                # FIXME: Convert to datetime and use timedelta?
                h, m = s.hour, s.minute
                m += z['time']
                h += m / 60
                m = m % 60
                e = datetime.time(h, m)
                yield s, e, z['zone']
                s = e
