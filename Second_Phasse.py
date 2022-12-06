'''---------------------------------------------Draw_FSM---------------------------------------------'''
class Finite_State_Machine_Drawer():
    def __init__(self, FD, label):
        self.label = label
        self.FD = FD
        self.Create_R()

    def click(self, char, first):
        for a in self.FD.transitions:
            if ((str(a.reg) == char) & (str(a.start) == first)):
                self.D_FSMColored(str(a.start), str(a.end), str(a.reg))
            else:
                self.D_FSM(str(a.start), str(a.end), str(a.reg))

        self.fsm.attr("node", shape="plaintext", color="#fdfaf6")
        self.fsm.edge("", str(self.FD.start), color="#fdfaf6")

        self.fsm.render(view=False)

        self.clearReference()

    def D_FSM(self, fsmStart, fsmNext, fsmLabel):
        self.fsm.attr("node", shape="circle", color="#fdfaf6", fontcolor="#fdfaf6")
        self.fsm.edge(fsmStart, fsmNext, label=fsmLabel, color="#fdfaf6", fontcolor="#fdfaf6")

    def D_FSMColored(self, fsmStart, fsmNext, fsmLabel):
        self.fsm.attr("node", shape="circle", color="#fdfaf6", fontcolor="#fdfaf6")
        self.fsm.edge(fsmStart, fsmNext, fontcolor="#fb743e", label=fsmLabel, color="#fb743e")

    def Create_R(self):
        self.fsm = Digraph("FSM", format="svg", fileS_Name="fsm.txt")
        self.fsm.attr("node", shape="doublecircle", color="#fdfaf6", fontsize="10")  # fontsize can be resize
        self.fsm.attr(rankdir="LR", bgcolor="transparent", size="9,9!")

        try:
            for i in self.FD.accept:
                self.fsm.node(str(i), fontcolor="#fdfaf6")
        except:
            self.fsm.node(str(self.FD.accept))
        self.img = Window(self.label)

    def clearReference(self):
        time.sleep(0.8)
        self.fsm.clear()
        self.Create_R()


"""---------------------------------------------------GUI---------------------------------------------"""

import sys
from PyQt5.QtWidgets import *
'''from textSearchGui import TextEdit'''


