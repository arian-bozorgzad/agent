from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class NoteInput(StrictModel):
    title: str = Field(min_length=1, max_length=160)
    content: str = Field(default="", max_length=20000)


class TaskInput(StrictModel):
    title: str = Field(min_length=1, max_length=240)


class TaskPatch(StrictModel):
    completed: bool


class TimerInput(StrictModel):
    label: str = Field(default="Focus session", min_length=1, max_length=100)
    minutes: int = Field(ge=1, le=180)


class LinkInput(StrictModel):
    url: HttpUrl
    label: str = Field(min_length=1, max_length=100)

    @field_validator("url")
    @classmethod
    def https_only(cls, value):
        if value.scheme not in {"https", "http"}:
            raise ValueError("Only HTTP(S) links are allowed")
        return value


class IdInput(StrictModel):
    id: UUID


class QueryInput(StrictModel):
    query: str = Field(default="", max_length=200)


class EmptyInput(StrictModel):
    pass


class Step(StrictModel):
    tool: Literal["create_note", "add_task", "start_timer", "open_link"]
    arguments: dict[str, Any]


class WorkflowInput(StrictModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=400)
    steps: list[Step] = Field(min_length=1, max_length=8)


class PreferencesInput(StrictModel):
    display_name: str = Field(default="", max_length=60)
    instructions: str = Field(default="", max_length=2000)


class ChatInput(StrictModel):
    type: Literal["send"]
    conversation_id: UUID
    request_id: UUID
    text: str = Field(min_length=1, max_length=8000)


class RunRequest(StrictModel):
    request_id: UUID


class ActionPlan(StrictModel):
    steps: list[Step] = Field(min_length=1, max_length=8)
