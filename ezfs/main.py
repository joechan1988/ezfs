#!/usr/bin/python

import click
import datetime
import utils
import os
import sys

@click.group()
def cli():
    """
    Enhanced ZFS CLI Tool version 1.0
    """
    if not os.path.exists("/usr/local/bin/zfs"):
        print("No symbol link of zfs binary found in /usr/local/bin/, please create first...")
        sys.exit(0)

    if not os.path.exists("/usr/local/bin/zpool"):
        print("No symbol link of zpool binary found in /usr/local/bin/, please create first...")
        sys.exit(0)

@cli.group()
def snap():
    """
    Snapshot zfs datasets/volumes
    """


@cli.command()
@click.option("--pool","-p",required=False)
def list(pool):
    utils.list_all(pool)


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
    yst_day = (cur_date - datetime.timedelta(days=1)).day
    cur_hour = cur_date.hour
    cur_year = cur_date.year

    utils.create_snapshot(dataset, cur_date_string)

    snap_list = utils.get_snapshot_list(dataset)

    for snap in snap_list:
        snap_tag = snap.split("@")[-1]
        snap_date = utils.string_to_date(snap_tag)

        if snap_date.year != cur_year or \
                (snap_date.month != cur_month and snap_date.day != 1) or \
                (snap_date.isocalendar()[1] != cur_week and snap_date.isoweekday() != 1 and snap_date.day != 1) or \
                (snap_date.day != cur_day and snap_date.day != yst_day and snap_date.hour != 0) or \
                (snap_date.day == yst_day and snap_date.hour < cur_hour and snap_date.hour != 0):
            print("Deleting snapshot {}".format(snap))
            utils.delete_snapshot(snap)


@snap.command()
@click.argument('dataset')
@click.option('--host', '-h', required=False)
@click.option('--dest-dataset', '-d', required=True)
def sync(dataset, host, dest_dataset):
    """
    sample: \n
    ezfs snap sync pool/dataset -d dest_pool/dest_dataset [-h user@hostname]

    """
    dest_dataset_snap_list = utils.get_snapshot_list(dest_dataset, remote_host=host)
    src_dataset_snap_list = utils.get_snapshot_list(dataset)

    snap_deleted = []

    for snap in dest_dataset_snap_list:
        snap_tag = utils.get_snapshot_tag(snap)
        src_snap = utils.append_snapshot_tag(dataset, snap_tag)

        if src_snap not in src_dataset_snap_list:
            snap_deleted.append(snap)

    for snap in snap_deleted:
        print("Deleting destination snapshot {}".format(snap))
        utils.delete_snapshot(snap, remote_host=host)

    # Find first snap in common
    last_common_snap = ""
    for snap in reversed(src_dataset_snap_list):
        snap_tag = snap.split("@")[-1]
        dest_snap = dest_dataset + "@" + snap_tag
        if dest_snap in dest_dataset_snap_list:
            last_common_snap = snap
            break

    print last_common_snap

    if not last_common_snap:
        src_snap = src_dataset_snap_list[-1]
        snap_tag = src_snap.split("@")[-1]
        dest_snap = dest_dataset + "@" + snap_tag
        utils.send_full_snapshot(src_snap, dest_snap, remote_host=host)
    elif last_common_snap == src_dataset_snap_list[-1]:
        print("Destination dataset already in sync...")
        return
    else:
        incr_start = last_common_snap
        incr_end = src_dataset_snap_list[-1]
        print("Sending new snapshot {} to backup dataset...".format(incr_end))
        utils.send_incr_snapshot(incr_start, incr_end, dest_dataset, remote_host=host)

    # Start Sync Increment Snapshots


if __name__ == '__main__':
    cli()
