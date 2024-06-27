from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from code.functions import password_hash, password_verify
from code.models import User, Base

DATABASE_URL = "sqlite+aiosqlite:///./database/users.db"

#  асинхронный движок SQLAlchemy для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)

# создание таблицы в базе данных, только при первом запуске!
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# создается асинхронная сессия для взаимодействия с базой данных
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# добавление нового пользователя
async def create_user(username: str, password: str, role: str ):
    async with async_session_maker() as session:
        try:
            user = User(username=username, password=password, role=role)
            session.add(user)
            await session.commit()
            return user  # возврат созданного пользователя
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при создании пользователя: {e}")
            return None

# получение всех пользователей
async def get_all_users():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        if not result:
            return []  # пустой список, если пользователей нет
        return result.scalars().all()

# удаление пользователя по ID
async def delete_user_id(user_id: int):
    async with async_session_maker() as session:
        try:
            # вычисляем пользователя по ID
            user = await session.get(User, user_id)
            if not user:
                return None  # пользователь не найден

            # Удаляем пользователя
            await session.delete(user)
            await session.commit()
            return user  # возврат удаленного пользователя
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при удалении пользователя: {e}")
            return None

# запрос пользователя по логину
async def get_user_by_username(username: str):
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        return user

async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if user and password_verify(password, user.password):
        return user
    return None

# изменение пустого пароля
async def update_user_password(user_id: int, password_hash: str):
    async with async_session_maker() as session:
        try:
            user = await session.get(User, user_id)
            if user:
                user.password = password_hash
                await session.commit()
                return user
            return None
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при обновлении пароля пользователя: {e}")
            return None

async def register_user(username: str, password: str):
    async with async_session_maker() as session:
        user = await get_user_by_username(username)
        if user:
            if not user.password:
                # пользователь найден, но пароль не установлен
                password_new = password_hash(password)
                updated_user = await update_user_password(user.id, password_new)
                return updated_user
            else:
                # пользователь уже зарегистрирован
                print("Пользователь уже зарегистрирован")
                return None
        else:
            # пользователь не найден
            print("Пользователь не найден")
            return None