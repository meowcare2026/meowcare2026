from typing import Any, Literal

from pydantic import BaseModel


AdminLogAction = Literal[
    "create",
    "update",
    "delete",
    "login",
    "logout",
]


class AdminLogAdminResponse(BaseModel):
    id: str
    name: str
    role: str


class AdminLogResponse(BaseModel):
    id: str
    admin_id: str | None
    action: AdminLogAction
    table_name: str
    record_id: str | None
    description: str | None
    old_data: dict[str, Any] | None
    new_data: dict[str, Any] | None
    created_at: str
    admin: AdminLogAdminResponse | None = None