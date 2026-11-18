 
import tkinter as tk
import random
import threading

# AUTUMN COLORS
BG = "#FFF3E2"
BROWN = "#593B2B"
ORANGE = "#C76B32"
GOLD = "#D9A441"
BEIGE = "#E8D3B5"
CARAMEL = "#B87945"
PEACH = "#F2C6A0"
WHITE = "#FFFFFF"


# TEXT TO SPEECH
def speak(text):
    def voice():
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as error:
            print("TTS error:", error)

    threading.Thread(target=voice, daemon=True).start()


# DATASET - ONLY 5 QUESTIONS
questions = [
    ("Which vegetable is known for the autumn season?",
     ["Carrot", "Potato", "Pumpkin", "Cucumber"],
     "Pumpkin",
     "It is orange and often used to make pie."),

    ("Is autumn a kind of celebration because people decorate their homes for it?",
     ["Yes", "No", "Only in summer", "Never"],
     "Yes",
     "People decorate with pumpkins and autumn leaves."),

    ("What do many trees lose in autumn?",
     ["Roots", "Leaves", "Branches", "Flowers"],
     "Leaves",
     "They fall from the trees."),

    ("Which animal is commonly associated with autumn?",
     ["Dolphin", "Squirrel", "Shark", "Penguin"],
     "Squirrel",
     "It collects nuts before winter."),

    ("What is the main reason leaves change color in autumn?",
     ["Less sunlight and shorter days",
      "Rain every day",
      "More water",
      "Strong wind"],
     "Less sunlight and shorter days",
     "Days become shorter and trees receive less sunlight.")
]


