import random
import threading

from kivy import Logger
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.graphics import *


class IntroScreen(Screen):
    def __init__(self, Globals, *args, **kwargs):
        super(IntroScreen, self).__init__(*args, **kwargs)
        self.starClock = None
        self.shakeClock = None
        self.Globals = Globals

        self.shakeScreenX = Globals.width / Globals.GameSettings.intro_ship_shake_amount_divider * -1
        self.shakeScreenY = Globals.height / Globals.GameSettings.intro_ship_shake_amount_divider * -1
        self.shakeDistanceX = self.shakeScreenX * -1
        self.shakeDistanceY = self.shakeScreenX * -1
        self.shakeScreenWidth = Globals.width - (self.shakeScreenX * 2)
        self.shakeScreenHeight = Globals.height - (self.shakeScreenY * 2)
        self.shakeScreenLayout = self.ids["shakeScreen"]


    def on_enter(self, *args):
        self.starClock = Clock.schedule_interval(self.draw, self.Globals.GameSettings.intro_star_new_frame_delay)
        self.shakeClock = Clock.schedule_once(self.shake, self.Globals.GameSettings.intro_ship_shake_delay)

    def draw(self, _):
        self.shakeScreenLayout.canvas.clear()

        Globals = self.Globals

        for i in range(Globals.GameSettings.intro_star_amount):
            with self.shakeScreenLayout.canvas:
                Color(1, 1, 1)

                x, y = random.randint(0, Globals.width), random.randint(0, Globals.height / 2) + Globals.height / 2

                Rectangle(pos=(x, y), size=(Globals.width / Globals.GameSettings.intro_star_width_divider,
                                            Globals.height / Globals.GameSettings.intro_star_height_divider))
                Rectangle(pos=(self.shakeScreenX, self.shakeScreenY), size=(self.shakeScreenWidth,
                                                                            self.shakeScreenHeight),
                          source="textures/shipInside.png")
                # Rectangle(pos=(x - 10, y - 10), size=(Globals.width / 10 + 10, Globals.height / 50 + 10),
                #         color=Color(1, 0, 0, 0.1))

    def shake(self, _):
        animation = Animation(pos=self.shakeScreenLayout.pos, duration=0)

        for pos in self.Globals.GameSettings.intro_ship_shake_positions:
            animation += Animation(pos=(self.shakeScreenX * pos[0], self.shakeScreenY * pos[1]),
                                   duration=self.Globals.GameSettings.intro_ship_shake_shake_length)


        animation += Animation(pos=(0, 0), duration=self.Globals.GameSettings.intro_ship_shake_shake_length)
        print("start")
        animation.start(self.shakeScreenLayout)
        print("done")


    def on_leave(self, *args):
        self.starClock.cancel()
