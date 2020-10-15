from twisted.internet.protocol import Protocol

class RawBoardDataReceived(Protocol):
    def __init__(self, client):
        self.__client = client
        self.__reset_state()

    def dataReceived(self, data):
        print('Got %d bytes:[%s]' % (len(data), data))
        header_len = 3
        if self.__state == 0:
            self.__header += data
        if self.__state == 0:
            if len(self.__header) >= header_len:
                self.__state = 1
                self.__message = ()
                data = self.__header[3:]
                self.__header = self.__header[0:3]
                try:
                    header = struct.unpack('>BBB', self.__header)
                except struct.error:
                    logging.warning('timeout in header reading')
                self.__message_id = self.__header[0]
                self.__message_length = (self.__header[1] << 7) + self.__header[2] - header_len
        if self.__state == 1:
            for byte in data:
                try:
                    datum = struct.unpack('>B', byte)
                    if datum[0] & 0x80:
                        logging.warning('illegal data in message 0x%x found', self.__message_id)
                        logging.warning('ignore collected message data %s', self.__message)
                        self.__reset_state()
                    else:
                        logging.warning('timeout in data reading')
                    self.__message += datum
                except struct.error:
                    logging.warning('struct error => maybe a reconnected board?')
        if self.__state == 1 and len(self.__message) >= self.__message_length:
            self.__client._process_board_message(self.__message_id, self.__message, self.__message_length)
            self.__reset_state()

    def __reset_state(self):
        self.__state = 0
        self.__header = ()
