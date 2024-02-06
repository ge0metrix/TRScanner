from fastapi import FastAPI, Depends, Form, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
import sqlalchemy.orm as _orm
from schemas import *
import controllers
from typing import List
import json

app = FastAPI()

controllers.create_database()


@app.get("/")
def root():
    response = RedirectResponse(url="/docs")
    return response


@app.get("/api/calls/", response_model=List[CallOut])
def get_calls(
    skip: int | None = None,
    limit: int | None = None,
    db: _orm.Session = Depends(controllers.get_db),
):
    if limit:
        return controllers.get_calls(db=db).offset(skip).limit(limit)
    return controllers.get_calls(db=db).offset(skip).all()


@app.get("/api/calls/{call_id}", response_model=CallOut)
def get_call(call_id: int, db: _orm.Session = Depends(controllers.get_db)):
    call = controllers.get_call(db=db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call Not Found")
    return call


"""
@app.post("/calls/")
def post_call(call: CallIn, db: _orm.Session = Depends(controllers.get_db)):
    return controllers.post_call_to_db(db=db, call=call)
"""


@app.post("/api/calls/", response_model=CallOut)
def uploadcall(
    file: UploadFile,
    calldata: Annotated[str, Form(description="Json Call Data")],
    db: _orm.Session = Depends(controllers.get_db),
):
    call = CallIn(**json.loads(calldata))
    print(file.size)
    return controllers.post_call_to_db(db=db, call=call)
