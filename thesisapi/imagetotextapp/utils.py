import os
import requests
import time


def create_extraction(extraction):
    token = os.getenv('API_KEY')

    url = "https://api.extracta.ai/api/v1/createExtraction"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {token}"}
    extraction_details = {
        "name": "lol",
        "language": "Multi-Lingual",
        "fields": [
            {
                "key": "merchant",
                "description": "the merchant in the invoice",
                "type": "object",
                "properties": [
                    {
                        "key": "merchant_name",
                        "description": "name of the merchant",
                        "example": "ΣΚΛΑΒΕΝΙΤΗΣ",
                        "type": "string"
                    },
                    {
                        "key": "merchant_address",
                        "description": "address of the merchant",
                        "example": "ΛΕΩΦ. ΚΗΦΙΣΟΥ 80",
                        "type": "string"
                    },
                    {
                        "key": "merchant_tax_id",
                        "description": "tax id or vat id of the merchant",
                        "example": "ΑΦΜ: 325238975",
                        "type": "string"
                    }
                ]
            },
            {
                "key": "items",
                "description": "the items in the receipt",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": [
                        {
                            "key": "name",
                            "example": "Item 1",
                            "type": "string"
                        },
                        {
                            "key": "quantity",
                            "example": "1",
                            "type": "string"
                        },
                        {
                            "key": "unit_price",
                            "description": "return only the number as a string.",
                            "example": "100.00",
                            "type": "string"
                        },
                        {
                            "key": "total_price",
                            "description": "return only the number as a string.",
                            "example": "100.00",
                            "type": "string"
                        }
                    ]
                }
            },
            {
                "key": "grand_total",
                "description": "The total amount after tax has been added. This should capture the final payable amount. Return only the number as a string.",
                "example": "25,00",
                "type": "string"
            }
        ]
    }

    response = requests.post(
        url, json={"extractionDetails": extraction_details}, headers=headers)
    response.raise_for_status()
    response_data = response.json()

    print(response_data)
    return response_data


def upload_file(extraction_id, extraction):
    token = os.getenv('API_KEY')

    url = "https://api.extracta.ai/api/v1/uploadFiles"
    headers = {
        # "Content-Type": "multipart/form-data",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "extractionId": extraction_id,
    }
    response = requests.post(
        url, files={"files": open(extraction.image.path, 'rb')}, data=payload, headers=headers)
    response.raise_for_status()
    print('response', response)

    response_data = response.json()

    print('response_data', response_data)

    return response_data


def get_results(extraction_id, batch_id):
    try:
        token = os.getenv('API_KEY')

        url = "https://api.extracta.ai/api/v1/getBatchResults"
        headers = {
            # "Content-Type": "multipart/form-data",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "extractionId": extraction_id,
            "batchId": batch_id
        }
        response = requests.post(
            url, data=payload, headers=headers)
        response.raise_for_status()
        print('response', response)

        response_data = response.json()

        print('response_data', response_data)

        return response_data
    except Exception as e:
        print(f"Error in get_results: {e}")
        return None


def send_image_to_api(extraction):
    print('send_image_to_api', extraction)
    # create extraction
    extraction_data = create_extraction(extraction)
    # upload file
    upload_file_data = upload_file(extraction_data['extractionId'], extraction)
    # get results
    # time.sleep(60)
    # results = get_results(
    #     upload_file_data['extractionId'], upload_file_data['batchId'])
    return upload_file_data


def update_extraction_data(extraction, extraction_data):
    if not extraction_data:
        print("Error: extraction_data is None")
        return None
    
    # Save basic extraction details
    extraction.extraction_id = extraction_data.get('extractionId')
    extraction.batch_id = extraction_data.get('batchId')
    extraction.save()
    
    # Check if we have files with results
    if 'files' in extraction_data and extraction_data['files']:
        file_data = extraction_data['files'][0]  # Get the first file
        
        # Check if the file has results
        if 'result' in file_data:
            result = file_data['result']
            
            # Create merchant if it exists in results
            if 'merchant' in result:
                merchant_data = result['merchant']
                merchant, created = Merchant.objects.get_or_create(
                    merchant_name=merchant_data.get('merchant_name', ''),
                    defaults={
                        'merchant_address': merchant_data.get('merchant_address', ''),
                        'merchant_tax_id': merchant_data.get('merchant_tax_id', '')
                    }
                )
                extraction.merchant = merchant
                extraction.save()
            
            # Create extraction items if they exist in results
            if 'items' in result:
                for item_data in result['items']:
                    ExtractionItem.objects.create(
                        extraction=extraction,
                        product_name=item_data.get('name', ''),
                        product_price=item_data.get('unit_price', 0),
                        quantity=int(item_data.get('quantity', 0))
                    )
    
    return extraction
