import datetime as dt
from collections import defaultdict
import re

import numpy as np
import rasterio as rio
from rasterio.transform import Affine
import gdal


ascii_date_format = '%Y%m%d%H'
ascii_date_regex = re.compile(r'\d{4}\d{2}\d{2}00')

# These constants taken from the existing GeoTIFFs
PROJ_WKT = 'PROJCS["unnamed",GEOGCS["unnamed ellipse",DATUM["unknown",SPHEROID["unnamed",6371200,0]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",60],PARAMETER["central_meridian",10],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1],AXIS["Easting",SOUTH],AXIS["Northing",SOUTH]]'
DATASET_TRANSFORM = Affine(23812.498583569406, 0.0, -8405812.0, 0.0, -23812.498583569406, 8405812.0)
DATA_DTYPE = np.float64
# 3.4e+38
NODATA = -1.7e+308


def read_daily_ascii_file(input_filepath):
    """Read the given daily ascii file and return a generator over (date, data).

    `date` is a datetime date object.
    `data` is a numpy array.

    """
    str_datas = defaultdict(list)
    with open(input_filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if ascii_date_regex.match(line):
                date = dt.datetime.strptime(line, ascii_date_format).date()
                continue

            str_datas[date].append(line.split())

    data = {}
    for date, str_data in str_datas.items():
        data[date] = np.array(str_data, dtype=DATA_DTYPE)

    return data


def make_geotiff(input_ascii_fp, output_geotiff_fp):
    data = read_daily_ascii_file(input_ascii_fp)
    nbands = len(data.keys())

    crs = rio.crs.CRS().from_wkt(PROJ_WKT)
    with rio.open(output_geotiff_fp, 'w',
            driver='GTiff',
            count=nbands,
            height=706,
            width=706,
            dtype=DATA_DTYPE,
            crs=crs,
            transform=DATASET_TRANSFORM,
            nodata=NODATA) as out_ds:
        for idx, (date, np_array) in enumerate(data.items(), start=1):
            print(f'Writing {date} to band {idx}')
            out_ds.write(np_array, idx)

    # Generate statistics
    gdal.Info(output_geotiff_fp, stats=True)


if __name__ == '__main__':
    input_fp = '/home/trst2284/code/nsidc0447-geotiffs/localdata/NSIDC-0447-2020/cmc_daily_analysis_2020.txt'
    make_geotiff(input_fp, '/tmp/test.tif')
