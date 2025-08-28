# app/entities/__init__.py
from .user import User
from .communities import Communities  
from .moderator import Moderator
from .post import Post  # if you have this
from .comments import Comments  # if you have this
from .votes import Votes  # if you have this
from .subscription import Subscription  # if you have this

# Make sure all models are available
__all__ = [
    "User",
    "Communities", 
    "Moderator",
    "Post",
    "Comments", 
    "Votes",
    "Subscription"
]