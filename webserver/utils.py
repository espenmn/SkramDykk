import pymongo
import pandas as pd

def generate_freq(title):
    coll = pymongo.MongoClient().saivasdata.gabrielraw

    l = list(coll.find(projection={"startdatetime":True, "_id":False}).sort([("startdatetime",pymongo.ASCENDING)]))
    df = pd.DataFrame(l)
    df.index = df['startdatetime']
    ndf = df.groupby(df.index.date).count()

    graphs = [
        dict(
            data=[
                dict(
                    x=ndf.index,
                    y=ndf['startdatetime'],
                    type='Scatter',
                    mode='markers'
                ),
            ],
            layout=dict(
                title=title
            )
        )
    ]


def generate_datasets(timeframe, datatype, title):

    coll = pymongo.MongoClient().saivasdata.resampled
    tempz = []
    y = []
    x = []
    for curs in coll.find({"timeframe": timeframe, "datatype": datatype}).sort("ts", pymongo.ASCENDING):
        # print(curs)

        col = []
        # sort the list so the dictionaries are sorted according to pressure
        newlist = sorted(curs['divedata'], key=lambda k: -k['pressure(dBAR)'])
        for i in newlist:
            col.append(i[datatype])
            if -i['pressure(dBAR)'] not in y:
                y.append(-i['pressure(dBAR)'])

        tempz.append(col)
        x.append(curs['ts'])
    z = list(map(list, zip(*tempz)))
    y = sorted(y)

    graphs = [
        dict(
            data=[
                dict(
                    z=z,
                    x=x,
                    y=y,
                    type='heatmap'
                ),
            ],
            layout=dict(
                title=title
            )
        )
    ]

    return graphs
