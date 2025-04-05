import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# ---------------------- Quiz Game ----------------------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Benefits Quiz")
        self.conn = sqlite3.connect("quiz.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                option1 TEXT,
                option2 TEXT,
                option3 TEXT,
                option4 TEXT,
                answer INTEGER
            )
        """)
        self.conn.commit()
        self.insert_questions()
        self.load_questions()
        self.current_question = 0
        self.score = 0
        self.question_var = tk.StringVar()
        self.options = [tk.StringVar() for _ in range(4)]
        self.radio_var = tk.IntVar()
        self.setup_ui()
        self.display_question()
    
    def insert_questions(self):
        """ Inserts health-related questions if the table is empty """
        self.cursor.execute("SELECT COUNT(*) FROM questions")
        if self.cursor.fetchone()[0] == 0:
            questions = [
                ("Which vitamin is primarily responsible for boosting immunity?", "Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", 3),
                ("What is the main benefit of regular exercise?", "Stronger bones", "Improved heart health", "Better digestion", "All of the above", 4),
                ("Which food is a good source of Omega-3 fatty acids?", "Bananas", "Salmon", "Carrots", "Rice", 2),
                ("Drinking plenty of water helps with?", "Digestion", "Skin hydration", "Temperature regulation", "All of the above", 4),
                ("What is a major benefit of meditation?", "Improves focus", "Reduces stress", "Enhances emotional health", "All of the above", 4)
            ]
            self.cursor.executemany("INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)", questions)
            self.conn.commit()
    
    def load_questions(self):
        self.cursor.execute("SELECT * FROM questions")
        self.questions = self.cursor.fetchall()
        random.shuffle(self.questions)
    
    def setup_ui(self):
        tk.Label(self.root, textvariable=self.question_var, font=("Arial", 16), wraplength=400).pack(pady=10)
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, textvariable=self.options[i], variable=self.radio_var, value=i+1, font=("Arial", 14))
            rb.pack(anchor="w")
            self.radio_buttons.append(rb)
        self.next_button = tk.Button(self.root, text="Next", command=self.check_answer, font=("Arial", 14), bg="#4CAF50", fg="white")
        self.next_button.pack(pady=10)
    
    def display_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_var.set(q[1])
            for i in range(4):
                self.options[i].set(q[i+2])
            self.radio_var.set(0)
        else:
            self.show_grade()
    
    def check_answer(self):
        if self.radio_var.get():
            selected_option = self.radio_var.get()
            correct_answer = int(self.questions[self.current_question][6])  # Ensure integer type
            
            print(f"Selected Option: {selected_option}, Correct Answer: {correct_answer}")  # Debugging print
            
            if selected_option == correct_answer:
                self.score += 1
                messagebox.showinfo("Result", "Correct Answer!")
            else:
                correct_option_text = self.questions[self.current_question][correct_answer + 1]
                messagebox.showinfo("Result", f"Wrong Answer!\nCorrect Answer: {correct_option_text}")
            
            self.current_question += 1
            self.display_question()
        else:
            messagebox.showwarning("Warning", "Please select an answer before proceeding!")
    
    def show_grade(self):
        percentage = (self.score / len(self.questions)) * 100
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"
        messagebox.showinfo("Quiz Completed", f"Your Final Score: {self.score}/{len(self.questions)}\nGrade: {grade}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
