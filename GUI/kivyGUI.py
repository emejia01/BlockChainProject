from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from BlockChainProject.GUI.database import DataBase
from google.cloud import datastore

from BlockChainProject.Node import Node
from hashlib import sha256
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/erikmejia/Desktop/blockchainproject-311018-0932eb94714c.json"

class CreateVoterAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submitVoter(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":

                # Check DB to see if email is already in use
                client = datastore.Client()
                query = client.query(kind="Nodes")
                query.add_filter("Email", "=", self.namee.text)
                result = list(query.fetch())

                if len(result) > 0:
                    invalidUser()
                else:
                    # Add to GCP
                    firstName, lastName = self.namee.text.split(" ")
                    currentNode = Node(firstName, lastName, self.email.text)
                    key = client.key('Nodes', currentNode.UID)
                    entity = datastore.Entity(key=key)

                    entity.update({
                        "FirstName": currentNode.FirstName,
                        "LastName": currentNode.LastName,
                        "Email": currentNode.Email,
                        "UID": currentNode.UID,
                        "balance": currentNode.balance,
                        "Blockchain": currentNode.Blockchain,
                        "isMiner": False,
                        "PASSWORD_HASH": sha256(self.password.text.encode("UTF-8")).hexdigest()
                    })

                    client.put(entity)
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

        # Check DB to see if email is already in use
        client = datastore.Client()
        query = client.query(kind="Nodes")
        query.add_filter("Email", "=", self.email.text)
        query.add_filter("PASSWORD_HASH", "=", sha256(self.password.text.encode("UTF-8")).hexdigest())
        result = list(query.fetch())

        if len(result) == 1:
            result = dict(result[0])
            firstName, lastName, email = result["FirstName"], result["LastName"], result["Email"]
            currentNode = Node(firstName, lastName, email)
            currentNode.UID = result["UID"]
            currentNode.balance = result["balance"]
            currentNode.Blockchain = result["Blockchain"]
            print(currentNode)

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

def invalidUser():
    pop = Popup(title='Invalid User',
                  content=Label(text='User already Exists!'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def insertError():
    pop = Popup(title='Insert Error',
                  content=Label(text='Oops! Something went wrong. Try again'),
                  size_hint=(None, None), size=(600, 600))

    pop.open()

kv = Builder.load_file("my.kv")

sm = WindowManager()
#db = DataBase("")

screens = [WelcomeWindow(name="welcome"),VoterLoginWindow(name="voterLogin"), MinerLoginWindow(name="minerLogin"),CreateVoterAccountWindow(name="createVoter"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "welcome"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()