===============
 Watering Time
===============

This package converts a representation of the watering schedule for my
sprinkler control system to a calendar view that is easier to
understand and validate.

Sprinkler System Model
======================

The operating model for the program is based on a sprinkler system
that can be programmed to send water to different sets of sprinkler
heads grouped into *zones*. Each zone can be activated for a number of
minutes, and a set of zone activations can be grouped into a *program*
which is given a start time and specified days of the week when it
runs. The model assumes that only run one zone at a time, so if the
schedule introduces overlaps or conflicts the activations are
serialized to run one after the other.

Input File
==========

The data input file is a YAML file listing the watering zones and the
watering programs.

Each zone is identified by a number, mapped to a short but descriptive
name.

::

  zones:
    1: turf
    2: f shrubs
    3: b shrubs
    4: patio
    5: garden

The watering programs are identified by letters or short strings, and
include a list of start times, a set of days of the week on which the
program runs, and run times for each zone in the order that the zone
is activated.

::

  programs:
    A:
      start:
        - '3:30'
      days: TuThSaSu
      zones:
        - zone: 1
          time: 30
        - zone: 3
          time: 30
        - zone: 4
          time: 10

Days are described using a string containing ``M``, ``Tu``, ``W``,
``Th``, ``F``, ``Sa``, and ``Su`` *or* ``odd`` *or* ``even``.

::

  programs:
    C:
      start:
        - '6:00'
      days: even
      zones:
        - zone: 5
          time: 15

Usage
=====

The ``wateringtime`` command line program produces output in two
formats. The simple formatter summarizes the YAML data in a table.

::

  $ wateringtime  --format simple wateringtime.yaml
  +---------+----------+-------------+----------------+----------+
  | Program |   Days   | Start Times | Zones          | Duration |
  +---------+----------+-------------+----------------+----------+
  |    A    | TuThSaSu |   03:30:00  | turf      (30) |    70    |
  |         |          |   04:00:00  | b shrubs  (30) |          |
  |         |          |   04:30:00  | patio     (10) |          |
  |    B    | TuThSaSu |   05:00:00  | f shrubs  (50) |    50    |
  |    C    |  MWFSu   |   06:00:00  | garden    (15) |    15    |
  +---------+----------+-------------+----------------+----------+

The caledar formatter shows the watering schedule for each program and
zone on each day of a specified month.

::

  $ wateringtime -v --format calendar --year 2016 --month 9 wateringtime.yaml
  
                                                                                  September                                                                                 
  
  +----------------------+------------------------+----------------------+------------------------+----------------------+------------------------+------------------------+
  | Mon                  | Tue                    | Wed                  | Thu                    | Fri                  | Sat                    | Sun                    |
  +----------------------+------------------------+----------------------+------------------------+----------------------+------------------------+------------------------+
  |                      |                        |                      | (1)                    | (2)                  | (3)                    | (4)                    |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      |                        |                      | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | A (TuThSaSu) [70]      |
  |                      |                        |                      | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 03:30-04:00 - turf     |
  |                      |                        |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs | 04:00-04:30 - b shrubs |
  |                      |                        |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    | 04:30-04:40 - patio    |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      |                        |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      | B (TuThSaSu) [50]      |
  |                      |                        |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs | 05:00-05:50 - f shrubs |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      |                        |                      |                        |                      |                        | C (MWFSu) [15]         |
  |                      |                        |                      |                        |                      |                        | 06:00-06:15 - garden   |
  +----------------------+------------------------+----------------------+------------------------+----------------------+------------------------+------------------------+
  | (5)                  | (6)                    | (7)                  | (8)                    | (9)                  | (10)                   | (11)                   |
  |                      |                        |                      |                        |                      |                        |                        |
  | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | A (TuThSaSu) [70]      |
  | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 03:30-04:00 - turf     |
  |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs | 04:00-04:30 - b shrubs |
  |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    | 04:30-04:40 - patio    |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      | B (TuThSaSu) [50]      |
  |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs | 05:00-05:50 - f shrubs |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      |                        |                      |                        |                      |                        | C (MWFSu) [15]         |
  |                      |                        |                      |                        |                      |                        | 06:00-06:15 - garden   |
  +----------------------+------------------------+----------------------+------------------------+----------------------+------------------------+------------------------+
  | (12)                 | (13)                   | (14)                 | (15)                   | (16)                 | (17)                   | (18)                   |
  |                      |                        |                      |                        |                      |                        |                        |
  | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | A (TuThSaSu) [70]      |
  | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 03:30-04:00 - turf     |
  |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs | 04:00-04:30 - b shrubs |
  |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    | 04:30-04:40 - patio    |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      | B (TuThSaSu) [50]      |
  |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs | 05:00-05:50 - f shrubs |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      |                        |                      |                        |                      |                        | C (MWFSu) [15]         |
  |                      |                        |                      |                        |                      |                        | 06:00-06:15 - garden   |
  +----------------------+------------------------+----------------------+------------------------+----------------------+------------------------+------------------------+
  | (19)                 | (20)                   | (21)                 | (22)                   | (23)                 | (24)                   | (25)                   |
  |                      |                        |                      |                        |                      |                        |                        |
  | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | A (TuThSaSu) [70]      |
  | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 03:30-04:00 - turf     |
  |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs | 04:00-04:30 - b shrubs |
  |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    | 04:30-04:40 - patio    |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      | B (TuThSaSu) [50]      |
  |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs | 05:00-05:50 - f shrubs |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      |                        |                      |                        |                      |                        | C (MWFSu) [15]         |
  |                      |                        |                      |                        |                      |                        | 06:00-06:15 - garden   |
  +----------------------+------------------------+----------------------+------------------------+----------------------+------------------------+------------------------+
  | (26)                 | (27)                   | (28)                 | (29)                   | (30)                 |                        |                        |
  |                      |                        |                      |                        |                      |                        |                        |
  | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       | A (TuThSaSu) [70]      | C (MWFSu) [15]       |                        |                        |
  | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden | 03:30-04:00 - turf     | 06:00-06:15 - garden |                        |                        |
  |                      | 04:00-04:30 - b shrubs |                      | 04:00-04:30 - b shrubs |                      |                        |                        |
  |                      | 04:30-04:40 - patio    |                      | 04:30-04:40 - patio    |                      |                        |                        |
  |                      |                        |                      |                        |                      |                        |                        |
  |                      | B (TuThSaSu) [50]      |                      | B (TuThSaSu) [50]      |                      |                        |                        |
  |                      | 05:00-05:50 - f shrubs |                      | 05:00-05:50 - f shrubs |                      |                        |                        |
  +----------------------+------------------------+----------------------+------------------------+----------------------+------------------------+------------------------+

