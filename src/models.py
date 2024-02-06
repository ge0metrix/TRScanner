import database as _db
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.types import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import List
from datetime import datetime as _dt

class Call(_db.Base):
    __tablename__ = 'calls'
    id = Column(Integer, primary_key=True, index=True)
    freq = Column(Integer, nullable=False)
    start_time = Column(DateTime, index=True, default=_dt.now)
    stop_time = Column(DateTime)
    emergency = Column(Boolean)
    priority = Column(Integer)
    mode = Column(Integer)
    duplex = Column(Boolean)
    encrypted = Column(Boolean)
    call_length = Column(Numeric)
    talkgroup = Column(Integer)
    talkgroup_tag = Column(String(255))
    talkgroup_description = Column(String(255))
    talkgroup_group = Column(String(255))
    talkgroup_group_tag = Column(String(255))
    audio_type = Column(String(255))
    short_name = Column(String(255))
    srcList = relationship("Src")
    freqList = relationship("Freq")

class Src(_db.Base):
    __tablename__ = 'call_sources'
    id = Column(Integer, primary_key=True, index=True)
    src = Column(Integer)
    time = Column(DateTime)
    pos = Column(Numeric)
    emergency = Column(Boolean)
    signal_system = Column(String(255))
    tag = Column(String(255))
    call_id = Column(Integer, ForeignKey("calls.id"))

class Freq(_db.Base):
    __tablename__ = "call_freqs"
    id = Column(Integer, primary_key=True, index=True)
    freq = Column(Integer)
    time = Column(DateTime)
    pos = Column(Numeric)
    len = Column(Numeric)
    error_count = Column(Integer)
    spike_count = Column(Integer)
    call_id = Column(Integer, ForeignKey("calls.id"))