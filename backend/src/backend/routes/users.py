from uuid import UUID

from fastapi import APIRouter, Depends, Path, HTTPException

from backend.schemas.message import MessageCreate, MessagePublic
from backend.schemas.user import UserPublic, UserCreate
# from backend.dependencies.user import UserController
# from backend.dependencies.message import MessageController
from backend.services.message import MessageService
from backend.services.user import UserService
from backend.dependencies import (
    get_user_service,
    get_message_service,
    get_current_user,
)


router = APIRouter()


@router.post("", status_code=201, response_model=UserPublic)
def register_user_route(
        user_data: UserCreate,
        user_service: UserService = Depends(get_user_service),
):
    user_db = user_service.create_user(user_data)
    return UserPublic.model_validate(user_db, from_attributes=True)


@router.get("/me/messages")
def get_user_messages_route(
        message_service: MessageService = Depends(get_message_service),
        current_user: UserPublic = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service),
):
    user_db = user_service.get_user(public_id=current_user.id)
    messages = message_service.get_messages(user_db)
    return messages


@router.post("/{recipient_id}/messages", response_model=MessagePublic)
def post_user_message_route(
        message_data: MessageCreate,
        recipient_id: UUID = Path(),
        current_user: UserPublic = Depends(get_current_user),
        message_service: MessageService = Depends(get_message_service),
        user_service: UserService = Depends(get_user_service),
):
    if current_user.id == recipient_id:
        raise HTTPException(status_code=400, detail="Cannot send message to self.")
    user_db = user_service.get_user(public_id=recipient_id)
    message = message_service.create_message(user_db, message_data)
    return message
