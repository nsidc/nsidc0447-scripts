![NSIDC logo](/images/nsidc_logo.png)
![NSIDC DAAC Logo](/images/nsidc_daac_logo.png)
![NASA logo](/images/nasa_logo.png)

nsidc0447-scripts
---

Scripts related to [NSIDC-0447](https://nsidc.org/data/nsidc-0447): Canadian Meteorological Center (CMC) Daily Snow Depth Analysis Data, Version 1. This repository is a work in progress! 

The scripts that are currently in this repository can be used to read the daily or monthly snow depth ASCII files and quickly visualize the data. 


## Level of Support

* This repository is fully supported by NSIDC. If you discover any problems or
  bugs, please submit an Issue. If you would like to contribute to this
  repository, you may fork the repository and submit a pull request.

See the [LICENSE](LICENSE.md) for details on permissions and warranties.  Please
contact nsidc@nsidc.org for more information.

# Scripts

## convert.py

Script/functions for converting snow depth text file for one year into a GeoTiff.

## read_all_cmc_daily_sdepth.py

Reads in the daily snow depth file for one year e.g. 'cmc_sdepth_dly_2019_v01.2.txt' and successively plots an array for each day 

## read_one_day_cmc_sdepth.py

Reads in the snow depth array for a user specified date and produces a quick plot of the array. 

## read_one_month_cmc_sdepth.py

Reads in the snow depth for a user specified month and produces a quick plot of the array. 


## read_one_month_cmc_swe.py

Reads in the monthly average swe for a user specified year and month and produces a quick plot of the array 

### Setup

The scripts require the numpy and matplotlib libraries. 

#### Example usage:

For the read_all_cmc_daily_sdepth.py
```
$ python read_all_cmc_daily_sdepth.py
```

For the read_one_day_cmc_sdepth.py and read_one_month_cmc_depth.py 
```
$ python read_one_day_cmc_sdepth.py
>Please input the file path (if applicable) and the name of the file you wish to read in e.g. cmc_sdepth_dly_2019_v01.2.txt
>cmc_sdepth_dly_2019_v01.2.txt
>Please input the date you wish to read, in the format YYYYMMDD00 e.g. 2019010500:
> 20190105
```
This will produce a quick plot the snow depth for the 5th Jan 2019. 

