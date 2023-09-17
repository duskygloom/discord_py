import secret, discord, logging
import pink_bot.bot as bot

discord.utils.setup_logging()

if __name__ == "__main__":
    try:
        bot.bot.run(secret.bot_token)
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
