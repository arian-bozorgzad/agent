from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def uid() -> str:
    return str(uuid4())


def now() -> str:
    return datetime.now(UTC).isoformat()


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    title: Mapped[str] = mapped_column(String(100), default="New conversation")
    created_at: Mapped[str] = mapped_column(default=now)


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"), index=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    run_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    sources: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    created_at: Mapped[str] = mapped_column(default=now)


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    title: Mapped[str] = mapped_column(String(160))
    content: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(default=now)
    updated_at: Mapped[str] = mapped_column(default=now)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    title: Mapped[str] = mapped_column(String(240))
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(default=now)


class Timer(Base):
    __tablename__ = "timers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    label: Mapped[str] = mapped_column(String(100))
    ends_at: Mapped[str]
    cancelled: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(default=now)


class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(400), default="")
    steps: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    created_at: Mapped[str] = mapped_column(default=now)


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    conversation_id: Mapped[str | None] = mapped_column(
        ForeignKey("conversations.id"), nullable=True, index=True
    )
    kind: Mapped[str] = mapped_column(String(20), default="chat")
    label: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(30), default="running", index=True)
    plan: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    result: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[str] = mapped_column(default=now)
    updated_at: Mapped[str] = mapped_column(default=now)


class Event(Base):
    __tablename__ = "events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), index=True)
    kind: Mapped[str] = mapped_column(String(30))
    label: Mapped[str] = mapped_column(String(300))
    detail: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(default=now)


class Preference(Base):
    __tablename__ = "preferences"
    id: Mapped[str] = mapped_column(String(20), primary_key=True, default="default")
    display_name: Mapped[str] = mapped_column(String(60), default="")
    instructions: Mapped[str] = mapped_column(String(2000), default="")
