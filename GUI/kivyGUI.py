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





class MainWindow(Screen):

    bal = ObjectProperty(None)

    def logOut(self):
        sm.current = "login"


    def submitVote(self):
        self.bal.text ='0'

        pop = Popup(title='Vote',
                    content=Label(text='Your Vote has been recorded, Thank you'),
                    size_hint=(None, None), size=(600, 600))

        pop.open()




class WelcomeWindow(Screen):
    wimg = ObjectProperty(None)
    voterLogin = ObjectProperty(None)
    createAccnt = ObjectProperty(None)


    def segueVoterLogin(self):
        sm.current = 'voterLogin'


    def segueCreateAccnt(self):
        sm.current = "createVoter"



class WindowManager(ScreenManager):
    pass

def invalidUser():
    pop = Popup(title='Invalid User',
                  content=Label(text='User already Exists!'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


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


def insertError():
    pop = Popup(title='Insert Error',
                  content=Label(text='Oops! Something went wrong. Try again'),
                  size_hint=(None, None), size=(600, 600))

    pop.open()




kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("GUI/users.txt")

screens = [WelcomeWindow(name="welcome"),VoterLoginWindow(name="voterLogin"),CreateVoterAccountWindow(name="createVoter"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "welcome"


class VoterChainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    VoterChainApp().run()