"""
Create a new day doc from 8:30 AM to 5 PM:
pomo 8.5 5

Open your existing day's doc
pomo

View your pomo from 3 days ago
pomo -m 3

View your week goals, or create a new one for this week
pomo -w

View your global list of tasks
pomo -l
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

POMO_DIR = Path.home() / ".pomo"

WEEKLY_TEMPLATE = """Goals:

"""

TEMPLATE = """{}

Goals:


{} - {}

{}
"""

def make_doc(filename, today, start, end):
    real_end = end

    if end < start:
        real_end += 12

    num_dashes = int((real_end - start) / 0.5)
    dashes = '\n'.join('-' * num_dashes)
    body = f"Planning\n{dashes}"

    start_time = str(start).replace('.0', ':00').replace('.5', ':30')
    end_time = str(end).replace('.0', ':00').replace('.5', ':30')

    with open(filename, 'w') as f:
        f.write(TEMPLATE.format(today, start_time, end_time, body))


def make_week_doc(filename):
    with open(filename, 'w') as f:
        f.write(WEEKLY_TEMPLATE)


def main():
    if not os.path.isdir(POMO_DIR):
        os.mkdir(POMO_DIR)

    if len(sys.argv) == 2 and sys.argv[1] == '-l':
        today = datetime.now().date()
        monday_of_the_week = today - timedelta(days=today.weekday())
        filename = POMO_DIR / 'list.txt'
        os.system('vim ' + str(filename))

    elif len(sys.argv) == 2 and sys.argv[1] == '-w':
        today = datetime.now().date()
        monday_of_the_week = today - timedelta(days=today.weekday())
        filename = POMO_DIR / 'week-{}.txt'.format(str(monday_of_the_week))

        if not os.path.isfile(filename):
            make_week_doc(filename)

        os.system('vim ' + str(filename))

    elif len(sys.argv) == 3 and sys.argv[1] == '-m':
        day = str(datetime.now().date() - timedelta(days=int(sys.argv[2])))
        filename = POMO_DIR / '{}.txt'.format(day)

        if not os.path.isfile(filename):
            print('No pomo found for {}'.format(day))
        else:
            os.system('vim ' + str(filename))

    else:
        today = str(datetime.now().date())
        filename = POMO_DIR / '{}.txt'.format(today)

        if not os.path.isfile(filename):
            if len(sys.argv) < 3:
                print("start and end are required for new days")
                sys.exit(1)

            start = float(sys.argv[1])
            end = float(sys.argv[2])

            make_doc(filename, today, start, end)

        os.system('vim ' + str(filename))


if __name__ == "__main__":
    main()
