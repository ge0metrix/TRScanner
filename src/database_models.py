from datetime import datetime as _dt
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

import database as _db


class Call(_db.Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True, index=True)
    freq = Column(Integer, nullable=False)
    start_time = Column(DateTime, index=True, default=_dt.now)
    stop_time = Column(DateTime, nullable=True)
    emergency = Column(Boolean, nullable=True)
    priority = Column(Integer, nullable=True)
    mode = Column(Integer, nullable=True)
    duplex = Column(Boolean, nullable=True)
    encrypted = Column(Boolean, nullable=True)
    call_length = Column(Numeric, nullable=True)
    talkgroup = Column(Integer)
    talkgroup_tag = Column(String(255), nullable=True)
    talkgroup_description = Column(String(255), nullable=True)
    talkgroup_group = Column(String(255), nullable=True)
    talkgroup_group_tag = Column(String(255), nullable=True)
    audio_type = Column(String(255), nullable=True)
    short_name = Column(String(255))
    srcList = relationship("Src")
    freqList = relationship("Freq")


class Src(_db.Base):
    __tablename__ = "call_sources"
    id = Column(Integer, primary_key=True, index=True)
    src = Column(Integer)
    time = Column(DateTime, nullable=True)
    pos = Column(Numeric, nullable=True)
    emergency = Column(Boolean, nullable=True)
    signal_system = Column(String(255), nullable=True)
    tag = Column(String(255), nullable=True)
    call_id = Column(Integer, ForeignKey("calls.id"))


class Freq(_db.Base):
    __tablename__ = "call_freqs"
    id = Column(Integer, primary_key=True, index=True)
    freq = Column(Integer)
    time = Column(DateTime, nullable=True)
    pos = Column(Numeric, nullable=True)
    len = Column(Numeric, nullable=True)
    error_count = Column(Integer, nullable=True)
    spike_count = Column(Integer, nullable=True)
    call_id = Column(Integer, ForeignKey("calls.id"))
