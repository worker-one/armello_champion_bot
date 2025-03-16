import logging
from pathlib import Path

from omegaconf import OmegaConf
from telebot import TeleBot, types
from telebot.states import State, StatesGroup

from ..database.core import get_session
from ..match.models import Player
from .service import CLAN_CATEGORIES, get_available_titles, update_title
from ..common.service import start_timeout

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load configuration
CURRENT_DIR = Path(__file__).parent
config = OmegaConf.load(CURRENT_DIR / "config.yaml")
strings = config.strings

# Define States
class TitleState(StatesGroup):
    """Title states"""
    select_title = State()
    enter_title = State()


def register_handlers(bot: TeleBot):
    """Register title handlers"""
    logger.info("Registering title handlers")

    @bot.message_handler(commands=["title"])
    def title_command(message: types.Message, data: dict):
        """Handle /title command - start title selection process"""
        user = data["user"]
        with get_session() as session:
            # Check if user has a player profile
            player = session.query(Player).filter(Player.user_id == user.id).first()
            if not player:
                bot.reply_to(message, "У вас нет профиля игрока. Сначала зарегистрируйтесь.")
                return

            # Check if user is channel owner
            is_channel_owner = user.role_id in {0, 1}

            # Get titles available for this player
            available_titles = get_available_titles(session, player.id, is_channel_owner)

            if not available_titles:
                bot.reply_to(message, "Вы не занимаете первое место ни в одном из рейтингов. "
                                     "Вы не можете изменить титулы.")
                return

            # Create keyboard with available titles
            markup = types.InlineKeyboardMarkup(row_width=1)
            for category, display_name in available_titles:
                markup.add(types.InlineKeyboardButton(
                    display_name,
                    callback_data=f"title_select:{category}"
                ))

            bot.send_message(message.chat.id, strings[user.lang].title_prompt, reply_markup=markup)
            data["state"].set(TitleState.select_title)
            start_timeout(bot, message.chat.id, message.message_id)


    @bot.callback_query_handler(func=lambda call: call.data.startswith("title_select:"), state=TitleState.select_title)
    def title_selected(call: types.CallbackQuery, data: dict):
        """Handle title category selection"""
        # Extract the category from callback data
        category = call.data.split(":")[1]
        user = data["user"]

        # Store selected category in user data for next step
        data["state"].add_data(title_category=category)

        # Determine display name for category
        if category == "overall":
            display_name = "Лучший игрок комьюнити"
        else:
            display_name = CLAN_CATEGORIES.get(category, category.capitalize())

        # Ask user for new title
        bot.edit_message_text(
            text=strings[user.lang].enter_title,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

        # Move to next state
        data["state"].set(TitleState.enter_title)


    @bot.message_handler(state=TitleState.enter_title)
    def save_title(message: types.Message, data: dict):
        """Save the new title"""
        user = data["user"]
        with data["state"].data() as state_data:
            category = state_data["title_category"]
        new_title = message.text.strip()

        # Check title length
        if len(new_title) > 50:  # Set a reasonable limit
            bot.reply_to(message, strings[user.lang].title_too_long)
            return

        with get_session() as session:
            update_title(session, category, new_title)

        bot.reply_to(message, strings[user.lang].title_updated)
        # Clear state
        data["state"].delete()
