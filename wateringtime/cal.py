from __future__ import print_function

import calendar
import datetime
import functools
import operator

import prettytable


def show(args, zones, programs):
    t = prettytable.PrettyTable(
        field_names=calendar.day_abbr,
        print_empty=False,
        hrules=prettytable.ALL,
    )
    t.align = 'l'

    cal = calendar.Calendar(calendar.MONDAY)
    month_data = cal.monthdays2calendar(args.year, args.month)

    for week in month_data:
        row = []
        for dom, dow in week:
            if not dom:
                # Zero days are from another month; leave the cell blank.
                row.append('')
                continue

            # Show the day and all watering events on that day.
            lines = ['(%s)' % dom]
            for p in (p for p in programs
                      if p.occurs_on_day(dow, dom)):
                if args.verbose:
                    lines.append('')
                    lines.append('{p.name} ({p.days}) [{p.duration}]'.format(p=p))
                for s, e, z in p.run_times:
                    name = zones[z]
                    lines.append(
                        '{s}-{e} - {name}'.format(
                            s=s.strftime('%H:%M'),
                            e=e.strftime('%H:%M'),
                            name=name,
                        )
                    )
            row.append('\n'.join(lines))
        t.add_row(row)

    formatted = t.get_string()
    # Center the name of the month over the output calendar.
    print('\n{:^{width}}\n'.format(
        calendar.month_name[args.month],
        width=len(formatted.splitlines()[0]),
    ))
    print(formatted)
