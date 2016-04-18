from pymongo import MongoClient
from bson import SON
import config
import json
import web
import pymongo

urls = (
    '/location/([0-9-\.]+),([0-9-\.]+),([0-9\.]+)', 'Locations',
)

f = file('config.conf')
cfg = config.Config(f)

client = MongoClient('localhost', 27017)
db = client['sentiment']

class Locations:
    def GET(self, lng, lat, radius):
        """
        GET /location/longitude,latitude,radius:
            - longitude must be float (mandatory)
            - latitude must be float (mandatory)
            - radius must be positive float (mandatory)
        """
        # LONGITUDE, LATITUDE, RADIUS
        if not lng or not lat or not radius:
            raise web.forbidden()

        # DB call
        # SON converts python dict to bson obj to avoid keys ordering issues
        cursor = db['locations'].find(
            {"loc": SON([('$near', [float(lng), float(lat)]), ('$maxDistance', float(radius))])}
        )

        cursor.sort('polarity', pymongo.ASCENDING)
        if cursor:
            results = list(cursor)
            if len(results):

                # aggregation here, but should be done in Mongo
                c = len(results)
                worst = {"text": results[0]['text'], "loc": results[0]['loc']}
                best = {"text": results[-1]['text'], "loc": results[-1]['loc']}
                avg = reduce(lambda x, y: x+y, map(lambda x: x['polarity'], results)) / float(c)

                # New line added at the end for inline automation
                return json.dumps(
                        {
                            "tweets": str(c),
                            "average": str(avg),
                            "most_positive": {
                                "text": best['text'],
                                "coordinates": best['loc']
                            },
                            "most_negative": {
                                "text": worst['text'],
                                "coordinates": worst['loc']
                            }
                        }
                ) + "\n"

        return 'No results\n'

    def POST(self, location):
        raise web.nomethod

    def PUT(self, location):
        raise web.nomethod

    def DELETE(self, location):
        raise web.nomethod


def test_db_connect():
    """
    Test the connection:
    """
    client = MongoClient('localhost', 27017)
    db = client['sentiment']
    rows = db['locations'].find()
    client.close()
    return rows


def test_db_query():
    """
    Test the query:
        - drop index
        - create index
        - basic query check
    """
    client = MongoClient('localhost', 27017)
    db = client['sentiment']

    db['locations'].drop_indexes()
    db['locations'].create_index([("loc", pymongo.GEO2D)], name='geo_index')
    print 'index OK'
    rows = []
    try:
        rows = db['locations'].find({"loc": SON([('$near', [-90.262, 38.640]), ('$maxDistance', 3)])})
    except TypeError:
        print 'check query format'
    client.close()
    return rows

if __name__ == "__main__":
    test_db_query()
    # print list(test_db_query())
    app = web.application(urls, globals())
    app.run()