class reg(QWidget):

    def search(self):
        self.BeginButton.setStyleSheet("background-color : rgba(120, 123, 147)")
        self.EndButton.setStyleSheet('background-color: None')
        self.textEdit.setReadOnly(True)  # It prevents typing in the text part.

        if self.nfaButton.isEnabled():
            fa = True
        else:
            fa = False

        # It is given as a reference so that they can operate on textedit and label
        self.src = TextEdit(self.lineEdit.text(), self.textEdit.toPlainText() + " ", self.textEdit, fa, 0.2, self.label)
        self.src.run()
        self.stop()

    def __init__(self):
        super(reg, self).__init__()
        # Specifies the background colors and the shape of the squares.
        self.setStyleSheet(("""background-color: 
                               rgba(35,39,42); 
                               color: rgba(153,170,181); 
                               border-style: solid;
                               border-radius: 6px;
                               border-width: 3px; 
                               border-color: 
                               rgba(68,68,68);"""))
        # Adding the buttons
        self.BeginButton = QPushButton('Start')
        self.EndButton = QPushButton('Stop')
        self.dfaButton = QPushButton('DFA')
        self.dfaButton.setEnabled(False)
        # Dfa button comes pressed
        self.dfaButton.setStyleSheet("background-color :rgba(120, 123, 147) ")
        self.nfaButton = QPushButton('NFA')
        self.File_Button = QPushButton('Open File')
        self.nfaButton.setFixedSize(80, 30)
        self.dfaButton.setFixedSize(80, 30)
        self.File_Button.setFixedSize(80, 30)
        self.BeginButton.setFixedSize(100, 30)
        self.EndButton.setFixedSize(100, 30)
        self.initUI()

    def initUI(self):
        # Adding text boxes and buttons
        self.text_css = 'border-style: none'  # erasing the lights.
        self.title = QLabel('reg')
        self.text = QLabel('Text')
        self.text.setFixedSize(40, 20)

        self.title.setStyleSheet(self.text_css)
        self.text.setStyleSheet(self.text_css)

        self.lineEdit = QLineEdit(self.text)
        self.textEdit = QTextEdit()
        self.label = QLabel(self)

        self.mainLayout = QHBoxLayout()
        self.regLayout = QHBoxLayout()
        self.metinLayout = QGridLayout()
        self.ssLayout = QHBoxLayout()  # Creating a layout with #start/stop buttons added
        self.layout1 = QVBoxLayout()  # creating a layout for the right side
        self.layout2 = QVBoxLayout()  # creating a layout for the left side
        self.nfaDfaLayout = QHBoxLayout()

        self.regLayout.addWidget(self.title)
        self.regLayout.addWidget(self.lineEdit)
        self.regLayout.addWidget(self.File_Button)

        self.metinLayout.addWidget(self.text, 0, 0, 1, 1)
        self.metinLayout.addWidget(self.textEdit, 0, 1, 5, 3)

        self.layout2.addLayout(self.regLayout)
        self.layout2.addLayout(self.metinLayout)
        self.layout2.addLayout(self.nfaDfaLayout)
        self.ssLayout.addStretch()
        self.ssLayout.addWidget(self.BeginButton)
        self.ssLayout.addWidget(self.EndButton)
        self.ssLayout.addStretch()

        self.nfaDfaLayout.addStretch()  # It leaves space.
        self.nfaDfaLayout.addWidget(self.dfaButton)
        self.nfaDfaLayout.addWidget(self.nfaButton)
        self.nfaDfaLayout.addStretch()

        self.layout1.addWidget(self.label)
        self.layout1.addLayout(self.ssLayout)

        self.mainLayout.addLayout(self.layout2)
        self.mainLayout.addLayout(self.layout1)

        self.dfaButton.clicked.connect(self.select)
        self.nfaButton.clicked.connect(self.select)
        self.File_Button.clicked.connect(self.open)

        self.BeginButton.clicked.connect(self.search)
        self.EndButton.clicked.connect(self.stop)

        self.setLayout(self.mainLayout)

        self.setFixedSize(1600, 700)
        self.setWindowTitle(' The Matcher  ')

    def open(self):
        options = QFileDialog.Options()
        # txt format file allows to be selected.
        fileS_Name, _ = QFileDialog.getOpenFileS_Name(self, 'QFileDialog.getOpenFileS_Name()', '',
                                                  'Text (*.txt)', options=options)

        if fileS_Name:
            with open(fileS_Name) as f:
                contents = f.read()
                self.textEdit.setText(contents)


    def stop(self):
        self.src.stop = True  # Stops the search process.
        self.textEdit.setReadOnly(False)
        self.EndButton.setStyleSheet("background-color : rgba(120, 123, 147)")
        self.BeginButton.setStyleSheet('background-color: None')

    def select(self):
        if self.sender().text() == 'DFA':
            self.dfaButton.setEnabled(True)
            self.nfaButton.setEnabled(False)  # Nfa button can be pressed.
            self.dfaButton.setStyleSheet("background-color: None ")
            self.nfaButton.setStyleSheet('background-color :rgba(120, 123, 147')
        else:
            self.nfaButton.setEnabled(False)
            self.dfaButton.setEnabled(True)
            self.nfaButton.setStyleSheet("background-color : rgba(120, 123, 147)")
            self.dfaButton.setStyleSheet('background-color: None')


def main():
    app = QApplication(sys.argv)
    ex = reg()
    ex.show()

    sys.exit(app.exec_())


if __S_Name__ == '__main__':
    main()


"""---------------------------------------------------NFA_to_DFA---------------------------------------------"""

'''import reg2nfa'''


class state:  # state object created
    def __init__(self, q, S_Name):
        self.S_Name = S_Name
        if type(q) == int:
            self.q = [q]
        else:
            self.q = q


