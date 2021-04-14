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

    def testScreen(self):
        names = [i for i in range(0, len(self.flashcard_list))]
        len_names = len(names)
        random.shuffle(names)
        for xx in range(len_names):
            i = names[xx]
            name = str(i)
            nexts = names[(xx+1) % len_names]
            question = self.flashcard_list[i][0]
            answer = self.flashcard_list[i][1]
            s = CardScreen(name=name, nexts=str(nexts),
                           question=question, answer=answer)
            self.screensList.append(s)
            self.add_widget(s)
        if len(names) > 0:
            self.current = str(names[0])

    def removeScreen(self):

        for i in self.screensList:
            self.remove_widget(i)
        self.current = "main"


class FlashcardApp(App):
    pass


if __name__ == "__main__":
    FlashcardApp().run()
