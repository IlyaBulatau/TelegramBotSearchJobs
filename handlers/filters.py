def is_valid_job(msg):
    if msg.text.isdigit():
        return False
    if 3 > len(msg.text) > 90:
        return False
    if msg.text.count(' ') > 4:
        return False
    for sy in msg.text:
        if sy in '?!:;*&^%#@()-+_}{[]\\/~':
            return False
    return True
    

def is_valid_count(msg):
    if not msg.text.isdigit():
        return False
    if msg.text[0] == '0':
        return False
    msg = int(msg.text)
    return 0 < msg < 46

def is_requests_callback(callback):
    import re
    compile = re.compile(r'202\d_\w{3}_\d{2}_\d{2}h_\d{2}m_\d{2}s')
    return re.fullmatch(compile, callback.data) != None
