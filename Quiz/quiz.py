import random
from tkinter import *
 
window = Tk()
window.title("Quiz")
window.geometry("600x450")
 
questions = [["Was ist die für den Körper gefährlichste Droge?","LSD","Cannabis","Pilze","Alkohol"]]
questions.append(["Was ist die beste Programmiersprache?","Javascript","C","Delphi","Python"])
questions.append(["Wie kalt ist flüssiger Stickstoff?","-87°C","-236°C","-346°C","-196°C"])
questions.append(["Aus was besteht Licht nicht?","Wellen","Energie","Teilchen","Strom"])
questions.append(["Wer erfand Python?","Albert Einstein","Steve Jobs","James Gosling","Guido van Rossum"])
questions.append(["Wie warm ist die Sonne im Kern?","15000°C","1600°C","200000000°C","15000000°C"])
 
def clear():
    list = window.grid_slaves()
    for n in list:
        n.destroy()
 
class Quiz:
    def __init__(self,quest):
        clear()
        self.Fragen = []
        for n in quest:
            self.Fragen.append(n)
        self.a1=""
        self.a2=""
        self.a3=""
        self.a4=""
        self.Ra=""
        self.RaBtn = Button(window, text="",font=("Arial",14))
        self.antw1 = Button(window, text="",font=("Arial",14))
        self.antw2 = Button(window, text="",font=("Arial",14))
        self.antw3 = Button(window, text="",font=("Arial",14))
        self.antw4 = Button(window, text="",font=("Arial",14))
        self.lock=False
        self.right=0
        self.naechste = Button(window,text="nächste",font=("Arial",14),command=self.Frage)
        self.nummer=0
        self.Max=3
        self.Frage()
    def Frage(self):
        self.naechste.grid(column=0,row=5,pady=5)
        if len(self.Fragen) > 0 and self.nummer < self.Max:
            self.nummer += 1
            self.lock = False
            randNum = random.randint(0,len(self.Fragen)-1)
            fragenText = self.Fragen[randNum][0]
            self.Ra = self.Fragen[randNum][-1]
            answers = []
            for i in range(1,5):
                answers.append(self.Fragen[randNum][i])
            random.shuffle(answers)
 
            self.a1 = answers[0]
            self.a2 = answers[1]
            self.a3 = answers[2]
            self.a4 = answers[3]
 
            frage = Text(window, font=("Arial", 14), width=40, height=2)
            frage.insert(END,fragenText)
            frage.grid(column=0,row=0,padx=80,pady=(75,0))
 
            self.antw1 = Button(window, text=self.a1, font=("Arial",14),width=39, command = self.control1)
            self.antw2 = Button(window, text=self.a2, font=("Arial",14),width=39, command = self.control2)
            self.antw3 = Button(window, text=self.a3, font=("Arial",14),width=39, command = self.control3)
            self.antw4 = Button(window, text=self.a4, font=("Arial",14),width=39, command = self.control4)
 
            self.antw1.grid(column=0,row=1,pady=(8,5))
            self.antw2.grid(column=0,row=2,pady=5)
            self.antw3.grid(column=0,row=3,pady=5)
            self.antw4.grid(column=0,row=4,pady=5)
 
            if self.a1 == self.Ra:
                self.RaBtn = self.antw1
            elif self.a2 == self.Ra:
                self.RaBtn = self.antw2
            elif self.a3 == self.Ra:
                self.RaBtn = self.antw3
            elif self.a4 == self.Ra:
                self.RaBtn = self.antw4
            self.Fragen.pop(randNum)
        else:
            clear()
            lb = Label(window, text="Du hast " + str(self.right) + " von " + str(self.Max) + " Fragen richtig beantwortet!",font=("Arial",14))
            lb.grid(column=0,row=0,padx=120,pady=(170,15))
            zumMenu = Button(window, text="Menu",font=("Arial",14),command=menuCreator)
            zumMenu.grid(column=0,row=1)
 
    def control1(self):
        if self.lock == False:
            if self.Ra != self.a1:
                self.antw1.configure(bg="red")
            else:
                self.antw1.configure(bg="green")
                self.right += 1
            self.RaBtn.configure(bg="green")
            self.lock = True
 
    def control2(self):
        if self.lock == False:
            if self.Ra != self.a2:
                self.antw2.configure(bg="red")
            else:
                self.antw2.configure(bg="green")
                self.right += 1
            self.RaBtn.configure(bg="green")
            self.lock = True
 
    def control3(self):
        if self.lock == False:
            if self.Ra != self.a3:
                self.antw3.configure(bg="red")
            else:
                self.antw3.configure(bg="green")
                self.right += 1
            self.RaBtn.configure(bg="green")
            self.lock = True
 
    def control4(self):
        if self.lock == False:
            if self.Ra != self.a4:
                self.antw4.configure(bg="red")
            else:
                self.antw4.configure(bg="green")
                self.right += 1
            self.RaBtn.configure(bg="green")
            self.lock = True
 
 
 
class Menu:
    def __init__(self):
        clear()
        self.Quiz = Button(window, text="Quiz", font=("Arial", 14), command=quizCreator, width=15, height=3)
        self.Quiz.grid(column=0,row=0,padx=218,pady=170)
 
def menuCreator():
    m = Menu()
 
def quizCreator():
    q = Quiz(questions)
 
menuCreator()
window.mainloop()