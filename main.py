from fastapi import FastAPI, UploadFile, Form, Response, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGERNOT NULL
            );
            """)

app = FastAPI()

SECRIT = "super-coding"
manager = LoginManager(SECRIT, '/login')

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'''id="{data}"'''
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str, Form()], 
        password:Annotated[str, Form()]):
    user = query_user(id)
    
    if not user :
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
        'sub' : {
            'id' : user['id'],
            'name': user['name'],
            'email': user['email']
        }
    })
    
    return { 'access_token':access_token}
    


@app.post("/signup")
def signup(id:Annotated[str, Form()], 
        password:Annotated[str, Form()],
        name:Annotated[str, Form()],
        email:Annotated[str, Form()]):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    return '200'


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
async def get_items(user=Depends(manager)):
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
    return Response(content=bytes.fromhex(image_bytes), media_type="image/*")



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


