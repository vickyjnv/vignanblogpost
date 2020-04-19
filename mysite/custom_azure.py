from storages.backends.azure_storage import AzureStorage
import os

class AzureMediaStorage(AzureStorage):
    account_name = 'viitblog' # Must be replaced by your <storage_account_name>
    account_key = os.environ['ACCOUNT_KEY1']
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'viitblog' # Must be replaced by your storage_account_name
    account_key = os.environ['ACCOUNT_KEY2']
    azure_container = 'static'
    expiration_secs = None