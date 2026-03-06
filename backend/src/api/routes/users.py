from fastapi import APIRouter, Depends, Path

from api.schemas.message import MessageCreate, MessagePublic
from api.dependencies.user import UserController
from api.dependencies.message import MessageController


router = APIRouter()


@router.get("/{user_id}/messages")
def get_user_messages_route(
        user_controller: UserController = Depends()
):
    messages = user_controller.get_messages()
    return messages


@router.post("/{recipient_id}/messages", response_model=MessagePublic)
def post_user_message_route(
        message_data: MessageCreate,
        recipient_id: str = Path(),
        message_controller: MessageController = Depends()
):
    message = message_controller.add_message(recipient_id, message_data)
    return message
