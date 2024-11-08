from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from random import randrange
from app.dbconfig import database, connect_db, disconnect_db


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # Optional field default value provided as none


@app.on_event("startup")
async def startup():
    
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
   
    await disconnect_db()

@app.get("/health")
async def health_check():
    try:
        
        result = await database.fetch_one("SELECT 1")
        if result:
            return {"status": "healthy", "message": "Database connection is active"}
        else:
            raise HTTPException(status_code=500, detail="Database query failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database not connected: {e}")


@app.get('/')
def root():
    return {'message': 'Hello World!'}

@app.get('/posts')
async def get_posts():
    query = "SELECT * FROM posts"
    my_posts = await database.fetch_all(query)
    if my_posts:
        my_posts = [dict(row) for row in my_posts]
        print(my_posts)
        return {"data":my_posts}

@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1, 1000000)  # Assigning random ID for each post
    my_posts.append(post_dict)
    return {"data": post_dict}

def find_post(id):
    
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.get('/posts/{id}')
def get_post(id: int):
 
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": post}
        

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    # deleting a post
    # find the index in the array that has required ID
    # my_post
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    # remove the post from the array
    my_posts.pop(index)
    return {"message": f"Post with id {id} deleted successfully"}
    
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict} 