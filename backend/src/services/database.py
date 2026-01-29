import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlmodel import Session, select, func
from typing import List, Optional
from models import Task as ExistingTask, TaskCreate, TaskUpdate  # Import only Task models from root models.py
# Import Conversation and Message from the src models directory
from ..models import Conversation, Message, ConversationBase, MessageBase

class ConversationCreate(ConversationBase):
    pass

class MessageCreate(MessageBase):
    pass


def create_conversation(db_session: Session, conversation_data: ConversationCreate) -> Conversation:
    """Create a new conversation in the database."""
    conversation = Conversation.model_validate(conversation_data)
    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)
    return conversation


def get_conversations_by_user(db_session: Session, user_id: str) -> List[Conversation]:
    """Get all conversations for a specific user."""
    statement = select(Conversation).where(Conversation.user_id == user_id)
    results = db_session.exec(statement)
    return results.all()


def get_conversation_by_id(db_session: Session, conversation_id: str) -> Optional[Conversation]:
    """Get a conversation by its ID."""
    statement = select(Conversation).where(Conversation.id == conversation_id)
    result = db_session.exec(statement).first()
    return result


def create_message(db_session: Session, message_data: MessageCreate) -> Message:
    """Create a new message in the database."""
    message = Message.model_validate(message_data)
    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)
    return message


def get_messages_by_conversation(db_session: Session, conversation_id: str) -> List[Message]:
    """Get all messages for a specific conversation."""
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
    results = db_session.exec(statement)
    return results.all()


def get_task_by_id(db_session: Session, task_id: int) -> Optional[ExistingTask]:
    """Get a task by its ID."""
    statement = select(ExistingTask).where(ExistingTask.id == task_id)
    result = db_session.exec(statement).first()
    return result


def get_tasks_by_user(db_session: Session, user_id: str) -> List[ExistingTask]:
    """Get all tasks for a specific user."""
    statement = select(ExistingTask).where(ExistingTask.user_id == user_id)
    results = db_session.exec(statement)
    return results.all()


def create_task(db_session: Session, task_data: TaskCreate, user_id: str) -> ExistingTask:
    """Create a new task for a user."""
    task_dict = task_data.model_dump()
    task_dict['user_id'] = user_id
    task = ExistingTask(**task_dict)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def update_task(db_session: Session, task_id: int, task_update: TaskUpdate) -> Optional[ExistingTask]:
    """Update an existing task."""
    task = db_session.get(ExistingTask, task_id)
    if not task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def delete_task(db_session: Session, task_id: int) -> bool:
    """Delete a task."""
    task = db_session.get(ExistingTask, task_id)
    if not task:
        return False

    db_session.delete(task)
    db_session.commit()
    return True


def complete_task(db_session: Session, task_id: int, completed: bool) -> Optional[ExistingTask]:
    """Mark a task as completed or not."""
    task = db_session.get(ExistingTask, task_id)
    if not task:
        return None

    task.completed = completed
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task