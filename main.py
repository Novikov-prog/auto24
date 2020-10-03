from fastapi import FastAPI, Response, status
import aiosqlite
from pydantic import BaseModel


app  = FastAPI()

@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect('voitures_5_tables.db')

@app.on_event("shutdown")
async def shutdown():
  await app.db_connection.close()
