import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json

FILENAME = "flashcards.json"
SCORES_FILENAME = "scores.json"

flashcards = []
scores = []

def save_data(filename, data):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving {filename}: {e}")

def load_data(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error loading {filename}: {e}")
        return []

def save_flashcards():
    save_data(FILENAME, flashcards)

def load_flashcards():
    global flashcards
    flashcards = load_data(FILENAME)

def save_scores():
    save_data(SCORES_FILENAME, scores)

def load_scores():
    global scores
    scores = load_data(SCORES_FILENAME)

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcards Quiz")
        self.geometry("500x400")

        btn_add = tk.Button(self, text="Add Flashcard", command=self.add_flashcard)
        btn_add.pack(pady=5)

        btn_delete = tk.Button(self, text="Delete Flashcard", command=self.delete_flashcard)
        btn_delete.pack(pady=5)

        btn_show = tk.Button(self, text="Show Flashcards", command=self.show_flashcards)
        btn_show.pack(pady=5)

        btn_search = tk.Button(self, text="Search Flashcards", command=self.search_flashcards)
        btn_search.pack(pady=5)

        btn_study = tk.Button(self, text="Study Flashcards", command=self.study_flashcards)
        btn_study.pack(pady=5)

        btn_scores = tk.Button(self, text="Show Scores", command=self.show_scores)
        btn_scores.pack(pady=5)

        btn_exit = tk.Button(self, text="Exit", command=self.quit)
        btn_exit.pack(pady=5)

    def add_flashcard(self):
        question = simpledialog.askstring("Add Flashcard", "Enter flashcard question:")
        if question is None or not question.strip():
            return
        answer = simpledialog.askstring("Add Flashcard", "Enter flashcard answer:")
        if answer is None or not answer.strip():
            return
        flashcards.append({"question": question.strip(), "answer": answer.strip()})
        save_flashcards()
        messagebox.showinfo("Success", "Flashcard added.")

    def delete_flashcard(self):
        if not flashcards:
            messagebox.showinfo("Info", "No flashcards to delete.")
            return

        questions = [f"{i+1}. {card['question']}" for i, card in enumerate(flashcards)]
        selected = simpledialog.askinteger("Delete Flashcard",
                                           "Select flashcard number to delete:\n" + "\n".join(questions))
        if selected is None:
            return
        if 1 <= selected <= len(flashcards):
            confirm = messagebox.askyesno("Confirm Delete",
                                          f"Are you sure you want to delete:\n{flashcards[selected - 1]['question']}?")
            if confirm:
                removed = flashcards.pop(selected - 1)
                save_flashcards()
                messagebox.showinfo("Deleted", f"Deleted flashcard:\n{removed['question']}")
        else:
            messagebox.showerror("Error", "Invalid selection.")

    def show_flashcards(self):
        if not flashcards:
            messagebox.showinfo("Info", "No flashcards to show.")
            return
        text = "\n".join([f"{i+1}. Q: {c['question']}  A: {c['answer']}" for i, c in enumerate(flashcards)])
        self.show_text_window("All Flashcards", text)

    def search_flashcards(self):
        if not flashcards:
            messagebox.showinfo("Info", "No flashcards to search.")
            return
        keyword = simpledialog.askstring("Search Flashcards", "Enter keyword to search:")
        if not keyword:
            return
        keyword = keyword.lower()
        results = [c for c in flashcards if keyword in c['question'].lower() or keyword in c['answer'].lower()]
        if not results:
            messagebox.showinfo("No Results", "No flashcards matched your search.")
            return
        text = "\n".join([f"{i+1}. Q: {c['question']}  A: {c['answer']}" for i, c in enumerate(results)])
        self.show_text_window("Search Results", text)

    def study_flashcards(self):
        if not flashcards:
            messagebox.showinfo("Info", "No flashcards to study. Please add some first.")
            return
        cards_copy = flashcards[:]
        random.shuffle(cards_copy)
        correct = 0
        total = len(cards_copy)
        for card in cards_copy:
            answer = simpledialog.askstring("Study", f"Question:\n{card['question']}\n\nEnter your answer (or Cancel to quit):")
            if answer is None:
                break
            if answer.strip().lower() == card['answer'].strip().lower():
                messagebox.showinfo("Correct", "Correct!")
                correct += 1
            else:
                messagebox.showinfo("Incorrect", f"Incorrect!\nCorrect answer: {card['answer']}")
        scores.append({"correct": correct, "total": total})
        scores[:] = scores[-20:]
        save_scores()
        messagebox.showinfo("Session Finished", f"You got {correct} out of {total} correct.")

    def show_scores(self):
        if not scores:
            messagebox.showinfo("Info", "No scores recorded yet.")
            return
        text = "\n".join([f"{i+1}. {score['correct']} correct out of {score['total']}" for i, score in enumerate(scores)])
        self.show_text_window("Previous Study Sessions", text)

    def show_text_window(self, title, content):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("400x300")
        text_widget = tk.Text(window, wrap=tk.WORD)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH)
        btn_close = tk.Button(window, text="Close", command=window.destroy)
        btn_close.pack(pady=5)

if __name__ == "__main__":
    load_flashcards()
    load_scores()
    app = FlashcardApp()
    app.mainloop()
