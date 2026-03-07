from uuid import UUID

from fastapi import APIRouter, Depends, Path

from api.schemas.message import MessageCreate, MessagePublic
# from api.dependencies.user import UserController
# from api.dependencies.message import MessageController
from api.services.message import MessageService
from api.services.user import UserService
from api.dependencies import (
    get_user_service,
    get_message_service,
)


router = APIRouter()


@router.get("/{user_id}/messages")
def get_user_messages_route(
        user_service = Depends(get_user_service)
):
    messages = user_service.get_messages()
    return messages


@router.post("/{recipient_id}/messages", response_model=MessagePublic)
def post_user_message_route(
        message_data: MessageCreate,
        recipient_id: UUID = Path(),
        message_service: MessageService = Depends(get_message_service),
        user_service: UserService = Depends(get_user_service),
):
    user_db = user_service.get_user(recipient_id)
    message = message_service.create_message(user_db, message_data)
    return message
