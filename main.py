from datetime import datetime
import json, glob
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import kivy
import pip
from setuptools.command.install import install
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
universal = ''

Builder.load_file('design.kv')
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="Sign_up_screen"
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current="login_screen_success"
            global universal
            universal = uname
        else:
            self.ids.login_wrong.text= "Wrong username or password!"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        users[uname]={'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", "w") as file:
            users = json.dump(users,file)
        self.manager.current="sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def backtologin(self):
        self.manager.transition.direction='right'
        self.manager.current= "Login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current='Login_screen'
    def get_response(self, businessIndustry):
        businessIndustry=businessIndustry.lower()
        available_industries = glob.glob("response/*txt")

        available_industries = [Path(filename).stem for filename in
                                available_industries]
        if businessIndustry in available_industries:
            with open(f"response/{businessIndustry}.txt") as file:
                industry = file.readlines()
            self.ids.advice.text= random.choice(industry)

        else:
            self.ids.advice.text="Try rephrase the industry name"

    def get_answer(self, inputtext):
        with open("answer.json") as file:
            answer = json.load(file)
        answer[universal]={'username':universal, 'industry': inputtext}

        with open("answer.json", "w") as file:
            answer = json.dump(answer,file)
        self.manager.current = 'Login_screen'
        print(universal)

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()