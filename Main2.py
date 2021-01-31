import vk
import plotly.graph_objects as go
import time
from bisect import bisect_left
from datetime import date
#import numpy as np
from Main1 import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import *
import sys

ACCESS_TOKEN = "9dc661b59dc661b59dc661b58b9db280db99dc69dc661b5c26ab527437c663b04510a38"


def double_exponentional_smoothing(series, alpha, beta):  # двойное экспоненциальное сглаживание
    res = [series[0]]
    for n in range(1, len(series) + 1):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series):
            value = res[-1]
        else:
            value = series[n]
        last_level, level = level, alpha * value + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        res.append(level + trend)
    return res[-1]


def unix_to_gmt(mass):
    for i in range(0, len(mass)):
        mass[i] = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(mass[i]))
    return mass


class Group:
    def __init__(self, owner_id, qt):  # инициализация класса
        self.qt = qt
        session = vk.Session(access_token=ACCESS_TOKEN)
        self.vkapi = vk.API(session)  # авторизация
        self.owner_id = -owner_id
        wall_posts = self.vkapi.wall.get(owner_id=self.owner_id, count=1, v=5.21)
        self.countall = wall_posts["count"]

        self.ls = []
        self.reps = []
        self.comms = []
        self.data = []

        offset = 0

        last = time.time()
        for i in range(0, self.countall, 100):  # из словаря получаем количество лайков, репостов, коммментариев и дату
            post = self.vkapi.wall.get(owner_id=self.owner_id, offset=offset, count=100, v=5.21)
            for j in post['items']:
                self.ls.append(j["likes"]["count"])
                self.reps.append(j["reposts"]["count"])
                self.comms.append(j["comments"]["count"])
                self.data.append(j["date"])
            offset += 100
            # print(time.time() - last)
            last = time.time()

        self.ls.reverse()  # реверс массивов, чтобы на графике данные отображались в человеческом виде
        self.reps.reverse()
        self.comms.reverse()
        self.data.reverse()

    def statistic(self, time_from, time_to):  # метод, находящий статистику сообщества
        # self.owner_id = -int(input())
        # time_from = input().split(".")
        # time_to = input().split(".")

        d = date(int(time_from[-1]), int(time_from[1]), int(time_from[0]))
        time_from_numb = time.mktime(d.timetuple())
        d = date(int(time_to[-1]), int(time_to[1]), int(time_to[0]))
        time_to_numb = time.mktime(d.timetuple())

        ls_pr = []
        data_pr = []
        comms_pr = []
        reps_pr = []
        activnost = []
        wts = [0.99, 0.5, 0.5]

        time_from_numb = bisect_left(self.data, time_from_numb)  # поиск ближайшего по значению в массиве элемента
        time_to_numb = bisect_left(self.data, time_to_numb)
        amount2_ls = self.ls[time_to_numb - 1]
        amount1_ls = self.ls[time_from_numb - 1]
        amount2_reps = self.reps[time_to_numb - 1]
        amount1_reps = self.reps[time_from_numb - 1]
        amount2_comms = self.comms[time_to_numb - 1]
        amount1_comms = self.comms[time_from_numb - 1]

        if amount1_ls != 0:  # нахождение общей статистики сообщества и перевод в проценты
            activnost.append(amount2_ls * 100 / amount1_ls)
        else:
            activnost.append(0)
        if amount1_reps != 0:
            activnost.append(amount2_reps * 100 / amount1_reps)
        else:
            activnost.append(0)
        if amount1_comms != 0:
            activnost.append(amount2_comms * 100 / amount1_comms)
        else:
            activnost.append(0)

        data = self.data[time_from_numb:time_to_numb]
        ls = self.ls[time_from_numb:time_to_numb]
        reps = self.reps[time_from_numb:time_to_numb]
        comms = self.comms[time_from_numb:time_to_numb]

        #print('=-=-=-==-=-=-==', ls, self.ls, '\n', time_from_numb, time_to_numb)

        ls_pr.append(ls[-1])
        ls_pr.append(round(double_exponentional_smoothing(ls, 0.7, 0.2)))
        data_pr.append(data[-1])
        data_pr.append(data[-1] + 86400)
        comms_pr.append(comms[-1])
        comms_pr.append(round(double_exponentional_smoothing(comms, 0.6, 0.2)))
        reps_pr.append(reps[-1])
        reps_pr.append(round(double_exponentional_smoothing(reps, 0.7, 0.2)))

        data = unix_to_gmt(data)  # Перевод времени из формата UNIX в GMT
        data_pr = unix_to_gmt(data_pr)

        self.graphic(self.qt.Plot_likes, data, data_pr, ls, ls_pr, 'Likes')
        self.graphic(self.qt.Plot_reposts, data, data_pr, reps, comms_pr, 'Commentaries')
        self.graphic(self.qt.Plot_comms, data, data_pr, comms, reps_pr, 'Reposts')
        return self.result(round(double_exponentional_smoothing(ls, 0.7, 0.2)))

    def graphic(self, window, data, data_pr, mass, mass_pr, name):  # графики, которые выведет программа
        window.clear()
        window.plot(mass, pen='r')

    def result(self, average):  # результат анализа, выводящийся программой
        if average > 100:
            if average <= 125:
                return (
                    'Советуем купить 2-3 рекламных поста для поддержания притока аудитории, а также развивать тему сообщества.')
            elif average > 125:
                return ('Стабильный рост сообщества. Самое время продавать рекламу!')
            return (
            'Активность участников вашего сообщества за выбранный период времени увеличилась на ', average - 100, ' %',)
        elif average == 100:
            return (
                'Активность участников вашего сообщества за выбранный период времени не изменилась. Советуем заняться рекламой для развития сообщества.')
        else:
            if average <= 30:
                return (
                    'Вам надо срочно купить около 10 рекламных постов и устроить розыгрыш или конкурс. Сообщество в упадке!')
            elif average > 30:
                return ('Советуем купить 5-8  рекламных постов и устроить розыгрыш или конкурс. Сообщество в упадке!')
            return (
            'Активность участников вашего сообщества за выбранный период времени уменьшилась на ', 100 - average, ' %',)



if __name__ == '__main__':
    b = Group()


'''fig = go.Figure()
        fig.add_trace(go.Scatter(x=data, y=mass, name=name,
                                 line=dict(color=color, width=4)))
        fig.add_trace(go.Scatter(x=data_pr, y=mass_pr, name=name + ' forecast',
                                 line=dict(color=color, width=4, dash='dashdot')))
        fig.update_layout(title=name + ' statistics',
                          xaxis_title='Time',
                          yaxis_title='Amount')
        fig.show()'''


# self.owner_id = 184112162
# self.owner_id = 164252168
# self.owner_id = 71729358           id групп
'''
a = Group(164252168)
a.statistic([1, 1, 1],[1, 1, 3000])
'''
