from fastapi import FastAPI

app = FastAPI()

@app.get("/blog") # /blog?limit=10&published=true
def index(limit=10, published:bool = True):
  if published:
    return {"data": f"{limit} published"}
  else:
    return {"data": f"{limit} can not published"}

@app.get("/blog/unpublished")
def unpublished():
  return {"data": "all unpublished blogs"}

@app.get("/blog/{id}")
def show(id: int):
  return {"data": id}


@app.get("blog/{id}/comments")
def comments(id):
  return {"data": {"1", "2"}}