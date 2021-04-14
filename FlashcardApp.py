from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.properties import StringProperty, ListProperty
import random


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

    def testScreen(self):
        names = [i for i in range(0, len(self.flashcard_list))]
        len_names = len(names)
        random.shuffle(names)
        self.screensList = []
        for xx in range(len_names):
            i = names[xx]
            name = str(i)
            nexts = names[(xx+1) % len_names]
            question = self.flashcard_list[i][0]
            answer = self.flashcard_list[i][1]
            # s = CardScreen(name=name, nexts=str(nexts),
            #               question=question, answer=answer)
            self.screensList.append((name, nexts, question, answer))
            # self.add_widget(s)
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
        name = self.screensList[0][0]
        nexts = str(self.screensList[0][1])
        question = self.screensList[0][2]
        answer = self.screensList[0][3]
        s = CardScreen(name=name, nexts=nexts,
                       question=question, answer=answer)
        self.add_widget(s)
        self.screensList.append(self.screensList[0])
        xxx = self.screensList.pop(0)
        self.current = xxx[0]
        self.remove_widget(self.saved_screen)
        self.saved_screen = s

    def removeScreen(self):
        self.remove_widget(self.saved_screen)
        self.current = "main"


class FlashcardApp(App):
    pass


if __name__ == "__main__":
    FlashcardApp().run()
