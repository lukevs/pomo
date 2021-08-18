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
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import typer


POMO_DIR = Path.home() / ".pomo"

WEEKLY_TEMPLATE = """Goals:

"""

TEMPLATE = """{}

Goals:


{} - {}

{}
"""


app = typer.Typer()


def make_doc(filepath: Path, today: datetime, start: float, end: float):
    real_end = end

    if end < start:
        real_end += 12

    num_dashes = int((real_end - start) / 0.5)
    dashes = '\n'.join('-' * num_dashes)
    body = f"Planning\n{dashes}"

    start_time = str(start).replace('.0', ':00').replace('.5', ':30')
    end_time = str(end).replace('.0', ':00').replace('.5', ':30')

    with filepath.open("w") as f:
        f.write(TEMPLATE.format(today, start_time, end_time, body))


def make_week_doc(filepath: Path) -> None:
    with filepath.open("w") as f:
        f.write(WEEKLY_TEMPLATE)


def vim_open(filepath: Path) -> None:
    os.system('vim ' + str(filepath))


@app.command()
def main(
    start: Optional[float] = typer.Option(None, "--start"),
    end: Optional[float] = typer.Option(None, "--end"),
    week: bool = typer.Option(False, "--week", "-w"),
    list: bool = typer.Option(False, "--list", "-l"),
):
    if not POMO_DIR.is_dir():
        POMO_DIR.mkdir()

    today = datetime.now().date()

    if list:
        monday_of_the_week = today - timedelta(days=today.weekday())
        vim_open(POMO_DIR / 'list.txt')

    elif week:
        monday_of_the_week = today - timedelta(days=today.weekday())
        filepath = POMO_DIR / 'week-{}.txt'.format(str(monday_of_the_week))

        if not filepath.is_file():
            make_week_doc(filepath)

        vim_open(filepath)

    else:
        filepath = POMO_DIR / '{}.txt'.format(today)

        if not filepath.is_file():
            if start is None or end is None:
                typer.echo("start and end are required for new days")
                sys.exit(1)

            make_doc(filepath, today, start, end)

        vim_open(filepath)