class DFA_Form:
    def create_table(self):

        self.find_Lang_Used()

        for i in range(self.nfa.Q):
            s = state(i, i)
            self.states.append(s)
            self.adding_row_to_table()

        for current_state in self.states:
            for i, char in enumerate(self.Lang_Used):
                for transition in self.nfa.transitions:
                    if transition.start in current_state.q and char == transition.reg:
                        if self.table[current_state.S_Name][i] == 61:
                            Third_D = []
                            Third_D.append(transition.end)
                            self.table[current_state.S_Name][i] = Third_D
                        else:
                            self.table[current_state.S_Name][i].append(transition.end)

            for i, Third_D in enumerate(self.table[current_state.S_Name]):
                find = 0
                for control_state in self.states:
                    if Third_D == control_state.q:
                        self.table[current_state.S_Name][i] = control_state.S_Name
                        find = 1
                        break
                    elif Third_D == 61:
                        find = 1
                        break

                if find == 0:
                    if any([x in self.accept for x in Third_D]):
                        self.accept.append(self.number_of_states)
                    new_state = state(Third_D, self.number_of_states)
                    self.states.append(new_state)
                    self.adding_row_to_table()
                    self.table[current_state.S_Name][i] = self.number_of_states
                    self.number_of_states = self.number_of_states + 1

    def __init__(self, reg):
        self.reg = reg
        self.nfa = Reg_to_NFA.formal_nfa(reg)
        self.accept = self.nfa.accept
        self.start = self.nfa.start
        self.empty = 61
        self.Lang_Used = []
        self.states = []
        self.table = []
        self.transitions = []
        self.number_of_states = self.nfa.Q
        self.create_table()
        self.find_transitions()
        self.optimize()

    def optimize(self):

        for t in self.transitions:
            t.print_t()
        print()
        ends = [t.end for t in self.transitions]

        for q in range(self.number_of_states):
            if q not in ends and q != self.start:
                print(q, ' found')
                if q in self.accept:
                    self.accept.remove(q)

                for t in self.transitions:
                    if t.start == q:
                        self.transitions.remove(t)
                        break

                for t in self.transitions:
                    if t.start > q:
                        t.start = t.start - 1
                    if t.end > q:
                        t.end = t.end - 1

                self.number_of_states -= 1

                if self.start > q:
                    self.start = self.start - 1

                for i, a in enumerate(self.accept):
                    if a > q:
                        self.accept[i] -= 1

                self.optimize()
                break

    def find_transitions(self):
        for start, row in enumerate(self.table):
            for regnum, end in enumerate(row):

                t = transition(start, end, self.Lang_Used[regnum])
                if end != self.empty:
                    self.transitions.append(t)

    def adding_row_to_table(self):
        row = []
        for i in range(len(self.Lang_Used)):
            row.append(self.empty)

        self.table.append(row)

    def print_table(self):
        print('  |', end=' ')
        for char in self.Lang_Used:
            print(char, end=' ')
        print('')
        for i, row in enumerate(self.table):
            print(chr(i + 65), end=' | ')

            for unS_Named_states in row:
                print(chr(unS_Named_states + 65), end=' ')
            print('')

    def find_Lang_Used(self):
        for c in self.reg:
            if (c not in self.Lang_Used) and (c not in ['(', '|', ')', '*']):
                self.Lang_Used.append(c)

class transition:
    def __init__(self, start, end, reg):
        self.start = start
        self.end = end
        self.reg = reg

    # Print transition prettier.
    def print_t(self):
        print(f'\tq{self.start} -> q{self.end} when {self.reg} comes.')



"""---------------------------------------------------showFSM---------------------------------------------"""

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
import time


class Window(QWidget):
    def loadImage(self):
        self.acceptDrops()

        self.pixmap = QPixmap('fsm.txt.svg')

        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())

        QCoreApplication.processEvents()

    def __init__(self, label=None):
        super().__init__()
        self.label = label
        self.loadImage()




'''---------------------------------------------------State---------------------------------------------'''


class StateControl():
    def addState(self, obj: State):
        State_Dictionary = self.Adding(obj)
        self.allStates.append(State_Dictionary)

    def __init__(self):
        self.allStates = []


    def Adding(self, obj: State):
        State_DictionaryForNfa = {}
        State_DictionaryForNfa.update(
            {
                'state': obj.stateValue,
                'next': obj.next,
                'char': obj.values
            }
        )

        return State_DictionaryForNfa

class State():
    def __init__(self):
        self.values = []
        self.next = []
        self.stateValue = 0




'''---------------------------------------------------State_Manager---------------------------------------------'''

'''from state import State, StateControl
from drawFsm import Finite_State_Machine_Drawer'''


