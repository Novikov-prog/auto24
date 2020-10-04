from fastapi import FastAPI, Response, status
import aiosqlite
from pydantic import BaseModel


app  = FastAPI()

@app.on_event("startup")
async def startup():
    app.db_connection = await aiosqlite.connect('marques.db')

@app.on_event("shutdown")
async def shutdown():
  await app.db_connection.close()

@app.get("/marques")
async def get_marques(page: int = 0, per_page: int = 10):
  app.db_connection.row_factory = aiosqlite.Row
  cursor = await app.db_connection.execute("SELECT * FROM table1 ORDER BY annonce_id LIMIT :per_page OFFSET :per_page*:page",
      {'page': page, 'per_page': per_page})
      marques = await cursor.fetchall()
      return marques

@app.get("/marques/model")
async def get_model_by_marque(response: Response, model_name: str):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await app.db_connection.execute("SELECT Make FROM table1 WHERE Model = :model_name ORDER BY Name",
        {'model_name': model_name})
    marques = await cursor.fetchall()

    if len(marques) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":{"error":"Pas de modelès de cette marque."}}
    return marques    