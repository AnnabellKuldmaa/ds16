

MSG_SEP = ';'
BUFFER_SIZE = 1024
SPACE_INVADER = '||==||'

_RESP_OK = '00'
_GET_FILES = '01'
_FILE_LIST = '02'
_EDIT_FILE = '03'
_CREATE_FILE = '04'
_UPDATE_FILE = '05'
_OPEN_FILE = '06'
_EDIT_PERMISSION = '07'
_CONNECT = '08'
_FILE_NAME = '09'

def make_response(args):
    return MSG_SEP.join(args + [SPACE_INVADER])