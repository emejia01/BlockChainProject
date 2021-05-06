from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label

from google.cloud import datastore

from BlockChainProject.Protocol import *
from hashlib import sha256

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/theomanavazian/Desktop/blockchainproject-311018-0932eb94714c.json"


def getCurrentNode(email, password):
    # Check DB to see if email is already in use
    client = datastore.Client()
    query = client.query(kind="Nodes")
    query.add_filter("Email", "=", email)
    query.add_filter("PASSWORD_HASH", "=", sha256(password.encode("UTF-8")).hexdigest())
    result = list(query.fetch())

    if len(result) == 1:
        result = dict(result[0])
        firstName, lastName, email = result["FirstName"], result["LastName"], result["Email"]
        currentNode = Node(firstName, lastName, email)
        currentNode.UID = result["UID"]
        currentNode.balance = result["balance"]

        return currentNode
    else:
        return None



def getBlockByNum(num):
    # Get Blocks from GCP
    client = datastore.Client()
    query = client.query(kind="Blocks")
    query.add_filter("num", "=", num)
    results = list(query.fetch())

    # Format GCP data into Block Objects to return
    if results:
        result = dict(results[0])
        num, time, nonce, data, previousHash, currentHash = result["num"], result["time"], result["nonce"], result["data"], result["previousHash"], result["currentHash"]
        currentBlock = Block(nonce, data, previousHash) # TODO: change block counter
        currentBlock.num = num
        currentBlock.time = time
        currentBlock.currentHash = currentHash

        return currentBlock
    else:
        return None




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
    def segueBack(self):
        sm.current = 'welcome'















NODE = Node()

class VoterLoginWindow(Screen, EventDispatcher):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        n = getCurrentNode(self.email.text, self.password.text)

        if n:
            NODE.FirstName = n.FirstName
            NODE.LastName = n.LastName
            NODE.UID = n.UID
            NODE.balance = n.balance
            NODE.Email = n.Email
            MainWindow.currentBal = NODE.balance
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

    def segueBack(self):
        sm.current = 'welcome'













class MainWindow(Screen):

    bal = ObjectProperty(None)
    dropdown = ObjectProperty(None)

    def on_enter(self, *args):
        self.bal.text = str(NODE.balance)

    # Redundant exists in MINER class, maybe we move to protocol?????
    def isInMempool(self):
        # get all transactions from Mempool table in GCP
        client = datastore.Client()
        query = client.query(kind="Mempool")
        results = list(query.fetch())

        for result in results:
            result = dict(result)
            senderUID = result["senderID"]
            print('SENDER', senderUID)

            if str(senderUID) == str(NODE.UID):
                return True

        return False


    def segueBack(self):
        sm.current = "voterLogin"

    def submitVote(self):

        inMempool = self.isInMempool()

        print(inMempool)

        if NODE.balance == 0:
            notEnoughTokems()
            return
        elif inMempool:
            mempoolError()
            return


        content = FloatLayout()
        self.popup = Popup(title='Are you sure you want to cast this vote? \n this cannot be undone',
                    content=content,
                    size_hint=(None, None),
                    size=(600, 600),
                    title_align='center')

        button = Button(text="Yes",
                        size_hint=(0.6, 0.2),
                        pos_hint={"x": .2, "y": 0.1},
                        on_press=self.createTransaction,
                        on_release=self.popup.dismiss)
        content.add_widget(button)
        self.popup.open()

    def createTransaction(self, val):
        p = Protocol()

        # self.bal.text = '0' -> bal will auto set to 0 once the block its apart of is mined
        if self.selection == 'Bitcoin':
            rec = '124d0d8d47c3f4eddfa27c8004057d9f57fe52b76ec7e6c2c27d7c570ef984c1'
        else:
            rec = '15b8ec7d599c752a65a324c25558be720a3db5a7f80d20a7340baaa8bb21f64d'

        p.Trasact(NODE.UID,rec)
        print(self.selection)

    def spinner_clicked(self, value=''):
        self.selection = value













class WelcomeWindow(Screen):

    wimg = ObjectProperty(None)
    voterLogin = ObjectProperty(None)
    createAccnt = ObjectProperty(None)


    def segueVoterLogin(self):
        sm.current = 'voterLogin'


    def segueCreateAccnt(self):
        sm.current = "createVoter"

    def segueVisualizer(self):
        sm.current = 'visualize'











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

