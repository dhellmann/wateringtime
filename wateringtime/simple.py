import operator

import prettytable

from .program import Program


def show_programs(data):
    programs = [Program(*p) for p in data['programs'].items()]
    programs.sort(key=lambda p: p.start_times[0])

    t = prettytable.PrettyTable(
        field_names=('Program', 'Days', 'Start Times', 'Zones', 'Duration'),
        print_empty=False,
    )
    t.padding_width = 1
    t.align['Zones'] = 'l'

    for p in programs:
        zones = '\n'.join(
            '{zone:<10}({time})'.format(
                zone=data['zones'][z['zone']],
                time=z['time'],
            )
            for z in p.zones
        )
        t.add_row((
            p.name,
            p.days,
            '\n'.join(
                str(s)
                for s, e, z in p.run_times
            ),
            zones,
            p.duration,
        ))
    print t.get_string()


def show(args, data):
    show_programs(data)
