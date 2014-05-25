import argparse

import prettytable
import yaml


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
        t.add_row((p, '\n'.join(pdata['start']), pdata['days'],
                   '\n'.join(pdata['zones'])))
    print t.get_string()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        'filename',
        default='wateringtime.yaml',
        nargs='?',
        help='input file (%(default)s)',
    )
    args = ap.parse_args()

    data = yaml.load(open(args.filename, 'r'))

    show_zones(data)
    show_programs(data)
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
