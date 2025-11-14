import azure.functions as func
import os
import json
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="retrieveMaxCut")
def retrieveMaxCut(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    job_id = req_body.get("jobID")
    
    # get managed identity credential
    mgcredential = ManagedIdentityCredential()

    # Connect to Storage Account
    storage_account_name = os.environ['quantumStorageAccount']
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        credential=mgcredential
    )

    # read content from blog
    container_name = f"job-{job_id}"
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client("outputData")
    blob_content = blob_client.download_blob().content_as_text()

    # parsing the output of the quantum computer
    # to find the top 3 measurement with the highest count
    result = json.loads(blob_content)["Results"][0]["Histogram"]
    sorted_histogram = sorted(result, key=lambda x: x["Count"], reverse=True)
    top_result = sorted_histogram[0]["Outcome"]

    return func.HttpResponse(f"Hey, this is the likely max cut: {top_result}.")


    