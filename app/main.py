from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.dependecy import get_broker_consumer
from app.tasks.handlers import router as tasks_router
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    broker_consumer = await get_broker_consumer()
    await broker_consumer.consume_callback_message()
    yield




app = FastAPI(lifespan=lifespan)


app.include_router(tasks_router)
app.include_router(user_router)
app.include_router(auth_router)
