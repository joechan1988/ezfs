import subprocess
import datetime


def execute(cmd, debug=True):
    if not debug:
        try:
            return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            return "Command Failed: " + ex.message
    else:
        try:
            return subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as ex:
            return "Command Failed: " + ex.message


def get_snapshot_list(dataset, remote_host=None):
    cmd = "/usr/local/bin/zfs list -t snap -H  -r {} |awk '{{print $1}}'".format(dataset)
    if remote_host is not None:
        cmd = "ssh {} sudo ".format(remote_host) + cmd

    output = execute(cmd)
    snapshot_list = output.split("\n")

    if not snapshot_list[-1]:
        snapshot_list = sorted(snapshot_list[:-1])

    return snapshot_list


def delete_snapshot(name, remote_host=None):
    cmd = "/usr/local/bin/zfs destroy {}".format(name)

    if remote_host is not None:
        cmd = "ssh {} sudo ".format(remote_host) + cmd
    execute(cmd)


def send_full_snapshot(src, dest, remote_host=None):
    if remote_host is not None:
        cmd = "/usr/local/bin/zfs send {} | ssh {} sudo /usr/local/bin/zfs receive -F {}".format(src, remote_host, dest)
    else:
        cmd = "/usr/local/bin/zfs send {} | /usr/local/bin/zfs receive -F {}".format(src, dest)

    execute(cmd)


def send_incr_snapshot(start, end, dest_dataset, remote_host=None):
    if remote_host is not None:
        cmd = "/usr/local/bin/zfs send -I {start} {end} | ssh {host} sudo /usr/local/bin/zfs receive -d -F {dest}".format(
            start=start, end=end, host=remote_host, dest=dest_dataset)
    else:
        cmd = "/usr/local/bin/zfs send -I {start} {end} | /usr/local/bin/zfs receive -d -F {dest}".format(start=start,
                                                                                                          end=end,
                                                                                                          dest=dest_dataset)

    execute(cmd)


def create_snapshot(dataset, snap_tag):
    snap_name = dataset+"@"+snap_tag
    print("Creating snapshot {} ...".format(snap_name))
    cmd = "/usr/local/bin/zfs snapshot {}".format(snap_name)
    execute(cmd)


def get_snapshot_tag(snap):
    snap_tag = snap.split("@")[-1]
    return snap_tag


def append_snapshot_tag(dataset, tag):
    snapshot = dataset + "@" + tag
    return snapshot


def _get_snapshot_policy():
    pass


def _schedule():
    pass


class Datetime():
    def __init__(self, timedata):
        self.timedata = timedata
        self.month = None
        self.year = None
        self.day = None
        self.weekday = None
        self.time = None

    def __str__(self):
        pass

    def long_format(self):
        pass

    def _get_month(self):
        pass

    def _get_year(self):
        pass


def string_to_date(date_string):
    # date_str = "201810091514"

    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    hour = int(date_string[8:10])
    minute = int(date_string[10:12])
    date = datetime.datetime(year, month, day, hour, minute)

    return date


def date_to_string(date):
    date_string = date.strftime('%Y%m%d%H%M')
    return date_string
