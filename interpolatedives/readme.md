# Documentation for processing of dive data

We are reading one dive data-set at a time and interpolate.
By using the "force" option all documents will be updated - previous conversions will not be overwritten

# down-draft and up-draft 

We do filter away up-draft values. In pandas this is very simple when the dataframe is cronologically sorted:

```python
df = df.iloc[:df.index.argmax()]
```

# interpolation

The interpolation is based on pandas. We insert the depth values (depth_set) we want and interpolate afterwards:

```python
depth_set = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5]
for x in depth_set:
    if x not in df.index and x < df.index.max():
        df.ix[x] = nan
df = df.sort_index()
df = df.interpolate(method='index', axis=0).ffill(axis=0).bfill(axis=0)
```

To remove rows we do not need to show we simply do:
```python
query = "index in "  + json.dumps(depth_set)
df = df.query(query)
```

# Links

http://stackoverflow.com/questions/2745329/how-to-make-scipy-interpolate-give-an-extrapolated-result-beyond-the-input-range

https://pypi.python.org/pypi/ctd
 
http://nbviewer.jupyter.org/github/castelao/seabird/blob/master/docs/notebooks/BasicsReadingData.ipynb



