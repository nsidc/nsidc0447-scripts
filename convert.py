import datetime as dt
from collections import defaultdict
from pathlib import Path
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
NODATA = -1.7e+308
COMPRESSION = rio.enums.Compression.deflate.name


def read_daily_ascii_file(input_filepath):
    """Read the given daily ascii file and return the data.

    Returns a dict where keys are dt.date objects and values are 2D numpy
    arrays representing the data read from the given `input_filepath`.
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
    """Create a GeoTiff version of the given cmc sdepth daily text file.

    Args:
    * input_ascii_fp - full path to input sdepth text file. E.g.,
                       `cmc_sdepth_dly_2001_v01.2.tif`

    * output_geotiff_fp - full path to the output GeoTiff this function will
                          create.
    """
    data = read_daily_ascii_file(input_ascii_fp)
    nbands = len(data.keys())

    crs = rio.crs.CRS().from_wkt(PROJ_WKT)
    with rio.open(
        output_geotiff_fp, 'w',
        driver='GTiff',
        count=nbands,
        height=706,
        width=706,
        dtype=DATA_DTYPE,
        crs=crs,
        transform=DATASET_TRANSFORM,
        nodata=NODATA,
        compress=COMPRESSION
    ) as out_ds:
        for idx, (date, np_array) in enumerate(data.items(), start=1):
            print(f'Writing {date} to band {idx}')
            out_ds.write(np_array, idx)

    # Generate statistics
    print('Generating statistics (this could take a while...)')
    gdal.Info(str(output_geotiff_fp), stats=True)
    print('Done generating statistics.')


def convert_cmc_daily_analysis_txt_to_geotiff(input_ascii_fp, output_geotiff_fp):
    """Convert the cmc daily analysis txt file given by `input_fp` to a geotiff.
    Args:
    * input_ascii_fp - full path to input sdepth text file. E.g.,
                       `cmc_sdepth_dly_2001_v01.2.tif`

    * output_geotiff_fp - full path to the output GeoTiff this function will
                          create.
    """
    Path(output_geotiff_fp).parent.mkdir(parents=True, exist_ok=True)

    # Make the output filename consistent with the existing filenaming
    # structure.
    make_geotiff(input_ascii_fp, output_geotiff_fp)


def crosscheck_existing():
    """Simple regression test to ensure this code produces outputs consistent
    with GeoTiffs already in production.

    This function assumes a local `localdata/` directory containing
    nsidc0447_CMC_snow_depth_v01 data, and an unzipped version of the
    `cmc_sdepth_dly_2001_v01.2.txt` file.

    This was meant as a one-off test, so be careful running it. It probably
    needs to be edited.
    """
    input_fp = 'localdata/test/cmc_sdepth_dly_2001_v01.2.txt'
    output_dir = Path('localdata/test/cmc_sdepth_dly_2001_v01.2.tif')
    output_dir.mkdir(parents=True, exist_ok=True)

    output_fp = output_dir / 'cmc_sdepth_dly_2020_v01.2.tif'
    make_geotiff(input_fp, output_fp)

    new_ds = rio.open(output_fp, 'r')
    old_ds = rio.open('localdata/projects/DATASETS/nsidc0447_CMC_snow_depth_v01/Snow_Depth/Snow_Depth_Daily_Values/GeoTIFF/cmc_sdepth_dly_2001_v01.2.tif', 'r')

    assert new_ds.count == old_ds.count
    for band_idx in range(1, new_ds.count + 1):
        new_data = new_ds.read(band_idx)
        old_data = old_ds.read(band_idx)
        print(f'checking {band_idx}')
        if not np.all(new_data == old_data):
            raise RuntimeError(f'Newly created GeoTiff does not match regression for band {band_idx}')
    print('Done!')
