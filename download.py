import argparse
import json
import os
from urllib import request

LIST_URL='http://archive.org/advancedsearch.php?q=collection%3A{0}&rows=1000&output=json'
PUB_URL='http://archive.org/download/{0}/{0}.{1}'

parser = argparse.ArgumentParser(description='Download stuff from an archive.org JSON file')
parser.add_argument('--format', help='pdf or epub', default='pdf')
parser.add_argument('--collection', help='Name of the collection to fetch', required=True)
parser.add_argument('--destination', help='Where to put the files', default='.')
args = parser.parse_args()

url = LIST_URL.format(args.collection)
print('Fetching document list from {0}'.format(url))
response = request.urlopen(url)
listdata = response.read()
data = json.loads(listdata.decode('UTF-8'))

for doc in data['response']['docs']:
    id = doc['identifier']
    url = PUB_URL.format(id, args.format)
    filename = os.path.join(args.destination, '{0}.{1}'.format(id, args.format))
    print('Downloading {0} as {1} from {2} to {3}'.format(id, args.format, url, filename))
    request.urlretrieve(url, filename)
