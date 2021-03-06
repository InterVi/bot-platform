from core.file_transfers.file_transfers import *
from core.util import get_avatar_path
from wrapper.toxcore_enums_and_consts import *
from core.file_transfers.file_transfer_thread import start, stop


class FileTransfersHandler:

    SETTINGS_FILE_NAME = 'settings.json'

    AVATAR_FILE_NAME = 'avatar.png'

    def __init__(self, tox, permission_checker):
        self._tox = tox
        self._permission_checker = permission_checker
        self._file_transfers = {}  # dict of file transfers. key - tuple (friend_number, file_number)
        start()

    def __del__(self):
        stop()

    def send_avatar(self, friend_number):
        avatar_path = get_avatar_path()
        sa = SendAvatar(avatar_path, self._tox, friend_number)
        self._file_transfers[(friend_number, sa.get_file_number())] = sa

    def cancel_transfer(self, friend_number, file_number):
        control = TOX_FILE_CONTROL['CANCEL']
        self._tox.file_control(friend_number, file_number, control)
        self.remove_transfer(friend_number, file_number)

    def process_incoming_transfer(self, friend_number, file_number, file_name, file_size):
        if not self._permission_checker.check_permissions(['admin'], friend_number):
            self.cancel_transfer(friend_number, file_number)
        elif file_name == FileTransfersHandler.SETTINGS_FILE_NAME:
            self.accept_transfer(friend_number, file_number, get_avatar_path(), file_size)
        elif file_name == FileTransfersHandler.AVATAR_FILE_NAME:
            pass
        else:
            self.cancel_transfer(friend_number, file_number)

    def accept_transfer(self, friend_number, file_number, file_path, file_size):
        rt = ReceiveTransfer(file_path, self._tox, friend_number, file_size, file_number)
        self._file_transfers[(friend_number, file_number)] = rt
        self._tox.file_control(friend_number, file_number, TOX_FILE_CONTROL['RESUME'])

    def remove_transfer(self, friend_number, file_number):
        if (friend_number, file_number) in self._file_transfers:
            del self._file_transfers[(friend_number, file_number)]

    def transfer_cancelled(self, friend_number, file_number):
        """
        Stop transfer
        :param friend_number: number of friend
        :param file_number: file number
        """
        self.remove_transfer(friend_number, file_number)

    def pause_transfer(self, friend_number, file_number, by_friend=False):
        """
        Pause transfer with specified data
        """
        tr = self._file_transfers[(friend_number, file_number)]
        tr.pause(by_friend)

    def resume_transfer(self, friend_number, file_number, by_friend=False):
        """
        Resume transfer with specified data
        """
        tr = self._file_transfers[(friend_number, file_number)]
        if not by_friend:
            tr.send_control(TOX_FILE_CONTROL['RESUME'])

    def incoming_chunk(self, friend_number, file_number, position, data):
        """
        Incoming chunk
        """
        if (friend_number, file_number) in self._file_transfers:
            transfer = self._file_transfers[(friend_number, file_number)]
            transfer.write_chunk(position, data)

    def outgoing_chunk(self, friend_number, file_number, position, size):
        """
        Outgoing chunk
        """
        if (friend_number, file_number) in self._file_transfers:
            transfer = self._file_transfers[(friend_number, file_number)]
            transfer.send_chunk(position, size)
