import time
import threading
import pyperclip
import random
import string
import os
import sys


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def is_http_or_https(url):
    if url.startswith("http://") or url.startswith("https://"):
        return True
    return False


def print_infos(finalPath):
    print('**********************************************************************************')
    print('Image will be downloaded here : '+finalPath)
    print('**********************************************************************************')


def guess_extension(url):
    if 'png' in url:
        return '.png'
    if 'jpg' in url:
        return '.jpg'
    if 'jpeg' in url:
        return '.jpeg'


def print_model():
    print('*******************************************************')
    print('* Images auto-downloader start ! - Made by Retro0Root *')
    print('*******************************************************')


def print_to_stdout(clipboard_content):
    print ("Found url: %s" % str(clipboard_content))
    finalPath = path + get_random_string(10) + guess_extension(clipboard_content)
    print_infos(finalPath)
    os.system("wget -O {0} {1}".format(finalPath, clipboard_content))
    print('***********************************************************************************')


class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True


def main():
    watcher = ClipboardWatcher(is_http_or_https,print_to_stdout,5.)
    watcher.start()
    while True:
        try:
            print("Waiting for changed clipboard...")
            time.sleep(1)
        except KeyboardInterrupt:
            watcher.stop()
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        global path
        path = sys.argv[1]
        print_model()
        main()
    else:
        print('Run: python3 main.py [PATH TO DOWNLOAD IMAGE]')
        print('Ex: python3 main.py /home/samSepi0l/Documents/Images/')

