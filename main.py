import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, 
    QLabel, QProgressBar, QGridLayout, QCheckBox, QButtonGroup,QScrollArea
)
from PyQt5.QtCore import (QRect, QPropertyAnimation, QParallelAnimationGroup, 
                        Qt, QAbstractAnimation,QEasingCurve)

from PyQt5.QtGui import QIcon
from Question import Questionnaire,Direction

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800,600)
        self.score=0
        self.progress_bar=QProgressBar()
        self.stacked_widget = QStackedWidget()
        self.reponses=[]
        self.pages = []
        self.questionnaire = Questionnaire("question.json")
        for i in range(1, self.questionnaire.get_length()+1):
            question_ = self.questionnaire.get_question_info(i)
            page = QWidget()
            layout = QGridLayout()
            label = QLabel(question_['question'])
            self.reponses.append(question_['reponse'])
            layout.addWidget(label)
            scroll=QScrollArea()
            scrollLayout=QGridLayout()

            button_group = QButtonGroup(self)
            button_group.setExclusive(True) 
            for labelname in question_['options']:
                checkbox = QCheckBox(labelname)
                checkbox.setMinimumHeight(100)
                checkbox.setMinimumWidth(500)
                button_group.addButton(checkbox)
                scrollLayout.addWidget(checkbox)

            scrollContent = QWidget()
            scrollContent.setLayout(scrollLayout)
            scroll.setWidget(scrollContent)

            layout.addWidget(scroll)
            page.setLayout(layout)
            self.stacked_widget.addWidget(page)
            self.pages.append(page)

        
        main_layout = QGridLayout()
        progress_bar = QProgressBar()
        progress_bar.setMaximum(9)
        progress_bar.setValue(0)
        button1 = QPushButton('Precedent')
        button1.clicked.connect(self.previousPage)
        button2 = QPushButton('Continuer')
        button2.clicked.connect(self.nextPage)
        main_layout.addWidget(progress_bar, 0, 0, 1, 2)
        main_layout.addWidget(self.stacked_widget, 1, 0, 1, 2)
        main_layout.addWidget(button1, 2, 0)      # Add button1 to row 1, column 0
        main_layout.addWidget(button2, 2, 1)   
        
        self.progress_bar = progress_bar
        self.initQuiz()
        self.setLayout(main_layout)

    def nextPage(self):
        if self.validateCurrentPage():
            next_page = self.current_page + 1
            if next_page == 10:
                self.result(next_page)
            if next_page < len(self.pages):
                #self.animation_gauche_droite(next_page-1,next_page)
                self.stacked_widget.setCurrentIndex(next_page)
                self.current_page = next_page
                self.progress_bar.setValue(next_page)

    def previousPage(self):
        prev_page = self.current_page - 1
        if prev_page >= 0:
            self.stacked_widget.setCurrentIndex(prev_page)
            self.current_page = prev_page
            self.progress_bar.setValue(prev_page)

    def result(self,index):
        i=0
        for pg in self.pages:
            checkboxes = pg.findChildren(QCheckBox)
            for checkbox in checkboxes:
                if checkbox.isChecked() and checkbox.text()==self.reponses[i]:
                    self.score+=1
            i+=1
        self.finalpage()
        self.stacked_widget.setCurrentIndex(index)

    def finalpage(self):
        page1 = QWidget()
        layout1 = QVBoxLayout()

        v = "Votre score est de : " + str(self.score) + "/"+str(self.questionnaire.get_length())
        slabel = QLabel(v)
        slabel.setMinimumHeight(50)
        slabel.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        layout1.addWidget(slabel)

        scrollarea1 = QScrollArea()
        scrollContent1 = QWidget()
        scrollLayout1 = QVBoxLayout()

        for i in range(1, self.questionnaire.get_length() + 1):
            question_ = self.questionnaire.get_question_info(i)
            page = QWidget()
            layout = QVBoxLayout()
            label = QLabel(question_['question'])
            layout.addWidget(label)

            scroll = QScrollArea()
            scrollContent = QWidget()
            scrollLayout = QVBoxLayout()

            for labelname in question_['options']:
                checkbox = QCheckBox(labelname)

                if checkbox.text() == question_['reponse']:
                    checkbox.setChecked(True)
                    checkbox.setStyleSheet("background-color: green;border-radius:8px")

                checkbox.setMinimumHeight(100)
                scrollLayout.addWidget(checkbox)

            scrollContent.setLayout(scrollLayout)
            scroll.setWidget(scrollContent)
            layout.addWidget(scroll)
            page.setLayout(layout)
            scrollLayout1.addWidget(page)

        scrollContent1.setLayout(scrollLayout1)
        scrollarea1.setWidget(scrollContent1)
        layout1.addWidget(scrollarea1)
        page1.setLayout(layout1)
        self.stacked_widget.addWidget(page1)

    
    def initQuiz(self):
        self.current_page = 0
        self.prev_page = 0
        self.progress_bar.setValue(0)
        self.stacked_widget.setCurrentIndex(0)

    def validateCurrentPage(self):
        checkboxes = self.pages[self.current_page].findChildren(QCheckBox)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                return True
        return False
    
    def animation_gauche_droite(self, index_depart, index_arrivee):
        """animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        animation.setDuration(1000)  # Durée de l'animation en millisecondes
        
        start_geometry = self.stacked_widget.widget(index_depart).geometry()
        end_geometry = self.stacked_widget.widget(index_arrivee).geometry()
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        
        # Ajout de l'interpolation (easing curve)
        animation.setEasingCurve(QEasingCurve.InOutQuad)  # Choix de la courbe
        
        animation.start()
        
        # Connexion de la fonction animation_finie à la fin de l'animation
        animation.finished.connect(lambda: )"""
        self.stacked_widget.setCurrentIndex(index_arrivee)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Python Quiz')
    window.setWindowIcon(QIcon('puzzle-piece.png'))
    window.show()
    sys.exit(app.exec_())
