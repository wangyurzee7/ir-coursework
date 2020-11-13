# ir-coursework

IR Coursework

## Dataset

Please run Elastic Search server first.

Please put `rmrb1946-2003-delrepeat.all` at `dataset/src/` first.

```
cd THULAC
./thulac -output ../dataset/rmrb.txt <../dataset/src/rmrb1946-2003-delrepeat.all

cd ../dataset
python3 structuring.py -i rmrb.txt --rebuild-dataset
```

## Run Website

```
cd fronted
python3 manage.py runserver
```

## Report

See `report.pdf` or `report.md`.