import calendar
import datetime
import functools
import operator

import prettytable

from .program import Program


def show(args, data):
    programs = [Program(*p) for p in data['programs'].items()]
    programs.sort(key=lambda p: p.starts[0])

    for p in programs:
        print p.name, p.starts

    t = prettytable.PrettyTable(
        field_names=calendar.day_abbr,
        print_empty=False,
        hrules=prettytable.ALL,
    )
    for d in calendar.day_abbr:
        t.align[d] = 'l'
    cal = calendar.Calendar(calendar.MONDAY)
    month_data = cal.monthdayscalendar(args.year, args.month)
    for week in month_data:
        row = []
        for n, day in enumerate(week):
            if not day:
                row.append('')
                continue
            lines = ['(%s)' % day]
            for p in (p for p in programs
                      if p.occurs_on_day(n, day)):
                if args.verbose:
                    lines.append('')
                    lines.append('%s (%s)' % (p.name, p.days))
                for s, e, z in p.get_run_times():
                    name = data['zones'][z]
                    lines.append(
                        '%s-%s - %s' %
                        (s.strftime('%H:%M'), e.strftime('%H:%M'), name)
                    )
            row.append('\n'.join(lines))
        t.add_row(row)

    formatted = t.get_string()
    width = len(formatted.splitlines()[0])
    format_str = '\n{:^%d}\n' % width
    print format_str.format(calendar.month_name[args.month])
    print formatted
