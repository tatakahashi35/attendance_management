# -*- coding: utf-8 -*-

from pynput import mouse, keyboard
import time
import datetime

DEBUG = False


class Monitoring:
    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.event_time_list = []

        with mouse.Listener(on_move=self.mouse_on_move) as mouse_listener, \
            keyboard.Listener(on_press=self.keyboard_on_press) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()


    def debug(self, hoge):
        if DEBUG:
            print(hoge)


    # Mouse
    def mouse_on_move(self, x, y):
        self.debug([x, y])
        if self.mouse_x != x or self.mouse_y != y:
            self.mouse_x = x
            self.mouse_y = y
            self.store_event_time()


    # Keyborad
    def keyboard_on_press(self, key):
        self.debug([key])
        self.store_event_time()


    def store_event_time(self):
        now = datetime.datetime.now()
        now_minute = now.replace(second=0, microsecond=0)
        if len(self.event_time_list) == 0:
            self.event_time_list = [now_minute]
        else:
            if self.event_time_list[-1] != now_minute:
                if self.event_time_list[-1].date() == now_minute.date():
                    # 日付が変わってない
                    self.event_time_list.append(now_minute)
                else:
                    self.output_file()
                    self.event_time_list = [now_minute]


    def output_file(self):
        event_time_str_list = [event_time.strftime('%H:%M') for event_time in self.event_time_list]
        filepath = "log/{date}.txt".format(date=self.event_time_list[-1].strftime('%Y-%m-%d'))
        with open(filepath, mode='w') as f:
            f.write('\n'.join(event_time_str_list))


if __name__ == '__main__':
    print('start monitoring')
    monitoring = Monitoring()
