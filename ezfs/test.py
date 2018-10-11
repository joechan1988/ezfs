#!/usr/bin/python
import utils
import main


def test_date():
    import datetime

    now = datetime.datetime.now()
    d = utils.string_to_date("201810010900")
    yesterday_date = (d - datetime.timedelta(days=1)).day
    print yesterday_date


def test_snap_list():
    snap_list = utils.get_snapshot_list("testpool/dataset1")
    print snap_list


def test_snap_rotate():
    main.rotate("testpool/dataset1")


if __name__ == '__main__':
    test_date()
