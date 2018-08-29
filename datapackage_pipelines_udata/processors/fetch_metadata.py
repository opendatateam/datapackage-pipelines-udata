import requests
import logging
from datapackage_pipelines.wrapper import ingest, spew
from datapackage_pipelines.generators import slugify
from datapackage_pipelines.utilities.resources import PATH_PLACEHOLDER, PROP_STREAMED_FROM

parameters, datapackage, _ = ingest()

host = parameters['host']
object_id = parameters['id']

url = f"https://{host}/api/1/datasets/{object_id}"

def metadata(url_):
    r = requests.get(url=url_)
    metadata = r.json()

    return metadata

dataset_metadata = metadata(url)

datapackage['udata'] = dataset_metadata 

# logging.info(datapackage)

for resource in dataset_metadata['resources']:
    
    # logging.info(resource)

    name = slugify(resource["title"].lower())
    path = resource["url"].split('/')[-1]
    format = resource["format"]
    url = resource["url"]

    logging.info(path)

    if path is not '':

        datapackage['resources'].append({
            'name': name,
            PROP_STREAMED_FROM: url,
            'format': format,
            'path': path
        })

parameters[PROP_STREAMED_FROM] = url
#datapackage['resources'].append(parameters)

stats = {
    "new resources": 0
}

spew(datapackage, _, stats)
