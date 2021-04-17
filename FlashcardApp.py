from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.properties import StringProperty, ListProperty
import random
import sqlite3


class MainScreen(Screen):
    pass


class AddFlashCardScreen(Screen):
    pass


class CardScreen(Screen):
    nexts = StringProperty("")
    question = StringProperty("")
    answer = StringProperty("")


class ScreenManagement(ScreenManager):
    shared_question = StringProperty("")
    shared_answer = StringProperty("")
    flashcard_list = ListProperty([])
    screensList = ListProperty([])
    saved_screen = None
    con = sqlite3.connect('flashCard.db')
    cur = con.cursor()

    def testScreen(self):
        try:
            flashcard_list_from_db = list(self.con.execute(
                "select question, answer from flashCard"))
        except:
            flashcard_list_from_db = []
        names = [i for i in range(len(flashcard_list_from_db))]
        len_names = len(names)
        random.shuffle(names)
        self.screensList = []
        for xx in range(len_names):
            i = names[xx]
            name = str(i)
            nexts = names[(xx+1) % len_names]
            question = flashcard_list_from_db[i][0]
            answer = flashcard_list_from_db[i][1]
            # s = CardScreen(name=name, nexts=str(nexts),
            #               question=question, answer=answer)
            self.screensList.append((name, nexts, question, answer))
            # self.add_widget(s)
        if len(self.screensList) == 1:
            name = "1"
            nexts = "blank"
            self.screensList.append((name, nexts, question, answer))

        if len(self.screensList) > 0:
            name = self.screensList[0][0]
            nexts = str(self.screensList[0][1])
            question = self.screensList[0][2]
            answer = self.screensList[0][3]
            s = CardScreen(name=name, nexts=nexts,
                           question=question, answer=answer)
            self.saved_screen = s
            self.add_widget(s)
            self.screensList.append(self.screensList[0])
            xxx = self.screensList.pop(0)
            self.current = xxx[0]

    def next_screen(self):
        cur_name = self.current
        name = self.screensList[0][0]
        nexts = str(self.screensList[0][1])
        question = self.screensList[0][2]
        answer = self.screensList[0][3]
        # if name == cur_name:
        #    name = name+"v2"
        s = CardScreen(name=name, nexts=nexts,
                       question=question, answer=answer)
        # print(name, cur_name)
        self.add_widget(s)
        self.screensList.append(self.screensList[0])
        # xxx = self.screensList[0]
        self.screensList.pop(0)
        self.current = name
        self.remove_widget(self.saved_screen)
        self.saved_screen = s

    def removeScreen(self):
        self.remove_widget(self.saved_screen)
        self.current = "main"

    def add_card(self):
        self.flashcard_list = [(self.shared_question, self.shared_answer)]
        # cur = con.cursor()

        try:
            self.con.execute("create table flashCard(question, answer)")
        except:
            pass

        with self.con:
            self.con.executemany(
                "insert into flashCard (question, answer) values (?, ?)", self.flashcard_list)

    def drop_table(self):
        with self.con:
            try:
                self.con.execute("drop table flashCard")
            except:
                pass

    def Print_db(self):
        for row in self.con.execute("select question, answer from flashCard"):
            print(row)


class FlashcardApp(App):
    pass


if __name__ == "__main__":
    FlashcardApp().run()
