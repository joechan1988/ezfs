#!/usr/bin/python
import utils
import main


def test_date():
    import datetime

    now = datetime.datetime.now()
    now_week = now.isocalendar()[1]
    print now_week


def test_snap_list():
    snap_list = utils.get_snapshot_list("testpool/dataset1")
    print snap_list


def test_snap_rotate():
    main.rotate("testpool/dataset1")


if __name__ == '__main__':
    test_snap_rotate()
