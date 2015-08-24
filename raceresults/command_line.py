"""
Command line interface to RR.
"""

import argparse
import datetime
import tempfile

from lxml import etree, html

from .active import ActiveRR
from .brrr import BestRace
from .crrr import CoolRunning
from .csrr import CompuScore
from .nyrr import NewYorkRR
from .common import RaceResults


def run_active():
    the_description = 'Process Active race results'
    parser = argparse.ArgumentParser(description=the_description)
    parser.add_argument('-d', '--day', dest='day', nargs=2, help='day range')
    parser.add_argument('-m', '--month', dest='month',
                        default=datetime.date.today().month,
                        choices=range(1, 13),
                        type=int,
                        help='month')
    parser.add_argument('-o', '--output', dest='output_file',
                        default='results.html',
                        help='output file, default is results.html')
    parser.add_argument('-s', '--states',
                        dest='states',
                        nargs='+',
                        default=['NJ'],
                        help='state, default is NJ')
    parser.add_argument('-y', '--year', dest='year',
                        default=datetime.date.today().year, help='year')
    parser.add_argument('--ml', dest='membership_list',
                        help='membership list', required=True)
    parser.add_argument('--verbose',
                        dest='verbose',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'],
                        default='info',
                        help='verbosity level, default is "info"')
    args = parser.parse_args()

    year = int(args.year)
    month = int(args.month)
    day = args.day

    states = [state.upper() for state in args.states]

    if args.day is not None:
        start_date = datetime.date(year, month, int(day[0]))
        stop_date = datetime.date(year, month, int(day[1]))
    else:
        # Make the range the entire month up until now.
        start_date = datetime.date(year, month, 1)
        stop_date = datetime.date(year, month, datetime.datetime.now().day)

    o = ActiveRR(date_range=[start_date, stop_date],
                 membership_list=args.membership_list,
                 verbose=args.verbose,
                 states=states,
                 output_file=args.output_file)
    o.run()


def run_bestrace():
    # -ml cannot be used with -d, -m, or -y
    # But -y and -m have defaults.
    the_description = 'Process BestRace race results'
    parser = argparse.ArgumentParser(description=the_description)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--day', dest='day',
                       nargs=2, help='day range')
    parser.add_argument('--verbose',
                        dest='verbose',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'],
                        default='info',
                        help='verbosity level, default is "info"')
    parser.add_argument('-m', '--month', dest='month',
                        default=datetime.date.today().month,
                        choices=range(1, 13),
                        type=int,
                        help='month')
    parser.add_argument('-o', '--output', dest='output_file',
                        default='results.html',
                        help='output file, default is results.html')
    parser.add_argument('-y', '--year', dest='year',
                        default=datetime.date.today().year, help='year')
    parser.add_argument('--ml', dest='membership_list',
                        help='membership list', required=True)
    args = parser.parse_args()

    year = int(args.year)
    month = int(args.month)
    day = args.day

    if args.day is not None:
        start_date = datetime.date(year, month, int(day[0]))
        stop_date = datetime.date(year, month, int(day[1]))
    else:
        # Make the range the entire month up until now.
        start_date = datetime.date(year, month, 1)
        stop_date = datetime.date(year, month, datetime.datetime.now().day)

    o = BestRace(start_date=start_date,
                 stop_date=stop_date,
                 membership_list=args.membership_list,
                 output_file=args.output_file,
                 verbose=args.verbose)
    o.run()


def run_coolrunning():
    # -ml cannot be used with -d, -m, or -y
    # But -y and -m have defaults.
    the_description = 'Process Coolrunning race results'
    parser = argparse.ArgumentParser(description=the_description)
    parser.add_argument('-y', '--year',
                        dest='year',
                        default=datetime.date.today().year,
                        help='year')
    parser.add_argument('-m', '--month',
                        dest='month',
                        default=datetime.date.today().month,
                        choices=range(1, 13),
                        type=int,
                        help='month')
    parser.add_argument('-d', '--day',
                        dest='day',
                        nargs=2,
                        help='day range')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'],
                        default='info',
                        help='verbosity level, default is "info"')
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        default='results.html',
                        help='output file, default is results.html')
    parser.add_argument('-s', '--states',
                        dest='states',
                        nargs='+',
                        default=['ma'],
                        help='state, default is ma')
    parser.add_argument('--ml',
                        dest='membership_list',
                        help='membership list',
                        required=True)
    args = parser.parse_args()

    year = int(args.year)
    month = int(args.month)
    day = args.day

    if args.day is not None:
        start_date = datetime.date(year, month, int(day[0]))
        stop_date = datetime.date(year, month, int(day[1]))
    else:
        start_date = None
        stop_date = None

    o = CoolRunning(start_date=start_date,
                    stop_date=stop_date,
                    membership_list=args.membership_list,
                    output_file=args.output_file,
                    states=args.states,
                    verbose=args.verbose)
    o.run()


