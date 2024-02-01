import azure.functions as func
import datetime
import json
import logging
import csv
import codecs
from additional_functions import bp

app = func.FunctionApp()
app.register_blueprint(bp)

@app.function_name('FirstHTTPFunction')
@app.route(route="myroute", auth_level=func.AuthLevel.ANONYMOUS)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
        "Wow this first HTTP Function works!!!!",
        status_code=200
    )

@app.function_name('SecondHTTPFunction')
@app.route(route="newroute")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting the second HTTP Function request')

    name=req.params.get('name')
    if name:
        message = f"Hello, {name}, so glad this function worked!!"
    else:
        message = "Hello, so glad this function worked!!"
    return func.HttpResponse(
        message,
        status_code=200
    )

@app.function_name(name="MyFirstBlobFunction")
@app.blob_trigger(arg_name="myblob",
                  path="newcontainer/output.json",
                  connection="AzureWebJobsStorage")
def test_function(myblob: func.InputStream):
    logging.info(f"Python blob function triggered after output.json file was uploaded"
                 f"Print the name of the blob path:{myblob.name}"
                 )

@app.function_name(name="ReadFileBlobFunction")
@app.blob_trigger(arg_name="readfile",
                  path="newcontainer/output.json",
                  connection="AzureWebJobsStorage")
def main(readfile: func.InputStream):
    reader=csv.reader(codecs.iterdecode(readfile,'utf-8'))
    for line in reader:
        print(line)
