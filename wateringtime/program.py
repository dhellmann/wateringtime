import calendar
import datetime
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
        self._day_checker = self._make_day_checker(self.days)

    @property
    def zones(self):
        """Returns the zones used in the program, sorted by zone id.
        """
        return sorted(self.data['zones'], key=operator.itemgetter('zone'))

    def occurs_on_day(self, dow, dom):
        """Tests whether the program runs on a given day.

        :param dow: Day of week
        :param dom: Day of month
        """
        return self._day_checker(dow, dom)

    @property
    def duration(self):
        """How long does the program run in total?
        """
        return sum(
            z['time']
            for z in self.data['zones']
        )

    @property
    def run_times(self):
        """Returns iterable of start, end, and zone name tuples.
        """
        for s in self.start_times:
            for z in self.zones:
                # FIXME: Convert to datetime and use timedelta?
                h, m = s.hour, s.minute
                m += z['time']
                h += m // 60
                m = m % 60
                e = datetime.time(h, m)
                yield s, e, z['zone']
                s = e

    @property
    def start_times(self):
        return sorted(datetime.datetime.strptime(t, '%H:%M').time()
                      for t in self.data['start'])

    def _make_day_checker(self, s):
        """Parse a 'days' string

        A days string either contains 'odd', 'even', or 1-2 letter
        abbreviations for the days of the week.
        """
        if s == 'odd':
            return lambda dow, dom: bool(dom % 2)
        elif s == 'even':
            return lambda dow, dom: not bool(dom % 2)
        else:
            valid = [
                self._day_abbr[m]
                for m in re.findall('([MWF]|Tu|Th|Sa|Su)', s)
            ]
            return lambda dow, dom, valid=valid: dow in valid