def run_compuscore():
    # --ml cannot be used with -m, or -y
    the_description = 'Process Compuscore race results'
    parser = argparse.ArgumentParser(description=the_description)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-y', '--year',
                        dest='year',
                        default=datetime.date.today().year,
                        help='year')
    parser.add_argument('-m', '--month',
                        dest='month',
                        default=datetime.date.today().month,
                        choices=range(1, 13),
                        type=int,
                        help='month')
    group.add_argument('-d', '--day',
                       dest='day',
                       default=[datetime.date.today().day,
                                datetime.date.today().day],
                       nargs=2,
                       help='day range')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'],
                        default='info',
                        help='verbosity level, default is "info"')
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        default='results.html',
                        help='output file, default is results.html')
    parser.add_argument('--ml', dest='membership_list',
                        help='membership list', required=True)

    args = parser.parse_args()

    year = int(args.year)
    month = int(args.month)
    day = args.day

    start_date = datetime.date(year, month, int(day[0]))
    stop_date = datetime.date(year, month, int(day[1]))

    o = CompuScore(start_date=start_date,
                   stop_date=stop_date,
                   membership_list=args.membership_list,
                   output_file=args.output_file,
                   verbose=args.verbose)
    o.run()


def run_new_jersey():
    # --ml cannot be used with -m, or -y
    the_description = 'Process New Jersey race results'
    parser = argparse.ArgumentParser(description=the_description)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-y', '--year',
                        dest='year',
                        default=datetime.date.today().year,
                        help='year')
    parser.add_argument('-m', '--month',
                        dest='month',
                        default=datetime.date.today().month,
                        choices=range(1, 13),
                        type=int,
                        help='month')
    group.add_argument('-d', '--day',
                       dest='day',
                       default=[datetime.date.today().day,
                                datetime.date.today().day],
                       nargs=2,
                       help='day range')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'],
                        default='info',
                        help='verbosity level, default is "info"')
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        default='results.html',
                        help='output file, default is results.html')
    parser.add_argument('--ml', dest='membership_list',
                        help='membership list', required=True)

    args = parser.parse_args()

    rrobj = RaceResults(output_file=args.output_file)

    year = int(args.year)
    month = int(args.month)
    day = args.day

    start_date = datetime.date(year, month, int(day[0]))
    stop_date = datetime.date(year, month, int(day[1]))

    with tempfile.NamedTemporaryFile() as afile:
        with tempfile.NamedTemporaryFile() as bfile:
            with tempfile.NamedTemporaryFile() as cfile:
                with tempfile.NamedTemporaryFile() as dfile:

                    CompuScore(start_date=start_date,
                               stop_date=stop_date,
                               membership_list=args.membership_list,
                               output_file=afile.name,
                               verbose=args.verbose).run()
                    BestRace(start_date=start_date,
                             stop_date=stop_date,
                             membership_list=args.membership_list,
                             output_file=bfile.name,
                             verbose=args.verbose).run()
                    ActiveRR(date_range=[start_date, stop_date],
                             membership_list=args.membership_list,
                             verbose=args.verbose,
                             states=['NY', 'NJ', 'PA'],
                             output_file=cfile.name).run()
                    NewYorkRR(start_date=start_date,
                              stop_date=stop_date,
                              team='RARI',
                              output_file=dfile.name).run()

                    # Rewind all four files.
                    afile.seek(0)
                    bfile.seek(0)
                    cfile.seek(0)
                    dfile.seek(0)

                    rrobj.initialize_output_file()

                    with open(args.output_file, 'rt') as ofile:
                        odoc = html.document_fromstring(ofile.read())
                    for tfile in [afile, bfile, cfile, dfile]:
                        doc = html.document_fromstring(tfile.read())
                        divs = doc.cssselect('div.race')
                        for div in divs:
                            odoc.append(div)

                    result = etree.tostring(odoc, pretty_print=True,
                                            method="html", encoding='unicode')

                    with open(rrobj.output_file, 'w') as fptr:
                        fptr.write(result)


def run_nyrr():
    # --ml cannot be used with -m, or -y
    the_description = 'Process NYRR race results'
    parser = argparse.ArgumentParser(description=the_description)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-y', '--year',
                        dest='year',
                        default=datetime.date.today().year,
                        help='year')
    parser.add_argument('-m', '--month',
                        dest='month',
                        default=datetime.date.today().month,
                        choices=range(1, 13),
                        type=int,
                        help='month')
    group.add_argument('-d', '--day',
                       dest='day',
                       default=[datetime.date.today().day,
                                datetime.date.today().day],
                       nargs=2,
                       help='day range')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'],
                        default='info',
                        help='verbosity level, default is "info"')
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        default='results.html',
                        help='output file, default is results.html')
    parser.add_argument('--team',
                        dest='team',
                        default='RARI',
                        help='team code (i.e. "RARI")')

    args = parser.parse_args()

    year = int(args.year)
    month = int(args.month)
    day = args.day

    start_date = datetime.date(year, month, int(day[0]))
    stop_date = datetime.date(year, month, int(day[1]))

    o = NewYorkRR(start_date=start_date,
                  stop_date=stop_date,
                  team=args.team,
                  output_file=args.output_file,
                  verbose=args.verbose)
    o.run()
