from fastapi import FastAPI

from api.admin import setup_admin

from api.routers.user import router as user_router
from api.routers.log_group import router as log_group_router
from api.routers.log_level import router as log_level_router
from api.routers.log_item import router as log_item_router


app = FastAPI()
setup_admin(app)

app.include_router(user_router)
app.include_router(log_group_router)
app.include_router(log_level_router)
app.include_router(log_item_router)

all = [
    app
]
