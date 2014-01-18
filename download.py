import argparse
import json
import os
from urllib import request

LIST_URL='http://archive.org/advancedsearch.php?q=collection%3A{0}&rows=1000&output=json'
DETAILS_URL='https://archive.org/details/{0}&output=json'
PUB_URL='http://archive.org/download/{0}/{1}'

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
    print('Fetching item details for {0}'.format(id))
    details = json.loads(request.urlopen(DETAILS_URL.format(id)).read().decode('UTF-8'))
    toDownload = ''
    lastSize = 0
    for filename in details['files']:
        if not filename.lower().endswith(args.format):
            continue
        size = int(details['files'][filename]['size'])
        if size > lastSize:
            toDownload = filename
            lastSize = size
    if toDownload == '':
        print('No {0} file found for {1}'.format(args.format), id)
        continue


    url = PUB_URL.format(id, toDownload)
    localFilename = os.path.join(args.destination, '{0}.{1}'.format(id, args.format))
    print('Downloading {0} as {1} from {2} to {3}'.format(id, args.format, url, localFilename))
    request.urlretrieve(url, localFilename)
