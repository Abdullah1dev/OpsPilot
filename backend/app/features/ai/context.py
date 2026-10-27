from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.features.auth.models import User


@dataclass
class AIToolContext:
    db: Session
    current_user: User