import xata
from xata import XataClient
from data_store import DataStoreItem

class XataDatabase(XataClient):
    db: XataClient = None
    
    def __init__(
        self,
        api_key: str = None,
        region: str = ...,
        workspace_id: str = None,
        db_name: str = None,
        db_url: str = None,
        branch_name: str = ...,
        domain_core: str = ...,
        domain_workspace: str = ...
    ):
        self.db = super().__init__(
            api_key,
            region,
            workspace_id,
            db_name,
            db_url,
            branch_name,
            domain_core,
            domain_workspace
        )
    
    def commit(self, items: list[DataStoreItem]) -> None:
        self.records().transaction({
            "operations": [
                { "insert": "table" "" }
            ]
        })
