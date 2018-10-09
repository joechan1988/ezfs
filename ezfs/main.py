#!/usr/bin/python

import click
import datetime
import utils


@click.group()
def cli():
    """

    :return:
    """


@cli.group()
def snap():
    """

    :return:
    """


@snap.command()
@click.argument('dataset')
@click.argument('new', required=False)
def rotate(dataset, new):
    cur_date = datetime.datetime.now()
    cur_date_string = utils.date_to_string(cur_date)
    cur_month = cur_date.month
    cur_weekday = cur_date.isoweekday()
    cur_week = cur_date.isocalendar()[1]
    cur_day = cur_date.day
    cur_year = cur_date.year

    snap_cmd = "zfs snapshot {}@{}".format(dataset, cur_date_string)
    utils.execute(snap_cmd)

    snap_list = utils.get_snapshot_list(dataset)

    for snap in snap_list:
        snap_tag = snap.split("@")[-1]
        snap_date = utils.string_to_date(snap_tag)

        destroy_cmd = "zfs destroy {}".format(snap)

        if snap_date.year != cur_year or \
                (snap_date.month != cur_month and snap_date.day != 1) or \
                (snap_date.isocalendar()[1] != cur_week and snap_date.isoweekday() != 1 and snap_date.day != 1):
            print (snap, snap_date.day)
            print("Deleting snapshot {}".format(snap))
            utils.execute(destroy_cmd)


if __name__ == '__main__':
    cli()
