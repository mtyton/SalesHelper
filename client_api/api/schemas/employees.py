from dataclasses import dataclass


@dataclass
class SingleEmployeeResponse:
    name: str
    surname : str
    position: str

    is_busy: bool
    resume_id: int
    category: str


@dataclass
class Resume:
    owner_id: int
    content: str
