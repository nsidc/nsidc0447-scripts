import datetime as dt
from collections import defaultdict
import re

import numpy as np


ascii_date_format = '%Y%m%d%H'
ascii_date_regex = re.compile(r'\d{4}\d{2}\d{2}00')


def read_daily_ascii_file(input_filepath):
    """Read the given daily ascii file and return a generator over (date, data).

    `date` is a datetime date object.
    `data` is a numpy array.

    """
    data = defaultdict(list)
    with open(input_filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if ascii_date_regex.match(line):
                date = dt.datetime.strptime(line, ascii_date_format).date()
                continue

            data[date].append(line.split())


    for date, str_data in data.items():
        # TODO: determine correct dtype
        yield date, np.array(str_data, dtype=np.float64)


if __name__ == '__main__':
    input_fp = '/home/trst2284/code/nsidc0447-geotiffs/localdata/NSIDC-0447-2020/cmc_daily_analysis_2020.txt'
    for date, data in read_daily_ascii_file(input_fp):
        breakpoint()
        pass
