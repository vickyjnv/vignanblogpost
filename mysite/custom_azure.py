from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'viitblog' # Must be replaced by your <storage_account_name>
    account_key = '3O2eDeGi3ZpDTXSFX8KVsTv2w8vcVumGQ/8rYXhaamDve2WN71thA1sc+GoSr8JbkFL5F1MEw4ed4bvhCBfIbQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'viitblog' # Must be replaced by your storage_account_name
    account_key = 'pjYOWF+ZKPUdKEt5PMbIJoXLiGUftLWeTHXASe16AeyGLNIdvk5gLWfEef3UkWKgtmHmrvjmvF2YMuV43kRC7g==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None