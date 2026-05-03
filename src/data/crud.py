
from sqlalchemy import select

from data.__init__ import User


async def add_fake_users(session_maker, fake_users):
    async with session_maker() as session:
        for user_data in fake_users.values():
            exists = await session.execute(
                select(User).where(User.username == user_data["username"])
            )
            if not exists.scalar_one_or_none():
                session.add(User(**user_data))
        await session.commit()