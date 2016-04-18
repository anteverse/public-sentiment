Average geolocalized sentiment on public tweets
===============================================

Description
-----------
`public-sentiment` provides is an API that provides sentiment statistics on geolocalized tweets.
The repository gathers:
- a twitter stream listener
- a distributed sentiment analyzer
- an API that allows locations parameters and returns sentiment statistics


Requirements
-----------
The service is running on python 2.7.*

Python libraries required:
- web
- json
- redis
- rq
- textblob
- config
- tweepy
- pika
- bson
- pymongo

Servers to set up:
- RabbitMQ (messaging)
- Redis + RQ (methods queuing)
- MongoDB
- (optional) nginx to build a reverse proxy

Getting started
-----------
Open the command line and cd to the solution forlder:
```sh
$ git clone https://github.com/anteverse/public-sentiment
```

#### Starting RabbitMQ, Redis and RQ
cd to the root the folder:
```sh
$ cd public-sentiment/
```
Assuming you're running a server OS, you can install Redis and RabbitMQ, and let them start automatically.
You should start RQ server from that location, otherwise you'll get ImportErrors:
```sh
$ rq worker
```
if you want to debug, or,
```sh
$ rq worker &> /dev/null &
```
if you don't want to see the logs.
At this point, you've started Redis, RabbitMQ and RQ.

#### Starting the workers + listener
Still in the root folder `public-sentiment/`, you should start several command.

You can set up a few workers with (in each command):
```sh
$ python worker.py
```
Each of them will print actions done. Nothing is printed so far though, we need to start the main listener. Open a new command, still in the same folder:
```sh
$ python server.py
```
After a few seconds it starts to send messages to the workers. The balancing schedule used by default is Round Robin. You should see messages being sent to the workers now.
If you read the prints from RQ you should see the `sentiment_analysis` method being queued. Depending on the filters you set on the stream listener and the number of workers you have, you can get a lot of messages per second.

The analysis is done under the method `sentiment_analysis`, and then stored in MongoDB. The database name is *sentiment* and the collection is *locations*.

Documents format:
```json
{
    "_id": "ObjectId()",
    "text": "text from tweet",
    "polarity": "from -1.0 to 1.0",
    "loc": ["longitude", "latitude"]
}
```
From this point listener and analyzer(s) are up and running.

#### Starting the webserver
```sh
$ python app.py {PORT}
```

You may want to use a reverse proxy to redirect HTTP inbound traffic (IP:80) to your python server. Please refer to that link: [Virtual Hosts with Nginx](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-web-server-and-reverse-proxy-for-apache-on-one-ubuntu-14-04-droplet). See Step 7 in particular.

The API provides one unique endpoint, which is decribed below.

A test query is run right before the actual boot of the webserver. It first drop indexes and then build a *geo index* on the location collection. It finally checks the objects returned when querying the location collection. Geo queries can't be run if the collection is not geo indexed.

API endpoint
-----------
#### Description
- `GET` `/location/{longitude},{latitude},{radius}`

Coordinates are coma separated. If any of these 3 params is missing, you're gonna get an access forbidden. Longitude is always first and latitude second. Radius is measured in degrees: 1 degree ~111.12 km or ~69 miles.

It return a document of that form:
```json
{
    "tweets": "11", 
    "average": "0.101136363636", 
    "most_positive": {
        "text": "text", 
        "coordinates": [-90.3371889, 38.6105426]
    },
    "most_negative": {
        "text": "text", 
        "coordinates": [-92.35901356, 38.9696862]
    }
}
```

#### Tests
You can run the _almost empty_ test_app.sh to test the API.

License
-----------
Please refer to the license document.

