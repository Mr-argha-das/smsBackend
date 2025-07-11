from typing import Optional
from pydantic import BaseModel


class CategoryIn(BaseModel):
    school_id: str
    name: str
    description: Optional[str] = None

class AssetIn(BaseModel):
    school_id: str
    category_id: str
    name: str
    description: Optional[str]
    quantity: int
    location: Optional[str] = "Store"
    assigned_to: Optional[str] = "Unassigned"
    condition: Optional[str] = "Working"

class MoveAssetIn(BaseModel):
    asset_id: str
    from_location: str
    to_location: str
    moved_by: str

class MaintenanceIn(BaseModel):
    asset_id: str
    cost: Optional[int] = 0
    notes: Optional[str] = ""