def notEnoughTokems():
    pop = Popup(title='Not Enough Tokens!',
                  content=Label(text='You dont have enough Tokens to vote!.'),
                  size_hint=(None, None), size=(600, 600))

    pop.open()


def insertError():
    pop = Popup(title='Insert Error',
                  content=Label(text='Oops! Something went wrong. Try again'),
                  size_hint=(None, None), size=(600, 600))

    pop.open()

def mempoolError():
    pop = Popup(title='Transactioin Error',
                  content=Label(text='UID already in Mempool'),
                  size_hint=(None, None), size=(600, 600))

    pop.open()

def searchError():
    pop = Popup(title='Search Error',
                  content=Label(text='Block Doesnt Exist'),
                  size_hint=(None, None), size=(600, 600))

    pop.open()





def grab6():
    # get all transactions from Mempool table in GCP
    client = datastore.Client()
    query = client.query(kind="Mempool")
    # query.order = ["created"]
    results = list(query.fetch())

    allTransactions = []
    for result in results:
        result = dict(result)
        transactionUID = result["UID"]
        senderUID = result["senderID"]
        recieverID = result["recieverID"]
        transactionAmount = result["amount"]
        fee = result["fee"]


        currentTransaction = [str(transactionUID[0:5])+'..  ', str(senderUID[0:5])+'..  ', str(recieverID[0:5])+'..  ', str(transactionAmount)+"  ", fee]
        allTransactions.append(currentTransaction)

    return allTransactions


class VisualizerWindow(Screen):

    #MEMPOOL LABLES
    l1T = ObjectProperty(None)
    l2T = ObjectProperty(None)
    l3T = ObjectProperty(None)
    l4T = ObjectProperty(None)
    l5T = ObjectProperty(None)
    l6T = ObjectProperty(None)
    l7T = ObjectProperty(None)
    l8T = ObjectProperty(None)
    l9T = ObjectProperty(None)
    l10T = ObjectProperty(None)

#BLOCK LABLES
    l1B = ObjectProperty(None)
    l2B = ObjectProperty(None)
    l3B = ObjectProperty(None)
    l4B = ObjectProperty(None)
    l5B = ObjectProperty(None)
    l6B = ObjectProperty(None)

    #SearchBoxes:
    searchNum = ObjectProperty(None)


    def searchBlock(self):
        if self.searchNum.text !='':
            bl = getBlockByNum(int(self.searchNum.text))
            if bl:
                self.l1B.text = str(bl.num)
                self.l2B.text = str(bl.time)
                self.l3B.text = str(bl.nonce)
                self.l4B.text = str(bl.data)
                self.l5B.text = str(bl.previousHash)[0:7] + "..."
                self.l6B.text = str(bl.currentHash)[0:7] + "..."



            else:
                searchError()
        else:
            invalidForm()


    def updateMemPool(self,val):
        self.l1T.text = ''
        self.l2T.text = ''
        self.l3T.text = ''
        self.l4T.text = ''
        self.l5T.text = ''
        self.l6T.text = ''
        self.l7T.text = ''
        self.l8T.text = ''
        self.l9T.text = ''
        self.l10T.text = ''




        ls = grab6()
        size = len(ls)
        if size > 0:
            self.l1T.text = str(ls[-1])
        if size > 1:
            self.l2T.text = str(ls[-2])
        if size > 2:
            self.l3T.text = str(ls[-3])
        if size > 3:
            self.l4T.text = str(ls[-4])
        if size > 4:
            self.l5T.text = str(ls[-5])
        if size > 5:
            self.l6T.text = str(ls[-6])
        if size > 6:
            self.l7T.text = str(ls[-7])
        if size > 7:
            self.l8T.text = str(ls[-8])
        if size > 8:
            self.l9T.text = str(ls[-9])
        if size > 9:
            self.l10T.text = str(ls[-10])

    def on_enter(self, *args):
        self.updateMemPool(1)
        Clock.schedule_interval(self.updateMemPool, 1)



    def segueBack(self):
        sm.current = 'welcome'






class WindowManager(ScreenManager):
    pass




kv = Builder.load_file("my.kv")
sm = WindowManager()


screens = [WelcomeWindow(name="welcome"), VoterLoginWindow(name="voterLogin"), CreateVoterAccountWindow(name="createVoter"), MainWindow(name="main"), VisualizerWindow(name="visualize")]
for screen in screens:
    sm.add_widget(screen)


sm.current = "welcome"



class VoterChainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    VoterChainApp().run()
