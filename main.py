from fastapi import FastAPI, Response, status
import aiosqlite
from pydantic import BaseModel


app  = FastAPI()

@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect('.db')

@app.on_event("shutdown")
async def shutdown():
  await app.db_connection.close()

@app.get("/marques")
async def get_marques(page: int = 0, per_page: int = 10):
  app.db_connection.row_factory = aiosqlite.Row
  cursor = await app.db_connection.execute("SELECT * FROM file1 ORDER BY annonce_id LIMIT :per_page OFFSET :per_page*:page",
      {'page': page, 'per_page': per_page})
      marques = await cursor.fetchall()
      return marques    