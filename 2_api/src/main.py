from fastapi import FastAPI
import uvicorn
from routers import router_list

app = FastAPI()
for router in router_list:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", reload=True)
