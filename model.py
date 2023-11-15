from dataclasses import dataclass


@dataclass(frozen=True)
class EmailContent:
    from_email: str
    body: str
    subject: str
    to_email: str
