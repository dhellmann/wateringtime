from __future__ import print_function

import operator

import prettytable

from .program import Program


def show_programs(zones, programs):
    t = prettytable.PrettyTable(
        field_names=('Program', 'Days', 'Start Times', 'Zones', 'Duration'),
        print_empty=False,
    )
    t.padding_width = 1
    t.align['Zones'] = 'l'

    for p in programs:
        zone_names = '\n'.join(
            '{zone:<10}({time})'.format(
                zone=zones[z['zone']],
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
            zone_names,
            p.duration,
        ))
    print(t.get_string())


def show(args, zones, programs):
    show_programs(zones, programs)
