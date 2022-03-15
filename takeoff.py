#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from gs_flight import FlightController, CallbackEvent
from gs_board import BoardManager
from time import time
from gs_module import CargoController

rospy.init_node("flight_test_node")  # инициализируем ноду

run = True  # переменная отвечающая за работу программы
position_number = 0  # счетчик пройденных точек


def timer(begin, duration):  # True if timer is going
    return duration > time() - begin


def set_timer(duration):
    # print('start')

    begin = time()
    while timer(begin, duration):
        pass

    # print('end')


def callback(event):  # функция обработки событй Автопилота
    global ap
    global run
    global coordinates
    global position_number

    event = event.data
    if event == CallbackEvent.ENGINES_STARTED:  # блок обработки события запуска двигателя
        print("engine started")
        ap.takeoff()  # отдаем команду взлета
    elif event == CallbackEvent.TAKEOFF_COMPLETE:  # блок обработки события завершения взлета
        print("takeoff complite")

        cargo.changeAllColor(255, 0, 0)
        print('red_on')

        set_timer(10)

        cargo.changeAllColor(0, 0, 0)
        print('red_off; start landing')

        ap.landing()  # отдаем команду посадки

    elif event == CallbackEvent.COPTER_LANDED:  # блок обработки события приземления
        print("finish programm")
        run = False  # прекращем программу


board = BoardManager()  # создаем объект бортового менеджера
ap = FlightController(callback)  # создаем объект управления полета

once = False  # переменная отвечающая за первое вхождение в начало программы

while not rospy.is_shutdown() and run:
    if board.runStatus() and not once:  # проверка подлкючения RPi к Пионеру

        print("start programm")

        cargo = CargoController()  # создаем объект магнитного захвата
        cargo.on()  # включаем магнит
        set_timer(1)  # задержка на 1с

        print("engine_starting")

        ap.preflight()  # отдаем команду выполенения предстартовой подготовки
        once = True

    pass
