import json
from datetime import datetime
from typing import Any, List, Optional, Union
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

from .models import FieldTypeChoices, RelationTypeChoices


class CustomFieldsConfigCreate(BaseModel):
    id: Optional[UUID4] = Field(default_factory=uuid4)
    name: str
    reference_id: str
    field_type: FieldTypeChoices
    is_active: bool
    entity_type: str
    created_by: Optional[UUID4]
    last_updated_by: Optional[UUID4]
    tenant_id: Optional[UUID4]


class CustomFieldsConfigPatch(BaseModel):
    name: Optional[str]
    reference_id: Optional[str]
    field_type: Optional[FieldTypeChoices]
    is_active: Optional[bool]
    entity_type: str
    created_by: Optional[UUID4]
    last_updated_by: Optional[UUID4]
    tenant_id: Optional[UUID4]


class CustomFieldsConfigResponse(BaseModel):
    id: UUID4
    name: str
    reference_id: str
    field_type: FieldTypeChoices
    is_active: bool
    created_by: Optional[UUID4]
    created_at: Optional[datetime]
    last_updated_by: Optional[UUID4]
    last_updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class PaginatedCustomFieldsConfigList(BaseModel):
    count: int
    next_page: Optional[int]
    previous_page: Optional[int]
    results: List[CustomFieldsConfigResponse]


class CustomFieldsRelationsRequest(BaseModel):
    relation_id: UUID4
    relation_type: str
    custom_field_configs: List[Optional[UUID4]]


class CustomFieldsRelationsResponse(BaseModel):
    relation_id: UUID4
    relation_type: str
    custom_field_configs: List[Optional[CustomFieldsConfigResponse]]


class CustomFieldsRelations(BaseModel):
    relation_id: UUID4
    relation_type: RelationTypeChoices
    cf_config_id: UUID4

    class Config:
        orm_mode = True


class CustomFieldValueResponseSchema(BaseModel):
    id: UUID4
    value: Optional[Union[str, float, int, list, dict]]
    created_at: Optional[datetime]
    created_by: Optional[UUID4]
    last_updated_at: Optional[datetime]
    last_updated_by: Optional[UUID4]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        obj.value = obj.field_value
        return super().from_orm(obj)


class CustomFieldValueRelatedConfigResponseSchema(BaseModel):
    id: UUID4
    name: Optional[str]
    reference_id: Optional[str]
    field_type: Optional[FieldTypeChoices]
    is_active: Optional[bool]

    class Config:
        orm_mode = True


class CustomFieldValueRequestSchema(BaseModel):
    id: Optional[UUID4]
    tenant_id: Optional[UUID4]
    cf_config_id: UUID4
    value: Optional[Union[str, float, int, list, dict]]
    field_value: Optional[Union[str, float, int, list, dict]]
    entity_id: UUID4
    created_at: Optional[datetime]
    created_by: Optional[UUID4]
    last_updated_at: Optional[datetime]
    last_updated_by: Optional[UUID4]


class CustomFieldvalueBareboneSchema(BaseModel):
    id: UUID4
    cf_config_id: UUID4
    entity_id: UUID4
    field_value: Optional[Union[str, float, int, list, dict]]
    created_at: Optional[datetime]
    created_by: Optional[UUID4]
    last_updated_at: Optional[datetime]
    last_updated_by: Optional[UUID4]

    class Config:
        orm_mode = True