class Check_State:

    def Getting_list(self):
        for item in self.auto_control.transitions:
            if item.start not in self.stateList:
                self.stateList.append(item.start)
        self.stateCreator(self.expectedValueList, self.stateList)
        self.stateCreator(self.nextStateList, self.stateList, True)

    # Getting all values that desired as a list.
    def stateCreator(self, list, stateList, isItEnd=False):
        for value in stateList:
            tempList = []
            for item in self.auto_control.transitions:
                if item.start == value:
                    if isItEnd:
                        tempList.append(item.end)
                    else:
                        tempList.append(item.reg)
            list.append(tempList)
            del tempList


    def checkString(self, string):
        return self.isItAcceptable(string, self.auto_control.start)

    def isItAcceptable(self, string, stateValue, index=0):
        possibleStates = []

        try:
            for item in self.statesControl.allStates:
                if string[index] in item.get('char') and stateValue == item.get('state'):
                    for i in range(len(item.get('next'))):
                        if (item.get('char')[i] == string[index]):
                            if (stateValue != self.tempState or (
                                    stateValue == self.tempState and string[index] != self.tempChar)):
                                # Connection to drawFsm
                                currentState = str(item.get('state'))
                                self.Finite_State_Machine_Drawer.click(string[index], currentState)
                                self.tempState = item.get('state')
                                self.tempChar = string[index]

                            possibleStates.append(item.get('next')[i])

            # Wrong value or wrong state.
            if not possibleStates:
                return False

        except IndexError:
            # End of the process. That means out of the index range.
            try:
                if stateValue in self.auto_control.accept:
                    return True
            except:
                if stateValue == self.auto_control.accept:
                    return True
            else:
                return False

        for stateValue in possibleStates:
            # When the process is over, if True returns, that string is right.
            if (self.isItAcceptable(string, stateValue, index + 1)):
                return True
        # if it's not.
        return False

    def addToStatesControl(self):
        ''' Creating state then adding into statesControl.'''
        for i in range(len(self.stateList)):
            newState = State()
            for item in self.expectedValueList[i]:
                newState.values.append(item)
            for item in self.nextStateList[i]:
                newState.next.append(item)
            newState.stateValue = self.stateList[i]
            self.statesControl.addState(newState)
            del newState

  def __init__(self, auto_control, label):
        self.label = label
        self.auto_control = auto_control
        self.stateList = []
        self.expectedValueList = []
        self.nextStateList = []
        self.Finite_State_Machine_Drawer = Finite_State_Machine_Drawer(self.auto_control, label)
        self.transitionDict = {}

        self.tempState = -1
        self.tempChar = ""

        # Get all lists values.
        self.Getting_list()

        # Create a stateControl object.
        self.statesControl = StateControl()
        self.addToStatesControl()


'''---------------------------------------------------Text_Search_GUI---------------------------------------------'''

import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit)
'''import reg2nfa
import NFA_to_DFA
import statemanager'''
import time
import os


class TextEdit(QWidget):
    def __init__(self, reg='a*li', txt="Michael Adel", textEdit=None, fa=False, timer=0.4, label=None):
        super(TextEdit, self).__init__()

        self.stop = False
        self.reg = reg
        self.txt = txt
        self.textEdit = textEdit
        self.timer = timer

        self.wait(self.timer)

        if not fa:
            nfaController = Reg_to_NFA.formal_nfa(self.reg)
        else:
            nfaController = NFA_to_DFA.DFA_Form(self.reg)

        self.controlManager = statemanager.Check_State(nfaController, label)


    def highlight(self, start, n, col):
        cursor = self.textEdit.textCursor()
        clr = QColor(255, 255, 255)
        if col == 1:
            clr = QColor(0, 255, 0)
        elif col == 2:
            clr = QColor(255, 255, 0)
        elif col == 3:
            clr = QColor(255, 255, 255)

        # text color
        fmt = QTextCharFormat()
        fmt.setForeground(clr)

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right,
                            QTextCursor.KeepAnchor, n)
        cursor.mergeCharFormat(fmt)

    def wait(self, second):
        QCoreApplication.processEvents()
        time.sleep(second)


   def run(self):
        start = 0
        for i, char in enumerate(self.txt):
            if self.stop:
                break
            if char == " ":
                self.highlight(start, i - start, 2)
                self.wait(self.timer)

                if self.controlManager.checkString(self.txt[start: i]):
                    self.highlight(start, i - start, 1)
                else:
                    self.highlight(start, i - start, 3)
                start = i + 1
        os.remove("fsm.txt.svg")

if __S_Name__ == '__main__':
    app = QApplication(sys.argv)
    textdit = QTextEdit()

    textEdit = TextEdit('(ab)*', 'aba abbbaa abaaa aba ab ', textdit)
    textEdit.run()
    textEdit.show()

    sys.exit(app.exec_())

