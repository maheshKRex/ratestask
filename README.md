# HTTP-based API - Rates Task Solution

Returns a list with the average prices for each day on a route between port codes origin and destination. Return an empty value (JSON null) for days on which there are less than 3 prices in total.

## Launching the App and DB instances
### Dev Environment
```
docker-compose up
```

### Run Test Enviroment with Automated Testing
```
docker-compose -f docker-compose.test.yml up
```


## API Usage
### Request Query Parameters

``` 
date_from
date_to
origin
destination
```

## Usage

```python
# get average prices between CNGGZ and BEANR from  2016-01-01 to 2016-01-30
curl --location 'http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-30&origin=CNGGZ&destination=BEANR'

# get average prices between CNSGH and north_europe_main from  2016-01-01 to 2016-01-10
curl --location 'http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main'

# update Rates table in DB to have less than 3 records for one of the sets of pricing records for some of the origin and destination combinations, and expect the average price as null for those having less than 3 records
curl --location 'http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNGGZ&destination=EETLL'

[
    {
        "average_price": "1155",
        "day": "2016-01-01"
    },
    {
        "average_price": "1155",
        "day": "2016-01-02"
    },
    {
        "average_price": null,
        "day": "2016-01-03"
    },
    {
        "average_price": null,
        "day": "2016-01-05"
    },
    ...
]


```
