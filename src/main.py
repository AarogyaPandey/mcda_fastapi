from fastapi import FastAPI, HTTPException, status, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM
from src.routes import users, weatherapis, mcda_crud
# from src.crud import mcda_crud
from fastapi.routing import APIRouter

Tortoise.init_models(["src.database.models"], "models")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(weatherapis.router)
app.include_router(mcda_crud.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)

@app.get("/")
def home():
    return "Simple API Service"















# ===========================================================

# app = FastAPI()

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool=True
#     ratings: Optional[int]=None

# my_list = [
#     {"title": "NAXA", "content": "Private company", "id": 1},
#     {"title": "IHRR", "content": "NGO company", "id": 2}
# ]

# @app.get("/post")
# def get_all_posts():
#     return {"data": my_list}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post:Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0, 100000)
#     my_list.append(post_dict)
#     return {"data":post_dict}

# @app.get("/posts/latest")
# def get_latest_post():
#     post=my_list[-1]
#     return {"post_detail": post}

# @app.get("/posts/{id}")
# def get_post_by_id(id:int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
#     return {"post_detail": post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     indx=find_index_post(id)
#     if indx is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
#     my_list.pop(indx)
#     return {"message": f"Post with ID {id} does not exist"}

# @app.put("/posts/{id}")
# def update_post(id: int, post:Post):
#     indx=find_index_post(id)
#     if indx is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
#     post_dict=post.dict()
#     post_dict['id']=id
#     my_list[indx]=post_dict
#     return {"message": f"Post with ID {id} successfully updated"}

# def find_post(id):
#     for post in my_list:
#         if post['id']==id:
#             return post

# def find_index_post(id):
#     for index, post in enumerate(my_list):
#         if post['id']==id:
#             return index

