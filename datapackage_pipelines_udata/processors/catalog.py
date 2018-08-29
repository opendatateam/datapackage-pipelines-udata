from datapackage_pipelines.wrapper import ingest, spew

parameters, datapackage, res_iter = ingest()

spew(datapackage, res_iter)
