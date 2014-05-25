import calendar

import prettytable


def show(args, data):
    t = prettytable.PrettyTable(
        field_names=calendar.day_abbr,
        print_empty=False,
    )
    cal = calendar.Calendar(calendar.MONDAY)
    month_data = cal.monthdayscalendar(args.year, args.month)
    for week in month_data:
        row = []
        for n, day in enumerate(week, 1):
            if not day:
                row.append('')
                continue
            row.append(str(day))
        t.add_row(row)

    formatted = t.get_string()
    width = len(formatted.splitlines()[0])
    format_str = '\n{:^%d}\n' % width
    print format_str.format(calendar.month_name[args.month])
    print formatted
    raise NotImplementedError()
    
