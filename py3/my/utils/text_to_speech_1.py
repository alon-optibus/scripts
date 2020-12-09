from my.utils.bash_1 import shell_process

DEFAULT_SPEECH_SPEED = 157
DEFAULT_TRANS = str.maketrans('*~', '  ')

def speak(text, speed=None):
    speed = speed or DEFAULT_SPEECH_SPEED

    if isinstance(text, bytes):
        text = text.decode()

    text = text.translate(DEFAULT_TRANS)
    p = shell_process('espeak -s {speed} -ven-us+f1 --stdin'.format(speed=int(speed)))
    p.stdin.write(text.encode())
    pass


def test():
    speak('wow~*hello 10:00')
    pass


if __name__ == '__main__':
    test()
