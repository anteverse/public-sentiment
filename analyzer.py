import json
from pymongo import MongoClient
from textblob import TextBlob


def sentiment_analysis(data):
    # prep data
    _data = json.loads(data)

    # we know these keys exist
    text = _data['text']
    coordinates = _data['coordinates']

    # sentiment analysis
    testimonial = TextBlob(text)
    polarity = testimonial.sentiment.polarity

    # save it to mongo
    client = MongoClient('localhost', 27017)
    db = client['sentiment']
    locations = db['locations']

    # coordinates are nested
    locations.insert_one(
        {
            "loc": coordinates['coordinates'],
            "text": text,
            "polarity": polarity
        }
    )

    client.close()

    return


# if __name__ == "__main__":
    # test_data = '{"text": "Our guest enjoying the colors of spring. #local #organic #heirloom @ Wild Flower \
# Restaurant, Bar\u2026 https://t.co/omZqi1cDqr", "coordinates": {"type": "Point", \
# "coordinates": [-90.26209302, 38.64026254]}}'
    # sentiment_analysis(test_data)
