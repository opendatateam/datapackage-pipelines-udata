import os
import json

from datapackage_pipelines.generators import \
    GeneratorBase, slugify, steps, SCHEDULE_MONTHLY

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), 'schema.json')


class Generator(GeneratorBase):

    @classmethod
    def get_schema(cls):
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "name":          { "type": "string" },
                "udata-instance": { "type": "string" },
                "data-kind":     { "type": "string" },
                'dataset': { "type": "string" }
            }
	}

    @classmethod
    def generate_pipeline(cls, source, wp):
        pipeline_id = dataset_name = slugify(source['name'])
        host = source['udata-instance']
        action = source['data-kind']

        if action == 'datasets-list':
            schedule = SCHEDULE_MONTHLY
            pipeline_steps = steps(*[
                ('udata.catalog', {
                   'udata-instance': host
                }),
                ('add_metadata', {
                  'name': dataset_name
                }),
                ('dump.to_zip', {
                   'out-file': 'udata-list.zip'
                })])
            
            pipeline_details = {
                'pipeline': pipeline_steps,
                'schedule': {'crontab': schedule}
            }
            
            yield pipeline_id, pipeline_details

        if action == 'dataset':
            
            pipeline_steps = steps(*[
                ('udata.fetch_metadata', {
                    'host': source['udata-instance'],
                    'kind': 'dataset',
                    'id': source['dataset']
                }),
                ('add_metadata',{
                    'name': source['name']
                }),
                ('dump.to_path',{
                    'handle-non-tabular': 'true',
                    'pretty-descriptor': 'true'
                })
            ])

            pipeline_details = {
                'pipeline': pipeline_steps
            }

            yield pipeline_id, pipeline_details

