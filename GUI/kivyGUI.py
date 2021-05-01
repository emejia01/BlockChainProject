from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from BlockChainProject.GUI.database import DataBase


class CreateVoterAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submitVoter(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "voterLogin"
            else:
                invalidForm()
        else:
            invalidForm()

    def submitMiner(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "minerLogin"
            else:
                invalidForm()
        else:
            invalidForm()


    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class VoterLoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "createVoter"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class MinerLoginWindow(Screen):
    uid = ObjectProperty(None)




class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created



class WelcomeWindow(Screen):
    wimg = ObjectProperty(None)
    voterLogin = ObjectProperty(None)
    minerLogin = ObjectProperty(None)
    createAccnt = ObjectProperty(None)


    def segueVoterLogin(self):
        sm.current = 'voterLogin'

    def seqgueMinerLogin(selfs):
        sm.current = "minerLogin"

    def segueCreateAccnt(self):
        sm.current = "createVoter"



class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("GUI/users.txt")

screens = [WelcomeWindow(name="welcome"),VoterLoginWindow(name="voterLogin"), MinerLoginWindow(name="minerLogin"),CreateVoterAccountWindow(name="createVoter"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "welcome"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()