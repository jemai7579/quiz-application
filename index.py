import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import time

quiz_data = [
    {"question": "Quelle est la capitale de la France ?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": "Paris"},
    {"question": "Quelle ville est surnommée : la ville qui ne dort jamais ?", "options": ["Tokyo", "New York", "Paris", "Dubaï"], "answer": "New York"},
    {"question": "Dans quel pays le flamenco est-il né ?", "options": ["Portugal", "Espagne", "Italie", "Grèce"], "answer": "Espagne"},
    {"question": "Le mont Fuji est un symbole national de quel pays ?", "options": ["Chine", "Japon", "Corée du Sud", "Vietnam"], "answer": "Japon"},
    {"question": "Dans quel pays a été inventé le tango ?", "options": ["Espagne", "Brésil", "Argentine", "Mexique"], "answer": "Argentine"},
    {"question": "Quelle ville est surnommée « la capitale mondiale du carnaval » ?", "options": ["Venise", "Rio de Janeiro", "La Nouvelle-Orléans", "Nice"], "answer": "Rio de Janeiro"},
    {"question": "Dans quel pays se trouve le Taj Mahal ?", "options": ["Inde", "Pakistan", "Népal", "Bangladesh"], "answer": "Inde"},
    {"question": "Quelle spécialité culinaire est originaire du Maroc ?", "options": ["Couscous", "Paella", "Pizza", "Moussaka"], "answer": "Couscous"},
    {"question": "Quelle boisson est la plus consommée au Royaume-Uni, après l'eau ?", "options": ["Café", "Thé", "Bière", "Limonade"], "answer": "Thé"},
    {"question": "Quel pays est connu pour ses aurores boréales et ses volcans actifs ?", "options": ["Suède", "Finlande", "Islande", "Norvège"], "answer": "Islande"},
    {"question": "Dans quel pays se déroule la fête des morts (Día de los Muertos) ?", "options": ["Espagne", "Pérou", "Mexique", "Colombie"], "answer": "Mexique"},
    {"question": "Quelle ville est considérée comme le berceau de la démocratie ?", "options": ["Athènes", "Rome", "Paris", "Londres"], "answer": "Athènes"}]

