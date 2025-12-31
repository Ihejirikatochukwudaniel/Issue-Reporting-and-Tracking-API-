"""
Issue Routes (API Endpoints)

This file defines all the API endpoints (URLs) for issue operations.
Each function handles a specific HTTP method and path.

REST API Design:
- GET /issues → List all issues
- POST /issues → Create new issue
- GET /issues/{id} → Get specific issue
- PUT /issues/{id} → Update entire issue
- PATCH /issues/{id} → Partially update issue
- DELETE /issues/{id} → Delete issue
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Issue, IssueStatus, IssuePriority
from app.schemas import (
    IssueCreate, 
    IssueUpdate, 
    IssueResponse, 
    IssueListResponse,
    MessageResponse
)

# Create a router - like a sub-application for issue-related routes
# prefix="/issues": All routes here start with /issues
# tags=["issues"]: Groups these endpoints in API documentation
router = APIRouter(prefix="/issues", tags=["issues"])


@router.post(
    "/",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new issue"
)
def create_issue(
    issue: IssueCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new issue in the system.
    
    Args:
        issue: Issue data from request body (validated by Pydantic)
        db: Database session (injected by FastAPI via Depends)
    
    Returns:
        The created issue with generated ID and timestamps
    
    Technical Details:
    - Pydantic validates the incoming data automatically
    - SQLAlchemy converts Python object to SQL INSERT
    - db.refresh() reloads the object with auto-generated fields
    - Returns 201 Created status (REST best practice)
    """
    # Convert Pydantic model to SQLAlchemy model
    db_issue = Issue(**issue.model_dump())
    
    # Add to database session (like staging changes)
    db.add(db_issue)
    
    # Commit changes to database (actually save)
    db.commit()
    
    # Refresh to get auto-generated fields (id, timestamps)
    db.refresh(db_issue)
    
    return db_issue


@router.get(
    "/",
    response_model=IssueListResponse,
    summary="List all issues with optional filters"
)
def list_issues(
    status: Optional[IssueStatus] = Query(None, description="Filter by status"),
    priority: Optional[IssuePriority] = Query(None, description="Filter by priority"),
    assignee: Optional[str] = Query(None, description="Filter by assignee"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of issues with optional filtering and pagination.
    
    Query Parameters:
        status: Filter issues by status (optional)
        priority: Filter issues by priority (optional)
        assignee: Filter issues by assignee (optional)
        skip: Pagination offset (default: 0)
        limit: Maximum results (default: 100, max: 100)
    
    Returns:
        List of issues with pagination metadata
    
    Why pagination?
    - Large datasets would be slow without it
    - Better user experience (load data in chunks)
    - Reduces server load and network usage
    
    Technical Details:
    - Query().filter() builds the SQL WHERE clause
    - .count() gets total (for metadata)
    - .offset() and .limit() handle pagination
    """
    # Start with base query
    query = db.query(Issue)
    
    # Apply filters if provided
    if status:
        query = query.filter(Issue.status == status)
    if priority:
        query = query.filter(Issue.priority == priority)
    if assignee:
        query = query.filter(Issue.assignee == assignee)
    
    # Get total count (before pagination)
    total = query.count()
    
    # Apply pagination and get results
    issues = query.offset(skip).limit(limit).all()
    
    return IssueListResponse(
        total=total,
        count=len(issues),
        issues=issues
    )


@router.get(
    "/{issue_id}",
    response_model=IssueResponse,
    summary="Get a specific issue by ID"
)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single issue by its ID.
    
    Args:
        issue_id: The ID of the issue to retrieve (from URL path)
        db: Database session
    
    Returns:
        The requested issue
    
    Raises:
        HTTPException 404: If issue with given ID doesn't exist
    
    Why 404?
    - REST convention: 404 means "resource not found"
    - Distinguishes from 500 (server error)
    - Client knows the ID is invalid
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    return issue


@router.put(
    "/{issue_id}",
    response_model=IssueResponse,
    summary="Fully update an issue"
)
def update_issue(
    issue_id: int,
    issue_update: IssueCreate,  # PUT requires all fields
    db: Session = Depends(get_db)
):
    """
    Fully update an issue (replace all fields).
    
    PUT vs PATCH:
    - PUT: Replace the entire resource (all fields required)
    - PATCH: Update specific fields (partial update)
    
    This is a PUT endpoint, so all fields must be provided.
    Use PATCH endpoint for partial updates.
    
    Args:
        issue_id: ID of issue to update
        issue_update: New complete issue data
        db: Database session
    
    Returns:
        The updated issue
    
    Raises:
        HTTPException 404: If issue doesn't exist
    """
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    # Update all fields
    for field, value in issue_update.model_dump().items():
        setattr(db_issue, field, value)
    
    db.commit()
    db.refresh(db_issue)
    
    return db_issue


@router.patch(
    "/{issue_id}",
    response_model=IssueResponse,
    summary="Partially update an issue"
)
def partial_update_issue(
    issue_id: int,
    issue_update: IssueUpdate,  # PATCH allows optional fields
    db: Session = Depends(get_db)
):
    """
    Partially update an issue (only specified fields).
    
    Only updates fields that are provided in the request.
    Useful when you only want to change status, for example.
    
    Args:
        issue_id: ID of issue to update
        issue_update: Partial issue data (only fields to change)
        db: Database session
    
    Returns:
        The updated issue
    
    Raises:
        HTTPException 404: If issue doesn't exist
    
    Technical Detail:
    - exclude_unset=True: Only include fields that were explicitly set
    - Ignores fields that are None/not provided
    """
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    # Only update fields that were provided (exclude_unset=True)
    update_data = issue_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_issue, field, value)
    
    db.commit()
    db.refresh(db_issue)
    
    return db_issue


@router.delete(
    "/{issue_id}",
    response_model=MessageResponse,
    summary="Delete an issue"
)
def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an issue from the system.
    
    Args:
        issue_id: ID of issue to delete
        db: Database session
    
    Returns:
        Confirmation message
    
    Raises:
        HTTPException 404: If issue doesn't exist
    
    Warning:
    - This is a hard delete (data is permanently removed)
    - Production systems often use "soft delete" (mark as deleted)
    - Consider adding a "deleted" flag instead for audit trails
    """
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id {issue_id} not found"
        )
    
    db.delete(db_issue)
    db.commit()
    
    return MessageResponse(message=f"Issue {issue_id} deleted successfully")