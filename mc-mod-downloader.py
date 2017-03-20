#!/usr/bin/env python3

import os
import sys
import json
import argparse
import re
from pprint import pprint
from urllib.request import urlopen, urlretrieve


# directory in which to put the mods
path = './downloaded-mods'

curseforge_mod_url = 'https://minecraft.curseforge.com/mc-mods/'


parser = argparse.ArgumentParser(description='Simple Minecraft mod downloader.')
parser.add_argument('json_file', help='the manifest.json of the modpack')
args = parser.parse_args()

with open(args.json_file) as json_file:    
    data = json.load(json_file)
    files = data['files']

# mode=755 doesn't work, I don't care
os.makedirs(path, mode=755, exist_ok=True)

pprint('Downloading:')
for f in files:
    projectID = str(f['projectID'])
    mod_url = curseforge_mod_url + projectID

    response = urlopen(mod_url)
    if response.getcode() == 200:
        project_url = response.geturl()
        project_url = re.sub('\?cookieTest=1$', '/', project_url)
        dl_url = project_url + 'files/' + str(f['fileID']) + '/download'

        pprint(dl_url)

        zip_resp = urlopen(dl_url)
        if zip_resp.getcode() == 200:
            url_zipfile = zip_resp.geturl()
            zip_name = url_zipfile.split('/')[-1]
            urlretrieve(url_zipfile, path + '/' + zip_name)
