# -*- coding: utf-8 -*-

import argparse
import os
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--filenamne', help='%Y-%m-%d', default='')
    args = parser.parse_args()
    filenamne = args.filenamne

    if filenamne == '':
        parser.print_help()
        sys.exit()


    # ファイル読み込み
    with open(os.path.join('log', filenamne + '.txt')) as f:
        event_time_list = f.readlines()


    # 1分ごとに active かどうかを表すリストを作成
    active_list = [0] * (60 * 24)
    for event_time in event_time_list:
        hour, minute = [int(d) for d in event_time.split(':')]
        active_list[60 * hour + minute] += 1
        # イベントから5分間は稼働扱い
        if 60 * hour + minute + 5 + 1 < len(active_list):
            active_list[60 * hour + minute + 5 + 1] -= 1


    # 稼働時間帯の計算
    attendance_time_list = []
    start = None
    end = None
    active_sum = 0
    for i in range(len(active_list)):
        active_sum += active_list[i]
        if active_sum > 0:
            if start is None:
                start = i
            else:
                if end is not None:
                    if end - i < 10:
                        # 10分以下のイベントなしは連続した稼働扱い
                        end = None
                    else:
                        attendance_time_list.append([start, end])
                        start = i
                        end = None
        else:
            if start is not None:
                end = i - 1
    if start is not None:
        if end is not None:
            attendance_time_list.append([start, end])
        else:
            attendance_time_list.append([start, len(active_list)])


    # 時間表示に変更
    for start, end in attendance_time_list:
        start_hour, start_minute = start // 60, start % 60
        end_hour, end_minute = end // 60, end % 60
        print('{start_hour}:{start_minute} - {end_hour}:{end_minute}'.format(
            start_hour=start_hour,
            start_minute=start_minute,
            end_hour=end_hour,
            end_minute=end_minute))
