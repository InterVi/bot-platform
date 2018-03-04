from core.interpreter import *
from core.bot import *
from core.file_transfers.file_transfers_handler import *


def interpreter_default_factory(bot):
    return Interpreter(bot)


def bot_default_factory(tox, settings, profile_manager, permission_checker):
    return Bot(tox, settings, profile_manager, permission_checker)


def file_transfer_handler_default_factory(tox, permission_checker):
    return FileTransfersHandler(tox, permission_checker)