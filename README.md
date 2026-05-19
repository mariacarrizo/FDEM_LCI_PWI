[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.20282212)

# FDEM_LCI_PWI
Repository for publication: [Impact of non-1D Earth on FDEM measurements and the performance of PWI and LCI Inversions](<https://doi.org/10.1016/j.jappgeo.2026.106130>)

### Requirements
- Python 3
- Other libraries such as `empymod` and `pygimli` listed in `requirements.txt`

### Installation
1. Clone the repository
2. Install `pygimli` in a separate conda environment
Open a terminal (Linux & Mac) or the Anaconda Prompt (Windows) and type
```
conda create -n pg -c gimli -c conda-forge pygimli=1.4.6
```
3. Activate your environment
If you are using Windows or Mac, a new environment named “pg” should be visible in the Anaconda Navigator. If you want to use pyGIMLi from the command line, you have to activate the environment. 
```
conda activate pg
```
For more information about pygimli instalation go to <https://www.pygimli.org/installation.html>

4. Install dependencies
```
pip install -r requirements.txt
```

## Notes
- Data is simulated for an EMI device with the following characteristics
  - Frequency: 9000 Hz
  - Geometries: Horizontal coplanar (H) with offsets [2 m, 4 m, 8 m],
    Vertical coplanar (V) with offsets [2 m, 4 m, 8 m],
    and Perpendicular (P) with offsets [2.1 m, 4.1 m, 8.1 m]

## Data
- Field data acquired with a DUALEM842s EMI instrument is stored in file `FieldCase/data/Field_data.npy`
```

### References
Forward modelling using `empymod` from: [Werthmüller (2017)](<https://doi.org/10.1190/geo2016-0626.1>).
