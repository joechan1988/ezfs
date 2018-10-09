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


def get_snapshot_list(dataset):
    cmd = "zfs list -t snap -H  -r {0} |awk '{{print $1}}'".format(dataset)
    output = execute(cmd)
    snapshot_list = output.split("\n")

    if not snapshot_list[-1]:
        snapshot_list = sorted(snapshot_list[:-1])

    return snapshot_list


def _delete_snapshot():
    pass


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
