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
        print(f"{filename} saved successfully.")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def load_data(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"Loaded data from {filename}.")
        return data
    except FileNotFoundError:
        print(f"No saved data found in {filename}, starting fresh.")
        return []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
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

def print_flashcards(cards):
    if not cards:
        print("No flashcards to show.")
        return
    for i, card in enumerate(cards, 1):
        print(f"{i}. Q: {card['question']} A: {card['answer']}")

def add_flashcards():
    while True:
        flashcard_q = input("Enter flashcard question: ").strip()
        if flashcard_q.lower() == "quit":
            break
        if not flashcard_q:
            print("Question cannot be empty. Please try again.")
            continue

        flashcard_a = input("Enter flashcard answer: ").strip()
        if not flashcard_a:
            print("Answer cannot be empty. Please try again.")
            continue

        card = {"question": flashcard_q, "answer": flashcard_a}
        flashcards.append(card)

    save_flashcards()
    print("Flashcards added successfully")

def delete_flashcards():
    if not flashcards:
        print("No flashcards to delete.")
        return

    print("\nFlashcards:")
    print_flashcards(flashcards)

    try:
        choice = int(input("Enter the number of the flashcard you want to delete: "))
        if 1 <= choice <= len(flashcards):
            confirm = input(f"Are you sure you want to delete flashcard '{flashcards[choice - 1]['question']}' y/n: ").strip().lower()
            if confirm == "y":
                removed_card = flashcards.pop(choice - 1)
                save_flashcards()
                print(f"Deleted Flashcard: {removed_card['question']}")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

def show_flashcards():
    print("\nFlashcards:")
    print_flashcards(flashcards)

def search_flashcards():
    if not flashcards:
        print("No flashcards to search.")
        return

    while True:
        keyword = input("Enter keyword to search (or 'quit' to return to menu): ").strip().lower()
        if keyword == "quit":
            break
        if not keyword:
            print("Search keyword cannot be empty. Please try again.")
            continue

        results = [card for card in flashcards if keyword in card['question'].lower() or keyword in card['answer'].lower()]

        if not results:
            print("No flashcards matched your search. Try again or type 'quit' to return.")
            continue

        print("\nSearch Results:")
        print_flashcards(results)
        break

def study_flashcards():
    global scores

    if not flashcards:
        print("No flashcards to study. Please add some first.")
        return

    print("\nStarting Study Mode! Type 'quit' to stop anytime.")
    correct = 0
    total = len(flashcards)

    cards_copy = flashcards[:]
    random.shuffle(cards_copy)

    for card in cards_copy:
        print(f"\n{card['question']}")
        user_answer = input("Enter your answer: ").strip()
        if user_answer.lower() == 'quit':
            break

        if user_answer.strip().lower() == card['answer'].strip().lower():
            print("Correct!\n")
            correct += 1
        else:
            print(f"Incorrect! The correct answer is: {card['answer']}\n")

    print(f"Study session finished. You got {correct} out of {total} correct.")

    scores.append({"correct": correct, "total": total})
    scores[:] = scores[-20:]
    save_scores()

def show_scores():
    if not scores:
        print("No scores recorded yet.")
        return

    print("\nPrevious Study Sessions:")
    for i, score in enumerate(scores, 1):
        print(f"{i}. {score['correct']} correct out of {score['total']}")

def main_menu():
    while True:
        print()
        print("Flashcards Quiz Menu!")
        print("1. Add Flashcard")
        print("2. Delete Flashcard")
        print("3. Show Flashcards")
        print("4. Search Flashcards")
        print("5. Study Flashcards")
        print("6. Show Scores")
        print("7. Exit")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            add_flashcards()
        elif choice == 2:
            delete_flashcards()
        elif choice == 3:
            show_flashcards()
        elif choice == 4:
            search_flashcards()
        elif choice == 5:
            study_flashcards()
        elif choice == 6:
            show_scores()
        elif choice == 7:
            print("Thank you for playing!")
            break
        else:
            print("Please enter a number between 1 and 7.")

if __name__ == "__main__":
    load_flashcards()
    load_scores()
    main_menu()
