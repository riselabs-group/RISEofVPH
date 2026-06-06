from deltachat2 import MsgData, events
from deltabot_cli import BotCli
cli = BotCli("echobot")


@cli.on(events.RawEvent)
def log_event(bot, accid, event):
    bot.logger.info(event)




if __name__ == "__main__":
    cli.start()
