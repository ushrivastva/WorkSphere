from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/login")
def login (response: Response):
    response.set_cookie(
        key="sesssion_id"
    )
    