__author__ = "Christopher Tomkins-Tinch, Johannes Köster"
__copyright__ = "Copyright 2023, Christopher Tomkins-Tinch, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from typing import List, Optional, Type
from snakemake_interface_storage_plugins.tests import TestStorageBase
from snakemake_interface_storage_plugins.storage_provider import StorageProviderBase
from snakemake_interface_storage_plugins.settings import StorageProviderSettingsBase
from snakemake_storage_plugin_http import (
    ResponseHandler,
    StorageProvider,
    StorageProviderSettings,
)


class DummyResponse:
    def __init__(self, headers=None):
        self.headers = headers or {}


class TestStorageNoSettings(TestStorageBase):
    __test__ = True
    retrieve_only = True

    def get_query(self, tmp_path) -> str:
        return "https://www.google.com"

    def get_query_not_existing(self, tmp_path) -> str:
        return "https://www.google.com/this/does/not/exist"

    def get_storage_provider_cls(self) -> Type[StorageProviderBase]:
        return StorageProvider

    def get_storage_provider_settings(self) -> Optional[StorageProviderSettingsBase]:
        return StorageProviderSettings()

    def get_example_args(self) -> List[str]:
        return []


def test_response_handler_size_from_content_length():
    response = DummyResponse(headers={"Content-Length": "12345"})
    assert ResponseHandler(response).size() == 12345


def test_response_handler_size_from_content_range():
    response = DummyResponse(headers={"Content-Range": "bytes 0-0/98765"})
    assert ResponseHandler(response).size() == 98765
