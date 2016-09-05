import argparse
import datetime
import sys

import yaml

from wateringtime import cal
from wateringtime import program
from wateringtime import simple


def main():
    today = datetime.date.today()
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '--format', '-f',
        choices=('simple', 'calendar'),
        default='simple',
        help='output format (%(default)s)',
    )
    ap.add_argument(
        '-c',
        dest='format',
        action='store_const',
        const='calendar',
        help='output calendar format',
    )
    ap.add_argument(
        '--year',
        type=int,
        default=today.year,
        help='year to show schedule',
    )
    ap.add_argument(
        '--month',
        type=int,
        default=today.month,
        help='month of the year to show schedule',
    )
    ap.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='enable verbose output',
    )
    ap.add_argument(
        'filename',
        default='wateringtime.yaml',
        nargs='?',
        help='input file (%(default)s)',
    )
    args = ap.parse_args()

    data = yaml.load(open(args.filename, 'r'))

    formatters = {
        'simple': simple.show,
        'calendar': cal.show,
    }

    zones = data['zones']
    programs = [
        program.Program(*p)
        for p in data['programs'].items()
    ]
    programs.sort(key=lambda p: p.start_times[0])

    formatters[args.format](args, zones, programs)
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
