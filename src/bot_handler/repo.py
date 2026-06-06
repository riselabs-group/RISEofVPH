from deltachat2 import MsgData, events
from deltabot_cli import BotCli


def send_msg(bot, accid, chat_id, *messages):
    for msg in messages:
        bot.rpc.send_msg(accid, chat_id, MsgData(text=msg))
