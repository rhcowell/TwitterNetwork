import tweepy
from api import get_follower_ids, get_following_ids
import csv
import os
import json
import logging

id_file = "user_ids.csv"
directory = "user_info"
ids_per = 250
logging.basicConfig(filename='scrape.log', level=logging.INFO)

def create_id_csv():
    with open(id_file, 'wb') as write_file:
        writer = csv.writer(write_file, delimiter=',')
        for filename in os.listdir(directory):
            print filename
            with open(os.path.join(directory, filename), 'rb') as read_file:
                reader = csv.reader(read_file, delimiter=',')
                next(reader)
                for row in reader:
                    writer.writerow([row[0], row[2]])


def get_network(id):
    followers = get_follower_ids(id)
    following = get_following_ids(id)
    return followers, following


def graph_json():
    ids = []
    num = 0
    graph = []

    with open(id_file, 'rb') as read_file:
        reader = csv.reader(read_file, delimiter=',')
        for row in reader:
            ids.append(row)

    for i in range(len(ids)):
        source = ids[i][0]
        source_name = ids[i][1]

        if "+" in source:
            source = source_name

        if i % ids_per == 0:
            num += 1
            if num > 1:
                json.dump(graph, write_file, indent=4, sort_keys=True)
            write_file = open("graph" + str(num) + ".json", 'wb')
            graph = []

        relationships = {source: {"followers": None, "following": None}}

        try:
            followers, following = get_network(source)
            relationships[source]["followers"] = followers
            relationships[source]["following"] = following
            logging.info("SUCCESSFULLY got %s" % source)

        except tweepy.TweepError:
            logging.error("FAILED to get %s" % source)

        graph.append(relationships)


if __name__ == "__main__":
    graph_json()