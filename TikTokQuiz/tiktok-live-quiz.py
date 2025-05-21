import json
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from tkinter import ttk

# Load quiz questions from the JSON file
def load_quiz_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Class for the Quiz Application GUI
class QuizApp:
    def __init__(self, root, questions):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), padding=10)
        self.style.configure('TRadiobutton', font=('Helvetica', 12), padding=10)
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)

        self.questions = questions
        self.current_question = 0
        self.score = 0

        self.frame = ttk.Frame(root, padding="10 10 10 10")
        self.frame.pack(expand=True, fill='both')

        self.question_label = ttk.Label(self.frame, text="", wraplength=400, justify="left", background='lightblue')
        self.question_label.pack(pady=20, padx=20, fill='x')

        self.options = []
        self.var = tk.StringVar()

        for i in range(4):
            radio_button = ttk.Radiobutton(self.frame, text="", variable=self.var, value=chr(65 + i))
            radio_button.pack(anchor='w', padx=20, pady=5)
            self.options.append(radio_button)

        self.next_button = ttk.Button(self.frame, text="Next", command=self.next_question)
        self.next_button.pack(pady=20)

        self.load_question()

    def load_question(self):
        question = self.questions[self.current_question]
        self.question_label.config(text=f"Q{self.current_question + 1}: {question['question']}")
        
        for i, option in enumerate(question['options']):
            self.options[i].config(text=f"{chr(65 + i)}. {option}", value=chr(65 + i))
        
        self.var.set("")

    def next_question(self):
        selected_option = self.var.get()
        if not selected_option:
            messagebox.showwarning("Select an option", "Please select an option before proceeding.")
            return

        selected_index = ord(selected_option) - 65
        correct_index = self.questions[self.current_question]['solution']

        if selected_index == correct_index:
            self.score += 1

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.load_question()
        else:
            messagebox.showinfo("Quiz Completed", f"Your final score is {self.score}/{len(self.questions)}.")
            self.root.quit()

# Main function
def main():
    filename = 'quiz-questions.json'
    questions = load_quiz_questions(filename)

    root = tk.Tk()
    app = QuizApp(root, questions)
    root.mainloop()

if __name__ == "__main__":
    main()
