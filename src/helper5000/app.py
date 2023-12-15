"""
My program helps the user complete his homework on time
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import time
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import sys

# Получите путь к каталогу, в котором находится исполняемый файл программы
executable_path = os.path.dirname(sys.executable)

# Получите путь к папке AppData текущего пользователя
appdata_path = os.path.expanduser('~\\AppData\\Local\\Programs\\Daniil\\Helper5000\\Helper5000.exe')

class Helper5000(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.str_time = ""
        
        target_label = toga.Label(
            "Введите цель: ",
            style=Pack(padding=(0, 5))
        )
        self.target_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(target_label)
        name_box.add(self.target_input)

        tasks_label = toga.Label(
            "Введите задачи: ",
            style=Pack(padding=(0, 5))
        )
        self.tasks_input = toga.TextInput(style=Pack(flex=1))

        tasks_box = toga.Box(style=Pack(direction=ROW, padding=5))
        tasks_box.add(tasks_label)
        tasks_box.add(self.tasks_input)

        volume_label = toga.Label(
            "Введите объём роботы: ",
            style=Pack(padding=(0, 5))
        )
        self.volume_input = toga.TextInput(style=Pack(flex=1))

        volume_box = toga.Box(style=Pack(direction=ROW, padding=5))
        volume_box.add(volume_label)
        volume_box.add(self.volume_input)

        term_label = toga.Label(
            "Введите срок роботы: ",
            style=Pack(padding=(0, 5))
        )
        self.term_input = toga.TextInput(style=Pack(flex=1))

        term_box = toga.Box(style=Pack(direction=ROW, padding=5))
        term_box.add(term_label)
        term_box.add(self.term_input)

        break_period_label = toga.Label(
            "Введите срок отдыха: ",
            style=Pack(padding=(0, 5))
        )
        self.break_period_input = toga.TextInput(style=Pack(flex=1))

        break_period_box = toga.Box(style=Pack(direction=ROW, padding=5))
        break_period_box.add(break_period_label)
        break_period_box.add(self.break_period_input)

        self.time_input = toga.TextInput(readonly=True, style=Pack(flex=1))

        time_box = toga.Box(style=Pack(direction=ROW, padding=5))
        time_box.add(self.time_input)

        button = toga.Button(
            "Начать",
            on_press=self.starting_programm,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(tasks_box)
        main_box.add(volume_box)
        main_box.add(term_box)
        main_box.add(break_period_box)
        main_box.add(time_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        
    def timer(self, times):
        self.minute = times // 60
        for i in range(self.minute):
            self.minute -= 1
            seconds = 60
            for j in range(seconds):
                seconds -= 1
                self.str_time = f"{self.minute}:{seconds}"
                print(self.str_time)
                time.sleep(1)
            # time.sleep(1)

    def speak(self, text, file):  # Создаёт голос
        # Создайте объект gTTS с текстом, который вы хотите преобразовать в речь
        tts = gTTS(text, lang="ru")

        # Сохраните речь как аудиофайл
        tts.save(file)

        # Воспроизведите сгенерированное аудио с помощью pygame
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        self.time_input.value = text

        # Дождитесь окончания воспроизведения аудио
        while pygame.mixer.music.get_busy():
            continue

    def starting_programm(self, widget):
        string = Scheduler(str_target=self.target_input.value, list_tasks=self.tasks_input.value, int_volume=int(self.volume_input.value),
                       int_term=int(self.term_input.value), int_break_period=int(self.break_period_input.value))
        self.speak(string.goal_achievement(), "goal_achievement.mp3")
        self.speak(string.goal_sharing(), 'goal_sharing.mp3')
        stringer = string.estimate_the_volume()
        self.speak(f'Возможный объём равен {stringer}', 'stringer.mp3')
        a = string.set_a_deadline()
        self.speak(f'Полный срок равен {a}', 'set_a_deadline.mp3')
        b = string.set_a_break()
        self.speak(f'Полный срок отдыха равен {b}', 'set_a_break.mp3')
        
        for i in range(stringer):
            print('Начало работы')
            self.speak('Начало работы', "aa.mp3")
            self.timer(a)
            print('Перемена!')
            self.speak('Перемена!', "bb.mp3")
            self.timer(b)

        self.speak('Конец работы!', "сc.mp3")

class Scheduler(Helper5000):

    def __init__(self, str_target, list_tasks, int_volume=5, int_term=45, int_break_period=10,):
        """
        :param str_target: Gets the goal that the user wants to achieve
        :param int_volume: Gets the scope of the job
        :param int_term: Gets a deadline for completing homework
        :param int_break_period: Gets the period during which the user needs to rest
        """
        self.target = str_target
        self.tasks = list_tasks
        self.volume = int_volume
        self.term = int_term
        self.break_period = int_break_period

    def goal_achievement(self):
        print(f"Ваша цель: {self.target}")
        return f"Ваша цель: {self.target}"

    def goal_sharing(self):
        print(f'ваша цель разделена на: {self.tasks}')
        return f'ваша цель разделена на: {self.tasks}'
    
    def estimate_the_volume(self):
        the_full_amount = self.volume
        print(f'Возможный объём равен {the_full_amount}')
        return the_full_amount

    def set_a_deadline(self):
        my_term = self.term * 60
        print(f'Полный срок равен {my_term}')
        return my_term

    def set_a_break(self):
        my_term2 = self.break_period * 60
        print(f'Полный срок отдыха равен {my_term2}')
        return my_term2

def main():
    return Helper5000()
