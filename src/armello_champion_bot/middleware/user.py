import logging

from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware, CancelUpdate
from telebot.states.sync.context import StateContext
from telebot.types import CallbackQuery, Message

from ..auth.service import upsert_user
from ..database.core import db_session
from .service import create_event

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserMessageMiddleware(BaseMiddleware):
    """Middleware to log user messages"""

    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
        self.update_types = ["message"]

    def pre_process(self, message: Message, data: dict):
        """Pre-process the message"""

         
        user = upsert_user(
            db_session,
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

        # Check if user is blocked
        if user.is_blocked:
            self.bot.send_message(user.id, "You have been blocked from using this bot.")
            self.bot.answer_callback_query(message.id, "You have been blocked from using this bot.")
            return

        event = create_event(
            db_session, user_id=user.id, chat_id=message.chat.id,
            content=message.text, content_type=message.content_type,
            event_type="message", state=data["state"].get()
        )

        # Log event to the console
        # print(f"message.is_topic_message: {message.is_topic_message} message.message_thread_id not in ... {message.message_thread_id}"), 
        # if message.is_topic_message and message.message_thread_id not in {13183, 13186}:
        #     return CancelUpdate()
        logger.info(event.dict())

        # Set the user data to the data dictionary
        data["user"] = user

    def post_process(self, message, data, exception):
        pass


class UserCallbackMiddleware(BaseMiddleware):
    """Middleware to log user callbacks"""

    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
        self.update_types = ["callback_query"]

    def pre_process(self, callback_query: CallbackQuery, data: dict):
        """Pre-process the callback query"""
         
        user = upsert_user(
            db_session,
            id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            first_name=callback_query.from_user.first_name,
            last_name=callback_query.from_user.last_name,
        )

        # Check if user is blocked
        if user.is_blocked:
            self.bot.send_message(user.id, "You have been blocked from using this bot.")
            self.bot.answer_callback_query(callback_query.id, "You have been blocked from using this bot.")
            return

        event = create_event(
            db_session, user_id=user.id, chat_id=callback_query.message.chat.id,
            content=callback_query.data, content_type="callback_data", event_type="callback",
            state=data["state"].get()
        )

        # Log event to the console
        logger.info(event.dict())

        # Set the user data to the data dictionary
        data["user"] = user

    def post_process(self, callback_query, data, exception):
        pass
