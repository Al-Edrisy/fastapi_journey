from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from typing import Any, List, Optional, Type
from models.events import Event
from models.users import User

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = "mini-project-2/.env"

async def initialize_database():
    settings = Settings()
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database=client.get_default_database(),
                      document_models=[Event, User])

class Database:
    def __init__(self, model: Type[Any]):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        data = await self.model.find_all().to_list()
        return data

    async def update(self, id: PydanticObjectId, body: Any) -> Any:
        doc_id = id
        des_body = body.dict()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": des_body}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
