from api import get_follower_ids, get_following_ids
import csv
import os

write_file = "user_ids.csv"
directory = "user_info"
with open(write_file, 'wb') as wfile:
    writer = csv.writer(wfile, delimiter=',')
    for filename in os.listdir(directory):
        print filename
        with open(os.path.join(directory, filename), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for row in reader:
                writer.writerow([row[0]])
