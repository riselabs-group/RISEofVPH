from deltachat2 import MsgData, events
from deltabot_cli import BotCli
from bot_handler.repo import send_msg
from utils.repo import FIXED_RESPONSES

cli = BotCli("echobot")


@cli.on(events.RawEvent)
def log_event(bot, accid, event):
    bot.logger.info(event)


@cli.on(events.NewMessage(command="/start"))
def _start(bot, accid, event):
    send_msg(bot, accid, event.msg.chat_id, FIXED_RESPONSES["/start"])


if __name__ == "__main__":
    cli.start()