# MAIN APPLICATION
class AutumnQuizBot:

    def __init__(self, root):
        self.root = root
        self.root.title("Projekt Personal - Autumn AI QuizBot")
        self.root.geometry("700x700")
        self.root.configure(bg=BG)

        self.score = 0
        self.number = 0
        self.answered = False
        self.quiz = []

        # HEADER
        tk.Label(
            root,
            text="AUTUMN  AI QUIZBOT",
            font=("Georgia", 25, "bold"),
            bg=BROWN,
            fg=BG,
            pady=15
        ).pack(fill="x")

        # SCORE
        self.score_label = tk.Label(
            root,
            text="Score: 0/5",
            font=("Arial", 14, "bold"),
            bg=BG,
            fg=BROWN
        )
        self.score_label.pack(pady=10)

        # QUESTION
        self.question_label = tk.Label(
            root,
            text="Welcome to Autumn AI QuizBot!",
            font=("Arial", 15, "bold"),
            bg=BEIGE,
            fg=BROWN,
            wraplength=600,
            pady=20
        )
        self.question_label.pack(
            fill="x",
            padx=25,
            pady=10
        )

        # ANSWERS
        self.buttons = []

        for i in range(4):
            b = tk.Button(
                root,
                text="Answer",
                font=("Arial", 12),
                bg=WHITE,
                fg=BROWN,
                relief="flat",
                pady=10,
                command=lambda x=i: self.check(x)
            )
            b.pack(fill="x", padx=50, pady=5)
            self.buttons.append(b)

        # FEEDBACK
        self.feedback = tk.Label(
            root,
            text="Press START to begin!",
            font=("Arial", 12, "bold"),
            bg=BG,
            fg=BROWN,
            wraplength=600
        )
        self.feedback.pack(pady=12)

        # CONTROL BUTTONS
        controls = tk.Frame(root, bg=BG)
        controls.pack(pady=8)

        tk.Button(
            controls,
            text="START",
            command=self.start,
            bg=ORANGE,
            fg=WHITE
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="SPEAK",
            command=self.read,
            bg=GOLD,
            fg=BROWN
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="HINT",
            command=self.hint,
            bg=CARAMEL,
            fg=WHITE
        ).pack(side="left", padx=5)

        self.next_button = tk.Button(
            controls,
            text="NEXT",
            command=self.next,
            bg=ORANGE,
            fg=WHITE,
            state="disabled"
        )
        self.next_button.pack(side="left", padx=5)

        # CHATBOT
        tk.Label(
            root,
            text="Chat with  AI AutumnBot",
            font=("Georgia", 15, "bold"),
            bg=BG,
            fg=BROWN
        ).pack(pady=10)

        self.chat_entry = tk.Entry(
            root,
            font=("Arial", 12)
        )
        self.chat_entry.pack(
            fill="x",
            padx=30,
            ipady=5
        )

        self.chat_entry.bind(
            "<Return>",
            lambda event: self.chat()
        )

        tk.Button(
            root,
            text="SEND",
            command=self.chat,
            bg=BROWN,
            fg=WHITE
        ).pack(pady=5)

        self.chat_reply = tk.Label(
            root,
            text="Hello! Ask me about autumn!",
            bg=BG,
            fg=BROWN,
            wraplength=600
        )
        self.chat_reply.pack(pady=5)

    # START QUIZ
    def start(self):
        self.score = 0
        self.number = 0

        # SHUFFLE WITHOUT REPEATING QUESTIONS
        self.quiz = questions.copy()
        random.shuffle(self.quiz)

        self.score_label.config(text="Score: 0/5")
        self.show_question()

    # SHOW QUESTION
    def show_question(self):

        if self.number >= len(self.quiz):
            self.finish()
            return

        self.answered = False
        q = self.quiz[self.number]

        self.question_label.config(
            text=f"Question {self.number + 1}/5\n{q[0]}"
        )

        for i, option in enumerate(q[1]):
            self.buttons[i].config(
                text=option,
                state="normal",
                bg=WHITE,
                fg=BROWN
            )

        self.feedback.config(
            text="Choose your answer!",
            fg=BROWN
        )

        self.next_button.config(state="disabled")

    # CHECK ANSWER
    def check(self, index):

        if self.answered or not self.quiz:
            return

        self.answered = True
        q = self.quiz[self.number]
        answer = q[2]

        for b in self.buttons:
            b.config(state="disabled")

        if q[1][index] == answer:

            self.score += 1

            self.buttons[index].config(
                bg=CARAMEL,
                fg=WHITE
            )

            self.feedback.config(
                text="Correct! Amazing job!",
                fg=CARAMEL
            )

            speak("Correct! Amazing job!")

        else:

            self.buttons[index].config(bg=PEACH)

            self.feedback.config(
                text="Incorrect! Answer: " + answer,
                fg=BROWN
            )

            for b in self.buttons:
                if b["text"] == answer:
                    b.config(
                        bg=CARAMEL,
                        fg=WHITE
                    )

            speak("The correct answer is " + answer)

        self.score_label.config(
            text=f"Score: {self.score}/5"
        )

        self.next_button.config(state="normal")

    # NEXT QUESTION
    def next(self):

        if not self.answered:
            return

        self.number += 1
        self.show_question()

    # HINT
    def hint(self):

        if not self.quiz or self.number >= len(self.quiz):
            return

        message = self.quiz[self.number][3]

        self.feedback.config(
            text="Hint: " + message
        )

        speak(message)

    # TEXT TO SPEECH
    def read(self):

        if not self.quiz or self.number >= len(self.quiz):
            return

        q = self.quiz[self.number]

        speak(
            q[0] + ". Options: " + ", ".join(q[1])
        )

    # FINISH QUIZ
    def finish(self):

        self.question_label.config(
            text="QUIZ COMPLETED!"
        )

        self.feedback.config(
            text=f"You scored {self.score}/5! Well done!"
        )

        for b in self.buttons:
            b.config(
                text="Finished!",
                state="disabled"
            )

        self.next_button.config(state="disabled")

        speak(
            f"Quiz completed! Your score is {self.score} out of 5."
        )

    # CHATBOT
    def chat(self):

        message = self.chat_entry.get().lower().strip()
        self.chat_entry.delete(0, tk.END)

        if not message:
            return

        if "hello" in message or "hi" in message:
            reply = "Hello! Welcome to Autumn QuizBot!"

        elif "autumn" in message:
            reply = "Autumn is a beautiful season with colorful leaves!"

        elif "pumpkin" in message:
            reply = "Pumpkins are one of the symbols of autumn!"

        elif "leaves" in message:
            reply = "Many trees lose their leaves in autumn!"

        elif "squirrel" in message:
            reply = "Squirrels collect nuts before winter!"

        elif "score" in message:
            reply = f"Your score is {self.score} out of 5!"

        elif "quiz" in message:
            reply = "Our autumn quiz has only 5 questions!"

        elif "tts" in message or "speech" in message:
            reply = "TTS changes written text into spoken words!"

        else:
            reply = "Ask me about autumn, pumpkins, leaves or squirrels!"

        self.chat_reply.config(
            text="AutumnBot: " + reply
        )

        speak(reply)


# RUN PROGRAM
if __name__ == "__main__":

    root = tk.Tk()
    app = AutumnQuizBot(root)
    root.mainloop()