if not os.path.exists('quiz_data.json'):
    with open('quiz_data.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, indent=4, ensure_ascii=False)

class ModernQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 BRAIN BATTLE - Quiz")
        self.root.geometry("900x700")
        self.root.configure(bg="#0F172A")
        self.root.resizable(False, False)
        self.current_image = None

        self.colors = {
            "bg": "#0F172A",
            "card": "#1E293B",
            "primary": "#6366F1",
            "secondary": "#8B5CF6",
            "success": "#10B981",
            "danger": "#EF4444",
            "warning": "#F59E0B",
            "text": "#F1F5F9",
            "button": "#334155",
            "hover": "#475569",
            "timer": "#F87171"
        }

        self.quiz_data = self.load_quiz_data()
        if not self.quiz_data:
            return

        self.current_question = 0
        self.score = 0
        self.total_questions = len(self.quiz_data)
        self.selected_option = None
        self.answer_buttons = []
        self.time_left = 10
        self.timer_running = False
        self.timer_id = None

        self.correct_count = 0
        self.wrong_count = 0

        self.setup_styles()
        self.setup_ui()
        self.show_question()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TProgressbar", thickness=20, troughcolor=self.colors["card"], background=self.colors["primary"], lightcolor=self.colors["primary"], darkcolor=self.colors["primary"])

        style.configure("Option.TButton", font=("Arial", 12), background=self.colors["button"], foreground=self.colors["text"], borderwidth=0, focuscolor="none")

        style.map("Option.TButton", background=[("active", self.colors["hover"])])

        style.configure("Action.TButton", font=("Arial", 14, "bold"), background=self.colors["primary"], foreground=self.colors["text"], borderwidth=0, focuscolor="none",padding=(20, 10))

        style.map("Action.TButton", background=[("active", self.colors["secondary"])])

        style.configure("Success.TButton", font=("Arial", 12), background=self.colors["success"], foreground=self.colors["text"], borderwidth=0)

        style.configure("Danger.TButton", font=("Arial", 12), background=self.colors["danger"], foreground=self.colors["text"], borderwidth=0)

    def load_quiz_data(self):
        try:
            if not os.path.exists('quiz_data.json'):
                messagebox.showerror("Erreur", "Fichier quiz_data.json non trouvé!")
                return None
            with open('quiz_data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {str(e)}")
            return None

    def setup_ui(self):
        self.header = tk.Frame(self.root, bg=self.colors["bg"], height=100)
        self.header.pack(fill="x", padx=20, pady=10)

        self.title_label = tk.Label(self.header, text="🌍 BRAIN BATTLE - QUIZZ", font=("Arial", 28, "bold"), fg=self.colors["text"], bg=self.colors["bg"])
        self.title_label.pack(side="left")

        self.score_label = tk.Label(self.header, text=f"🏆 Score: 0/{self.total_questions}", font=("Arial", 16), fg=self.colors["text"], bg=self.colors["bg"])
        self.score_label.pack(side="right")

        self.timer_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.timer_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.timer_label = tk.Label(self.timer_frame, text="⏱️ 10s", font=("Arial", 16, "bold"), fg=self.colors["timer"], bg=self.colors["bg"])
        self.timer_label.pack(side="right")

        self.progress_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.progress_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.progress = ttk.Progressbar(self.progress_frame, length=800, mode="determinate")
        self.progress.pack(fill="x")

        self.progress_text = tk.Label(self.progress_frame, text="Question 1/12", font=("Arial", 12), fg=self.colors["text"], bg=self.colors["bg"])
        self.progress_text.pack(pady=(5, 0))

        self.question_card = tk.Frame(self.root, bg=self.colors["card"], highlightbackground=self.colors["primary"], highlightthickness=2, relief="flat")
        self.question_card.pack(fill="x", padx=20, pady=(20, 20), ipady=20)

        self.question_label = tk.Label(self.question_card, text="", font=("Arial", 18, "bold"), wraplength=800, justify="center", bg=self.colors["card"], fg=self.colors["text"], padx=20, pady=20)
        self.question_label.pack()

        self.options_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.action_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.action_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.submit_btn = ttk.Button(self.action_frame, text="🎯 Valider ma réponse", command=self.check_answer, style="Action.TButton", state="disabled")
        self.submit_btn.pack(side="left", padx=(0, 10))

        self.next_btn = ttk.Button(self.action_frame, text="➡ Question suivante", command=self.next_question, style="Action.TButton")
        self.next_btn.pack(side="left")
        self.next_btn.pack_forget()

        self.quit_btn = ttk.Button(self.action_frame, text="🚪 Quitter le quiz", command=self.confirm_quit, style="Action.TButton")
        self.quit_btn.pack(side="right")

        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), bg=self.colors["bg"], fg=self.colors["text"])
        self.feedback_label.pack(pady=(0, 20))

    def start_timer(self):
        self.time_left = 10
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

    def update_timer(self):
        if self.timer_running:
            self.timer_label.config(text=f"⏱️ {self.time_left}s")

            if self.time_left <= 3:
                self.timer_label.config(fg=self.colors["danger"])
            elif self.time_left <= 5:
                self.timer_label.config(fg=self.colors["warning"])
            else:
                self.timer_label.config(fg=self.colors["timer"])

            if self.time_left > 0:
                self.time_left -= 1
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.show_correct_answer()
                self.feedback_label.config(text="⏰ Temps écoulé ! Passage à la question suivante.", fg=self.colors["danger"])
                self.wrong_count += 1
                self.root.after(2500, self.next_question)

    def show_question(self):
        self.stop_timer()
        self.next_btn.pack_forget()
        self.submit_btn.pack(side="left", padx=(0, 10))
        self.feedback_label.config(text="")

        question = self.quiz_data[self.current_question]

        self.question_label.config(text=question['question'])

        progress_value = (self.current_question / self.total_questions) * 100
        self.progress['value'] = progress_value
        self.progress_text.config(text=f"Question {self.current_question+1}/{self.total_questions}")

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.answer_buttons = []
        self.selected_option = None

        for i, option in enumerate(question['options']):
            btn = ttk.Button(self.options_frame, text=f"   {option}", style="Option.TButton", command=lambda opt=option: self.select_option(opt))
            btn.pack(fill="x", pady=5, ipady=10)
            self.answer_buttons.append(btn)

        self.submit_btn.config(state="disabled")

        self.start_timer()

    def select_option(self, option):
        for btn in self.answer_buttons:
            btn.configure(style="Option.TButton")

        for btn in self.answer_buttons:
            if btn.cget("text").strip() == option:
                btn.configure(style="Action.TButton")
                self.selected_option = option
                break

        self.submit_btn.config(state="enabled")

    def show_correct_answer(self):
        question = self.quiz_data[self.current_question]
        correct_answer = question['answer']

        for btn in self.answer_buttons:
            text = btn.cget("text").strip()
            if text == correct_answer:
                btn.configure(style="Success.TButton")
            btn.state(["disabled"])

    def check_answer(self):
        if not self.selected_option:
            messagebox.showwarning("Attention", "Veuillez sélectionner une réponse")
            return

        self.stop_timer()

        question = self.quiz_data[self.current_question]
        correct_answer = question['answer']

        for btn in self.answer_buttons:
            text = btn.cget("text").strip()
            if text == correct_answer:
                btn.configure(style="Success.TButton")
            elif text == self.selected_option and self.selected_option != correct_answer:
                btn.configure(style="Danger.TButton")
            btn.state(["disabled"])

        if self.selected_option == correct_answer:
            self.score += 1
            self.correct_count += 1
            self.feedback_label.config(text="✅ Bonne réponse !", fg=self.colors["success"])
        else:
            self.wrong_count += 1
            self.feedback_label.config(text=f"❌ Mauvaise réponse. La bonne réponse était : {correct_answer}",
                                     fg=self.colors["danger"])

        self.score_label.config(text=f"🏆 Score: {self.score}/{self.total_questions}")

        self.submit_btn.pack_forget()
        self.next_btn.pack(side="left")

    def next_question(self):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.show_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        self.stop_timer()

        for widget in self.root.winfo_children():
            widget.destroy()

        end_frame = tk.Frame(self.root, bg=self.colors["bg"])
        end_frame.pack(expand=True, fill="both", padx=20, pady=20)

        percentage = (self.score / self.total_questions) * 100

        if percentage == 100:
            message = "🎉 PARFAIT ! Vous êtes un expert ! 🎉"
            color = self.colors["success"]
        elif percentage >= 75:
            message = "👏 Excellent ! Très bon score !"
            color = self.colors["success"]
        elif percentage >= 50:
            message = "👍 Bien joué ! Score honorable."
            color = self.colors["warning"]
        else:
            message = "💪 Continuez à apprendre, vous vous améliorerez !"
            color = self.colors["danger"]

        tk.Label(end_frame, text="Quiz Terminé !", font=("Arial", 32, "bold"), bg=self.colors["bg"], fg=self.colors["primary"]).pack(pady=(50, 20))

        tk.Label(end_frame, text=f"Score final: {self.score}/{self.total_questions}", font=("Arial", 24), bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=10)

        tk.Label(end_frame, text=f"Pourcentage: {percentage:.1f}%", font=("Arial", 20), bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=10)

        tk.Label(end_frame, text=f"✅ Bonnes réponses: {self.correct_count}", font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["success"]).pack(pady=5)
        tk.Label(end_frame, text=f"❌ Mauvaises réponses: {self.wrong_count}", font=("Arial", 18), bg=self.colors["bg"], fg=self.colors["danger"]).pack(pady=5)

        tk.Label(end_frame, text=message, font=("Arial", 18), bg=self.colors["bg"], fg=color, wraplength=600).pack(pady=20)

        button_frame = tk.Frame(end_frame, bg=self.colors["bg"])
        button_frame.pack(pady=30)

        ttk.Button(button_frame, text="🔄 Rejouer", command=self.restart_quiz, style="Action.TButton").pack(side="left", padx=10, ipadx=20, ipady=10)

        ttk.Button(button_frame, text="Quitter", command=self.root.destroy, style="Action.TButton").pack(side="right", padx=10, ipadx=20, ipady=10)

    def confirm_quit(self):
        result = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir quitter le quiz ?\nVotre progression sera perdue.")
        if result:
            self.root.destroy()

    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.time_left = 10

        for widget in self.root.winfo_children():
            widget.destroy()

        self.setup_ui()
        self.show_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernQuizApp(root)
    root.mainloop()