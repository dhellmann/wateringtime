import operator

import prettytable


def show_programs(data):
    t = prettytable.PrettyTable(
        field_names=('Program', 'Start Times', 'Days', 'Zones'),
        print_empty=False,
    )
    t.padding_width = 1
    t.align['Zones'] = 'l'

    for p, pdata in sorted(data['programs'].items()):
        zones = '\n'.join(
            '{zone:<10}({time})'.format(
                zone=data['zones'][z['zone']],
                time=z['time'],
            )
            for z in sorted(pdata['zones'],
                            key=operator.itemgetter('zone'))
        )
        t.add_row((p, '\n'.join(pdata['start']), pdata['days'],
                   zones))
    print t.get_string()


def show(args, data):
    show_programs(data)
