from backend.database import Base
from backend.models.content import Content
from backend.models.event import EVENT_WEIGHTS, Event
from backend.models.user import User

# Importing every model here means Alembic's target_metadata (Base.metadata)
# discovers all tables from a single `from backend.models import *`.
__all__ = ["Base", "User", "Content", "Event", "EVENT_WEIGHTS"]
