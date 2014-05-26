import operator

import prettytable


def show_zones(data):
    t = prettytable.PrettyTable(
        field_names=('Zone', 'Name'),
        print_empty=False,
    )
    t.padding_width = 1
    t.align['Zone'] = 'r'
    t.align['Name'] = 'l'

    for z in sorted(data['zones'].items()):
        t.add_row(z)

    print t.get_string()


def show_programs(data):
    t = prettytable.PrettyTable(
        field_names=('Program', 'Start Times', 'Days', 'Zones'),
        print_empty=False,
    )
    t.padding_width = 1
    t.align['Zones'] = 'l'

    for p, pdata in sorted(data['programs'].items()):
        zones = '\n'.join('%(zone)s(%(time)s)' % z
                          for z in sorted(pdata['zones'],
                                          key=operator.itemgetter('zone')))
        t.add_row((p, '\n'.join(pdata['start']), pdata['days'],
                   zones))
    print t.get_string()


def show(args, data):
    show_zones(data)
    show_programs(data)
