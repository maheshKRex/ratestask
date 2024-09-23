# HTTP-based API - Rates Task Solution

Returns a list with the average prices for each day on a route between port codes origin and destination. Returns an empty value (JSON null) for days on which there are less than 3 prices in total.

## Launching the App and DB instance by different environemnt
The app is deployable into dev/test/prod environments using following setup:
### Dev Environment
```
# configurable via .dev.env environment variables
# Port number
# PORT=5000
## Database credentials
# DATABASE_HOST
# DATABASE_NAME
# DATABASE_USER
# DATABASE_PASSWORD
## configured docker-compose.yml to deploy DB, app
docker-compose up

## similarly other environments are deployable by setting separate .env and docker-compose.yml configurations for separate environments, with their own DB, PORT, environment name settings
## test environment
#  python app.py --config=test
## prod environment
#  python app.py --config=prod
```

### Run Automated E2E Tests
```
# configurable via .test.env environment variables
# Port number
# PORT=5000
## Test Database credentials
# DATABASE_HOST
# DATABASE_NAME
# DATABASE_USER
# DATABASE_PASSWORD
## configured docker-compose.test.yml to deploy DB, app and pytests 
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
## Code Structure
```
.
├── README.md
├── app.py
├── app
│   ├── __init__.py
│   └── # app implementation with REST API endpoint, query param validation, Raw SQL query to fetch data, instead of using an ORM as advised in assignment
├── database
│   ├── __init__.py
│   └── # database connection setup using env vars
├── app.Dockerfile # app service docker file
├── database.Dockerfile # database service docker file
├── config.py # configuration setup for CLI option to trigger --config=(dev/test/prod)
├── docker-compose.test.yml # docker compose for launching automated tests
├── docker-compose.yml # docker compose for launching dev app, db
├── rates.sql
├── requirements-prod.txt # necessary dependencies for a prod release
├── requirements-test.txt # dependencies for automated tests/ dev enviornment
└── tests
    ├── __init__.py
    └── ratestask_test.py
    └── # e2e tests validating happy path, negative cases involving all possible query param variations, including invalid dates per calendar and empty origin/ destination values and verifying capturing all errors (not just first) in the query parmeter validations

```
