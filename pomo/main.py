import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import typer


POMO_DIRECTORY = Path.home() / ".pomo"

WEEKLY_TEMPLATE = """Goals:

"""

TEMPLATE = """{}

Goals:


{} - {}

{}
"""


app = typer.Typer()


def build_doc(today: datetime, start: float, end: float) -> str:
    real_end = end

    if end < start:
        real_end += 12

    num_dashes = int((real_end - start) / 0.5)
    dashes = '\n'.join('-' * num_dashes)
    body = f"Planning\n{dashes}"

    start_time = str(start).replace('.0', ':00').replace('.5', ':30')
    end_time = str(end).replace('.0', ':00').replace('.5', ':30')

    return TEMPLATE.format(today, start_time, end_time, body)


def handle_list() -> None:
    vim_open(POMO_DIRECTORY / 'list.txt')


def handle_week() -> None:
    today = datetime.now().date()
    monday_of_the_week = today - timedelta(days=today.weekday())
    filepath = POMO_DIRECTORY / 'week-{}.txt'.format(str(monday_of_the_week))

    if not filepath.is_file():
        make_week_doc(filepath)

    with filepath.open("w") as f:
        f.write(WEEKLY_TEMPLATE)

    vim_open(filepath)


def handle_minus(minus_days: int) -> None:
    day = datetime.now().date() - timedelta(days=minus_days)
    filepath = get_day_path(day)

    if not filepath.is_file():
        typer.echo(f"No pomo found for {day}")
        raise typer.Abort()

    vim_open(filepath)


def handle_day(start: Optional[float], end: Optional[float]) -> None:
    today = datetime.now().date()
    filepath = get_day_path(today)

    if not filepath.is_file():
        if start is None or end is None:
            typer.echo("start and end are required for new days")
            raise typer.Abort()

        doc_content = build_doc(today, start, end)

        with filepath.open("w") as f:
            f.write(doc_content)

    vim_open(filepath)


def get_day_path(day: datetime) -> Path:
    return POMO_DIRECTORY / '{}.txt'.format(day)


def vim_open(filepath: Path) -> None:
    os.system('vim ' + str(filepath))


@app.command()
def main(
    start: Optional[float] = typer.Argument(None),
    end: Optional[float] = typer.Argument(None),
    list: bool = typer.Option(False, "--list", "-l"),
    week: bool = typer.Option(False, "--week", "-w"),
    minus_days: int = typer.Option(0, "--minus", "-m"),
):
    if not POMO_DIRECTORY.is_dir():
        POMO_DIRECTORY.mkdir()

    if list:
        handle_list()
    elif week:
        handle_week()
    elif minus_days != 0:
        handle_minus(minus_days)
    else:
        handle_day(start, end)
