import os
import json
from dotenv import load_dotenv
from sqlalchemy import select

from data.__init__ import fake_db


async def add_fake_users(session_maker):
    load_dotenv()
    fake_users_str = os.getenv("FAKE_USERS")
    fake_users = json.loads(fake_users_str)
  
    async with session_maker() as session:
        for user_data in fake_users.values():
            exists = await session.execute(
                select(fake_db).where(fake_db.name == user_data["name"])
            )
            if not exists.scalar_one_or_none():
                session.add(fake_db(**user_data))
        await session.commit()