import json
import random
import tkinter as tk
from tkinter import messagebox

# Palet Warna Tema Mewah (Millionaire Dark Theme)
BG_COLOR = "#0b0c10"
PANEL_COLOR = "#1f2833"
ACCENT_BLUE = "#66fcf1"
TEXT_WHITE = "#c5c6c7"
BTN_BG = "#45a29e"
BTN_HOVER = "#66fcf1"
GOLD = "#f39c12"

class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Who Wants to Be a Millionaire - Python Edition")
        self.root.geometry("1000x650")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.load_questions()
        self.current_question = 0
        self.score = "Rp 0"
        self.lifeline_5050_used = False

        self.create_widgets()
        self.load_question_data()

    def load_questions(self):
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "File 'questions.json' tidak ditemukan!")
            self.root.destroy()

    def create_widgets(self):
        # Frame Utama Kiri (Pertanyaan & Pilihan)
        self.left_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.left_frame.place(x=30, y=30, width=650, height=580)

        # Frame Utama Kanan (Daftar Hadiah & Lifeline)
        self.right_frame = tk.Frame(self.root, bg=PANEL_COLOR, bd=2, relief="ridge")
        self.right_frame.place(x=700, y=30, width=270, height=580)

        # Header / Info Kuis
        self.lbl_level = tk.Label(self.left_frame, text="SOAL 1 dari 10", font=("Arial", 14, "bold"), fg=GOLD, bg=BG_COLOR)
        self.lbl_level.pack(anchor="w", pady=(0, 10))

        # Kotak Pertanyaan
        self.question_box = tk.Label(
            self.left_frame, text="", font=("Arial", 16, "bold"), fg=TEXT_WHITE, bg=PANEL_COLOR,
            wraplength=600, justify="center", bd=2, relief="solid", padx=20, height=5
        )
        self.question_box.pack(fill="x", pady=(0, 20))

        # Tombol Pilihan Jawaban (A, B, C, D)
        self.btn_options = []
        letters = ["A", "B", "C", "D"]
        for i in range(4):
            btn = tk.Button(
                self.left_frame, text="", font=("Arial", 13, "bold"), fg="#000000", bg=BTN_BG,
                activebackground=BTN_HOVER, relief="flat", anchor="w", padx=20,
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(fill="x", pady=8, ipady=8)
            self.btn_options.append(btn)

        # Tombol Bantuan (Lifeline) di Kiri Bawah
        self.btn_lifeline = tk.Button(
            self.left_frame, text="⭐ Bantuan 50:50", font=("Arial", 11, "bold"), fg="#ffffff", bg="#c0392b",
            activebackground="#e74c3c", relief="flat", command=self.use_5050
        )
        self.btn_lifeline.pack(anchor="w", pady=(15, 0))

        # --- WIDGET PANEL KANAN ---
        tk.Label(self.right_frame, text="STRUKTUR HADIAH", font=("Arial", 12, "bold"), fg=ACCENT_BLUE, bg=PANEL_COLOR).pack(pady=15)

        self.prize_labels = []
        for i in range(len(self.questions)-1, -1, -1):
            p_text = f"Level {i+1} : {self.questions[i]['prize']}"
            lbl = tk.Label(self.right_frame, text=p_text, font=("Arial", 10), fg=TEXT_WHITE, bg=PANEL_COLOR)
            lbl.pack(anchor="w", padx=20, pady=2)
            self.prize_labels.append(lbl)

    def load_question_data(self):
        if self.current_question < len(self.questions):
            q_data = self.questions[self.current_question]
            self.lbl_level.config(text=f"SOAL {self.current_question + 1} dari {len(self.questions)}")
            self.question_box.config(text=q_data["question"])
            
            options = q_data["options"]
            letters = ["A", "B", "C", "D"]
            for i in range(4):
                self.btn_options[i].config(text=f"{letters[i]}.  {options[i]}", state=tk.NORMAL, bg=BTN_BG)
            
            self.update_prize_display()
        else:
            messagebox.showinfo("Selamat!", "🎉 LUAR BIASA! Anda berhasil menjawab semua pertanyaan dan menjadi MILYARDER!")
            self.root.destroy()

    def update_prize_display(self):
        for i, lbl in enumerate(self.prize_labels):
            idx = len(self.questions) - 1 - i
            if idx == self.current_question:
                lbl.config(fg=GOLD, font=("Arial", 10, "bold"))
            elif idx < self.current_question:
                lbl.config(fg="#27ae60", font=("Arial", 10)) # Sudah dilewati
            else:
                lbl.config(fg=TEXT_WHITE, font=("Arial", 10))

    def check_answer(self, selected_idx):
        q_data = self.questions[self.current_question]
        correct_idx = q_data["answer"]

        # Efek Animasi Warna Klik Sementara
        self.btn_options[selected_idx].config(bg=GOLD)
        self.root.update()
        self.root.after(800)

        if selected_idx == correct_idx:
            self.btn_options[selected_idx].config(bg="#27ae60") # Hijau (Benar)
            self.score = q_data["prize"]
            self.root.after(600)
            self.current_question += 1
            self.load_question_data()
        else:
            self.btn_options[selected_idx].config(bg="#c0392b") # Merah (Salah)
            self.btn_options[correct_idx].config(bg="#27ae60") # Tunjukkan jawaban benar
            self.root.update()
            self.root.after(1000)
            messagebox.showerror("Game Over", f"Jawaban Anda kurang tepat!\nAnda pulang dengan hadiah: {self.score}")
            self.root.destroy()

    def use_5050(self):
        if self.lifeline_5050_used:
            return
        
        self.lifeline_5050_used = True
        self.btn_lifeline.config(state=tk.DISABLED, bg="#555555")

        q_data = self.questions[self.current_question]
        correct_idx = q_data["answer"]

        # Pilih 2 opsi salah untuk disembunyikan
        wrong_indices = [i for i in range(4) if i != correct_idx]
        hidden_indices = random.sample(wrong_indices, 2)

        for idx in hidden_indices:
            self.btn_options[idx].config(text="", state=tk.DISABLED, bg="#2b2d42")

if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireGame(root)
    root.mainloop()
