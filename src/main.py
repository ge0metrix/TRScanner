import json
from typing import List, Optional, Annotated

import sqlalchemy.orm as _orm
from fastapi import (
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Request,
    UploadFile,
    BackgroundTasks,
)
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

import controllers
from schemas import *

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


@app.post("/api/calls/", response_model=CallOut)
def uploadcall(
    file: UploadFile,
    calldata: Annotated[str, Form()],
    db: _orm.Session = Depends(controllers.get_db),
):
    try:
        call = CallIn(**json.loads(calldata))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500)
    print(file.size)
    return controllers.post_call_to_db(db=db, call=call)


# TODO: Abstract this out to a model and do it better!
@app.post("/api/calls/trunkrecorderupload/")
def uploadTRcall(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    system: str = Form(),
    systemLabel: str = Form(),
    dateTime: datetime.datetime = Form(),
    frequency: int = Form(),
    key: str = Form(),
    talkgroup: int = Form(),
    patches: List[int] | None = Form(None),
    talkgroupGroup: str | None = Form(None),
    talkgroupLabel: str | None = Form(None),
    talkgroupTag: str | None = Form(None),
    talkgroupName: str | None = Form(None),
    sources: List[str] | None = Form(None),
    frequencies: List[str] | None = Form(None),
    db: _orm.Session = Depends(controllers.get_db),
):
    filedata = file.file.read()
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No FileName provided!")
    
    background_tasks.add_task(
        WriteFileToDisk, filename=file.filename, filedata=filedata
    )


def WriteFileToDisk(filename: str, filedata: bytes) -> None:
    print(f"Writing {filename}")
    with open(filename, "bw") as file:
        file.write(filedata)
