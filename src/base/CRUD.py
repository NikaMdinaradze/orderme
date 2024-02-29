from uuid import UUID

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from tortoise.models import Model


class CRUDBase:
    def __init__(self, model: Model):
        self.model = model

    async def get(self, id: UUID):
        object_db = await self.model.get_or_none(id=id)
        if not object_db:
            raise HTTPException(status_code=404, detail="Item not found")
        return object_db

    async def create(self, schema: BaseModel):
        object_data = jsonable_encoder(schema)
        object_db = self.model(**object_data)
        await object_db.save()
        return object_db

    async def update(self, id: UUID, schema: BaseModel):
        object_db = await self.get(id=id)
        object_data = jsonable_encoder(schema)
        update_data = object_data.dict(exclude_unset=True)

        for field, value in update_data:
            setattr(object_db, field, value)
        await object_db.save()
        return object_db

    async def remove(self, id: UUID):
        object_db = await self.get(id=id)
        await object_db.delete()
