from fastapi import FastAPI, UploadFile, Form, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI()


@app.post('/items')
async def create_items(
                  image: UploadFile, 
                  title: Annotated[str, Form()], 
                  price: Annotated[int, Form()], 
                  description: Annotated[str, Form()], 
                  place: Annotated[str, Form()],
                  insertAt: Annotated[int, Form()]
                  ):
    
    image_bytes = await image.read()
    cur.execute("""
                INSERT INTO items(title, image, price, description, place, insertAt)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (title, image_bytes.hex(), price, description, place, insertAt))
    con.commit()
    return JSONResponse(content={"message": "Item created successfully"}, status_code=200)

@app.get("/items")
async def get_items():
    # 컬럼명도 같이 가져옴
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute("""
                       SELECT * FROM items;
                       """).fetchall()
    
    return JSONResponse(jsonable_encoder([dict(row) for row in rows]))

@app.get("/items/{item_id}")
async def get_image(item_id: int):
    cur = con.cursor()
    result = cur.execute("""
                              SELECT image FROM items WHERE id=?;
                              """, (item_id,)).fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    image_bytes = result[0]
    return Response(content=bytes.fromhex(image_bytes), media_type="image")


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")





# from fastapi import FastAPI, UploadFile,Form, Response
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from fastapi.staticfiles import StaticFiles
# from typing import Annotated
# import sqlite3

# con = sqlite3.connect('db.db', check_same_thread=False)
# cur = con.cursor()

# app = FastAPI()


# @app.post('/items')
# async def create_items(
#                   image:UploadFile, 
#                   title:Annotated[str,Form()], 
#                   price:Annotated[int,Form()], 
#                   description:Annotated[str,Form()], 
#                   place:Annotated[str,Form()],
#                   insertAt:Annotated[int,Form()]
#                   ):
    
#     image_bytes = await image.read()
#     cur.execute(f"""
#                 INSERT INTO items(title, image, price, description, place, insertAt)
#                 VALUES ('{title}', '{image_bytes.hex()}', {price},'{description}','{place}', {insertAt} )
#                 """)
#     con.commit()
#     return '200'

# @app.get("/items")
# async def get_items():
#     # 컬럼명도 같이 가져옴
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     rows = cur.execute(f"""
#                        SELECT * FROM items;
#                        """).fetchall()
#     # rows = [[id: 1], [title:'식칼팝니다'], [description:'잘 썰려요'...]]
#     # { id: 1, title: '식칼팝니다', description: '잘 썰려요'... }
    
#     return JSONResponse(jsonable_encoder(dict(row) for row in rows))

# @app.get("/items/{item_id}")
# async def get_image(item_id):
#     cur = con.cursor()
#     #16진법
#     image_bytes = cur.execute(f"""
#                               SELECT image from items WHERE id={item_id}
#                               """).fetchone()[0]
#     return Response(content=bytes.fromhex(ima))


# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


