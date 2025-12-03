from gui import *
from PyQt6.QtWidgets import *
import csv
import os

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        initialize the main window with the test score fields hidden.
        """
        super().__init__()
        self.setupUi(self)

        #checks lineEdit_scores to hide fields
        self.hide_fields()

        #number of test field changes then reveal appropriate label/lineEdits
        self.lineEdit_scores.textChanged.connect(self.update_test_fields)

        #submit button driving the interaction
        self.pushButton_submit.clicked.connect(lambda: self.submit())

    def hide_fields(self) -> None:
        """
        hides all fields when lineEdit is an empty string.
        """
        if self.lineEdit_scores.text() == "":
            self.label_submitted.hide()
            self.label_test1.hide()
            self.label_test2.hide()
            self.label_test3.hide()
            self.label_Test4.hide()
            self.lineEdit_test1.hide()
            self.lineEdit_test2.hide()
            self.lineEdit_test3.hide()
            self.lineEdit_test4.hide()
            self.lineEdit_test1.clear()
            self.lineEdit_test2.clear()
            self.lineEdit_test3.clear()
            self.lineEdit_test4.clear()

    def update_test_fields(self) -> None:
        """
        When the user submits the number of tests and it is 1-4, the corresponding fields show.
        When the lineEdit_scores field is empty, the test fields are hidden.
        """

        if self.lineEdit_scores.text().strip() == '':
            self.hide_fields()

        try:
            num_tests = int(self.lineEdit_scores.text())
        except ValueError:
            return

        #reveals label/test lineEdit based on input (1-4)
        if num_tests == 1:
            self.label_test1.show()
            self.lineEdit_test1.show()
            self.lineEdit_test1.setFocus()

        if num_tests == 2:
            self.label_test1.show()
            self.lineEdit_test1.show()
            self.label_test2.show()
            self.lineEdit_test2.show()
            self.lineEdit_test1.setFocus()

        if num_tests == 3:
            self.label_test1.show()
            self.lineEdit_test1.show()
            self.label_test2.show()
            self.lineEdit_test2.show()
            self.label_test3.show()
            self.lineEdit_test3.show()
            self.lineEdit_test1.setFocus()

        if num_tests == 4:
            self.label_test1.show()
            self.lineEdit_test1.show()
            self.label_test2.show()
            self.lineEdit_test2.show()
            self.label_test3.show()
            self.lineEdit_test3.show()
            self.label_Test4.show()
            self.lineEdit_test4.show()
            self.lineEdit_test1.setFocus()

    def calc_grade(self, test1, test2, test3, test4, num_of_tests) -> str:
        """
        Receives 4 test scores as floats and determines the letter grade to return
        :return: Letter grade as a string (A-F)
        """
        percent_grade = (test1 + test2 + test3 + test4) / num_of_tests
        if percent_grade >= 90:
            return 'A'
        elif percent_grade >= 80:
            return 'B'
        elif percent_grade >= 70:
            return 'C'
        elif percent_grade >= 60:
            return 'D'
        else:
            return 'F'

    def submit(self) -> None:
        """
        Sends student name (or anonymous) with the corresponding tests score(s) to a csv.
        Creates the csv if it does not exist already.
        Records test scores 1-4 and tracks the highest score submitted per student.
        """
        #hides previous label
        self.label_submitted.hide()

        #grabs student name and accepts any input
        student_name = self.lineEdit_name.text().strip()
        if len(student_name) == 0:
            student_name = "anonymous"

        #checks the input of the number of tests (1-4) as an int
        try:
            num_tests = int(self.lineEdit_scores.text())
            if num_tests <= 0 or num_tests > 4:
                QMessageBox.warning(self, "Input Error", "Please enter a valid number of tests (1-4)")
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid information for the number of scores")
            return

        #check test scores from revealed fields
        if len(self.lineEdit_test1.text()) > 0:
            try:
                test1 = float(self.lineEdit_test1.text())
                if test1 < 0 or test1 > 100:
                    QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 1")
                    return
            except ValueError:
                self.lineEdit_test1.clear()
                QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 1")
                return

        if len(self.lineEdit_test2.text()) > 0:
            try:
                test2 = float(self.lineEdit_test2.text())
                if test2 < 0 or test2 > 100:
                    QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 2")
                    return
            except ValueError:
                self.lineEdit_test2.clear()
                QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 2")
                return

        if len(self.lineEdit_test3.text()) > 0:
            try:
                test3 = float(self.lineEdit_test3.text())
                if test3 < 0 or test3 > 100:
                    QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 3")
                    return
            except ValueError:
                self.lineEdit_test3.clear()
                QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 3")
                return

        if len(self.lineEdit_test4.text()) > 0:
            try:
                test4 = float(self.lineEdit_test4.text())
                if test4 < 0 or test4 > 100:
                    QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 4")
                    return
            except ValueError:
                self.lineEdit_test4.clear()
                QMessageBox.warning(self, "Input Error", "Please enter a valid score for test 4")
                return

        #creates file if it doesn't exist
        while not os.path.isfile('student_grades.csv'):
            with open('student_grades.csv', 'a', newline='') as csvfile:
                content = csv.writer(csvfile)
                content.writerow(['student', 'test 1', 'test 2', 'test 3', 'test 4', 'highest', 'Grade'])
                break

        #updates the csv file
        with open('student_grades.csv', 'a', newline='') as csvfile:
            content = csv.writer(csvfile)
            test1 = 0.0
            test2 = 0.0
            test3 = 0.0
            test4 = 0.0
            #test1
            if len(self.lineEdit_test1.text()) == 0:
                test1 = 0.0
            else:
                test1 = float(self.lineEdit_test1.text())

            #test2
            if len(self.lineEdit_test2.text()) == 0:
                test2 = 0.0
            else:
                test2 = float(self.lineEdit_test2.text())

            #test3
            if len(self.lineEdit_test3.text()) == 0:
                test3 = 0.0
            else:
                test3 = float(self.lineEdit_test3.text())

            # test4
            if len(self.lineEdit_test4.text()) == 0:
                test4 = 0.0
            else:
                test4 = float(self.lineEdit_test4.text())
            num_tests = int(self.lineEdit_scores.text())
            scores = [test1, test2, test3, test4]
            highest = max(scores)
            grade = self.calc_grade(test1, test2, test3, test4, num_tests)
            content.writerow([student_name, test1, test2, test3, test4, highest, grade])

            #signals successful submission and clears fields
            self.label_submitted.setStyleSheet('color: green')
            self.label_submitted.show()
            self.lineEdit_scores.clear()
            self.lineEdit_name.clear()
            self.hide_fields()
            self.label_submitted.show()