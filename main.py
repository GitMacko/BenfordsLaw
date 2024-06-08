import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, END

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

def count_word_frequencies(text):
    clean_text_data = clean_text(text)
    words = clean_text_data.split()
    word_counts = Counter(words)
    return word_counts

def plot_pareto_distribution(word_counts):
    frequencies = np.array(list(word_counts.values()))
    frequencies = np.sort(frequencies)[::-1]

    cumulative_frequencies = np.cumsum(frequencies)
    cumulative_frequencies = cumulative_frequencies / cumulative_frequencies[-1]

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_frequencies, marker='o')
    plt.title('Rozkład Pareto - Częstości występowania słów')
    plt.xlabel('Ranga słowa')
    plt.ylabel('Skumulowany udział')
    plt.grid(True)
    plt.show()

def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()
        text_box.delete(1.0, END)
        text_box.insert(END, text)

def analyze_text():
    text = text_box.get(1.0, END)
    word_counts = count_word_frequencies(text)
    plot_pareto_distribution(word_counts)

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Rozkład Pareto - Analiza Tekstu")

# Tworzenie ramki tekstowej z paskiem przewijania
frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_box = Text(frame, wrap="word", yscrollcommand=scrollbar.set, height=20, width=60)
text_box.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.config(command=text_box.yview)

# Przycisk do otwierania plików
open_button = tk.Button(root, text="Otwórz plik", command=open_file)
open_button.grid(row=1, column=0, pady=10)

# Przycisk do analizy tekstu
analyze_button = tk.Button(root, text="Analizuj tekst", command=analyze_text)
analyze_button.grid(row=2, column=0, pady=10)
analyze_button.grid(row=2, column=0, pady=10)

# Uruchomienie głównej pętli aplikacji
root.mainloop()