from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.database import Base


class IssueStatus(str, enum.Enum):
    """
    Enumeration for issue statuses.
    
    Why use Enum?
    - Restricts values to predefined options (prevents typos)
    - Self-documenting code
    - Database-level constraint ensures data integrity
    """
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IssuePriority(str, enum.Enum):
    """
    Enumeration for issue priorities.
    
    Helps categorize issues by urgency.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Issue(Base):
    """
    Issue Model - Represents the 'issues' table in our database.
    
    Each attribute becomes a column in the database table.
    SQLAlchemy handles the translation between Python objects and SQL.
    """
    
    __tablename__ = "issues"  # Name of the table in the database
    
    # Primary Key: Unique identifier for each issue
    # autoincrement=True: Database automatically generates sequential IDs
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Title: Short description of the issue
    # index=True: Creates a database index for faster searches
    # nullable=False: This field is required (cannot be empty)
    title = Column(String(200), index=True, nullable=False)
    
    # Description: Detailed explanation of the issue
    # Text type allows longer content than String
    description = Column(Text, nullable=True)
    
    # Status: Current state of the issue
    # Enum ensures only valid status values can be stored
    # default: New issues start as "open"
    status = Column(
        Enum(IssueStatus), 
        default=IssueStatus.OPEN, 
        nullable=False
    )
    
    # Priority: Importance level of the issue
    priority = Column(
        Enum(IssuePriority), 
        default=IssuePriority.MEDIUM, 
        nullable=False
    )
    
    # Reporter: Email or name of person who reported the issue
    reporter = Column(String(100), nullable=False)
    
    # Assignee: Person assigned to fix the issue (optional)
    assignee = Column(String(100), nullable=True)
    
    # Timestamps: Track when issues are created and updated
    # func.now(): SQLAlchemy function that gets current time from database
    # server_default: Database sets this automatically on insert
    # onupdate: Database updates this automatically on any change
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        """
        String representation of the Issue object.
        Useful for debugging - shows the issue when you print it.
        """
        return f"<Issue(id={self.id}, title='{self.title}', status='{self.status}')>"