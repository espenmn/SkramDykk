# Fetch data 

This code fetches files from the Saivas ftp server and store the data to MongoDB.

The MongoDB database is `saivasdata` and the collection is `gabrielraw` 

The data stored to MongoDB will look like this:
```JSON
{
    "_id" : ObjectId("579860881a8e51751d9d366c"),
    "devicename" : "Gabriel",
    "profilenumber" : 4696,
    "location" : {
        "coordinates" : [ 
            60.229497, 
            5.205398
        ],
        "type" : "Point"
    },
    "airtemp" : -0.2,
    "filename" : "16042501.txt",
    "startdatetime" : ISODate("2016-04-25T02:00:30.000Z"),
    "sessionid" : LUUID("dcdaeb75-62fa-40a3-8815-2a6955451987"),
    "rawtimeseries" : [ 
        {
            "fluorescens" : 0.31,
            "pressure(dBAR)" : 0.0,
            "oxygene" : 98.84,
            "turbidity" : 0.03,
            "temp" : 6.049,
            "salt" : 0.0,
            "seq" : 1
        }, ...
   ],
}
```

