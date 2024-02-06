import pydantic as _pd
from typing import List, Optional, Annotated
import datetime
from database_models import *


class SrcIn(_pd.BaseModel):
    src: int
    time: datetime.datetime
    pos: float
    emergency: bool
    signal_system: str
    tag: str

    class Meta:
        orm_model = Src

    class Config:
        from_attributes = True


class SrcOut(SrcIn):
    id: int


class FreqIn(_pd.BaseModel):
    freq: int
    time: datetime.datetime
    pos: float
    len: float
    error_count: int
    spike_count: int

    class Meta:
        orm_model = Freq

    class Config:
        from_attributes = True


class FreqOut(FreqIn):
    id: int


class CallIn(_pd.BaseModel):
    freq: int
    start_time: datetime.datetime
    stop_time: datetime.datetime
    emergency: bool
    priority: int
    mode: int
    duplex: bool
    encrypted: bool
    call_length: float
    talkgroup: int
    talkgroup_tag: str
    talkgroup_description: str
    talkgroup_group: str
    talkgroup_group_tag: str
    audio_type: str
    short_name: str
    freqList: List[FreqIn]
    srcList: List[SrcIn]

    class Meta:
        orm_model = Call
    class Config:
        from_attributes = True


class CallOut(CallIn):
    id: int
    srcList: Optional[List[SrcOut]]
    freqList: Optional[List[FreqOut]]


"""
{
"freq": 471325000,
"start_time": 1707161525,
"stop_time": 1707161532,
"emergency": 0,
"priority": 0,
"mode": 0,
"duplex": 0,
"encrypted": 0,
"call_length": 5,
"talkgroup": 2,
"talkgroup_tag": "Westford Fire",
"talkgroup_description": "",
"talkgroup_group_tag": "",
"talkgroup_group": "",
"audio_type": "analog",
"short_name": "Westford",
"freqList": [ {"freq": 471325000, "time": 1707161525, "pos": 0.00, "len": 5.26, "error_count": "0", "spike_count": "0"} ],
"srcList": [ {"src": 9914, "time": 1707161525, "pos": 0.00, "emergency": 0, "signal_system": "", "tag": ""} ]
}

"""
