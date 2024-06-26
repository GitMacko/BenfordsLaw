import re
import lorem
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, END
import random
import string
import collections
from wordcloud import WordCloud


def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()
    return text


def count_word_frequencies(text):
    clean_text_data = clean_text(text)
    words = clean_text_data.split()
    word_counts = Counter(words)
    return word_counts, len(words), len(word_counts)


def plot_pareto_distribution(word_counts):
    frequencies = np.array(list(word_counts.values()))
    frequencies = np.sort(frequencies)[::-1]

    cumulative_frequencies = np.cumsum(frequencies)
    cumulative_frequencies = cumulative_frequencies / cumulative_frequencies[-1]

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_frequencies, marker="o")
    plt.title("Rozkład pareta")
    plt.xlabel("Ranga słowa")
    plt.ylabel("Skumulowany udział")
    plt.grid(True)
    plt.show()


def plot_letter_distribution():
    text_lower = text_box.get(1.0, END).lower()
    letter_counts = collections.Counter(text_lower)
    letter_counts = {k: v for k, v in letter_counts.items() if k.isalpha()}
    all_letters = {letter: 0 for letter in string.ascii_lowercase}

    all_letters.update(letter_counts)
    sorted_letter_counts = dict(
        sorted(all_letters.items(), key=lambda item: item[1], reverse=True)
    )

    letters = list(sorted_letter_counts.keys())
    counts = list(sorted_letter_counts.values())
    norm = plt.Normalize(min(counts), max(counts))
    plt.figure(figsize=(10, 6))
    plt.bar(letters, counts, color=plt.cm.viridis(norm(counts)))
    plt.title("Częstość występowania liter")
    plt.xlabel("Litera")
    plt.ylabel("Liczba wystąpień")
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


def plot_word_distribution():
    text = text_box.get(1.0, END)
    words = text.lower().split()
    word_counts = collections.Counter(words)
    word_counts = {k: v for k, v in word_counts.items() if k.isalpha()}
    sorted_word_counts = dict(
        sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    )
    sorted_word_counts = dict(list(sorted_word_counts.items())[:20])

    words = list(sorted_word_counts.keys())
    counts = list(sorted_word_counts.values())

    plt.figure(figsize=(10, 6))
    norm = plt.Normalize(min(counts), max(counts))
    plt.bar(words, counts, color=plt.cm.viridis(norm(counts)))
    plt.title("Częstość występowania słów")
    plt.xlabel("Słowo")
    plt.ylabel("Liczba wystąpień")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
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
    word_counts, total_words, unique_words = count_word_frequencies(text)
    total_words_label.config(text=f"Liczba wszystkich słów: {total_words}")
    unique_words_label.config(text=f"Liczba różnych słów: {unique_words}")
    plot_pareto_distribution(word_counts)


def check_text():
    text = text_box.get(1.0, END)
    word_counts, total_words, unique_words = count_word_frequencies(text)
    total_words_label.config(text=f"Liczba wszystkich słów: {total_words}")
    unique_words_label.config(text=f"Liczba różnych słów: {unique_words}")
    letter_count = count_letters(text)
    result_label.config(text=f"Liczba liter: {letter_count}")


def plot_word_cloud():
    text = text_box.get(1.0, END)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    wordcloud = wc.generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def generate_random_text():
    random_text = lorem.text()
    text_box.delete(1.0, END)
    text_box.insert(END, random_text)


def generate_random_words(max_sentences=100):
    alphabet = string.ascii_lowercase
    sentences = []

    for _ in range(max_sentences):
        num_words = random.randint(1, 10)
        words = []
        for _ in range(num_words):
            word_length = random.randint(1, 10)
            word = "".join(random.choices(alphabet, k=word_length))
            words.append(word)

        sentence = " ".join(words).capitalize() + "."
        sentences.append(sentence)

    text_box.delete(1.0, END)
    text_box.insert(END, " ".join(sentences))


def count_letters(text):
    text_without_whitespace = text.replace(" ", "").replace("\n", "").replace("\t", "")
    letters_only = "".join(filter(str.isalpha, text_without_whitespace))
    return len(letters_only)


def plot_digit_distribution():
    text = text_box.get(1.0, END)
    digit_counts = Counter(filter(str.isdigit, text))

    all_digits = {str(d): 0 for d in range(10)}
    all_digits.update(digit_counts)

    sorted_digit_counts = dict(
        sorted(digit_counts.items(), key=lambda x: x[1], reverse=True)
    )

    digits = list(sorted_digit_counts.keys())
    counts = list(sorted_digit_counts.values())

    plt.figure(figsize=(10, 6))
    norm = plt.Normalize(min(counts), max(counts))
    plt.bar(digits, counts, color=plt.cm.viridis(norm(counts)))
    plt.title("Histogram występowania cyfr")
    plt.xlabel("Cyfra")
    plt.ylabel("Liczba wystąpień")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=0)
    plt.show()


root = tk.Tk()
root.title("Analiza Tekstu")
root.geometry("600x560")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

frame2 = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame2.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

scrollbar = Scrollbar(frame2)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_box = Text(frame2, wrap="word", yscrollcommand=scrollbar.set, height=20, width=60)
text_box.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.config(command=text_box.yview)

frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)
frame1.columnconfigure(2, weight=1)

open_button = tk.Button(
    frame1,
    text="Otwórz plik",
    command=open_file,
    width=20,
    height=2,
)
open_button.grid(row=0, column=0, padx=10, pady=10)

random_text_button = tk.Button(
    frame1,
    text="Generuj losowy wyrazy",
    command=generate_random_text,
    width=20,
    height=2,
)
random_text_button.grid(row=0, column=1, padx=10, pady=10)

random_text_button = tk.Button(
    frame1,
    text="Generuj losowe litery",
    command=generate_random_words,
    width=20,
    height=2,
)
random_text_button.grid(row=0, column=2, padx=10, pady=10)

frame3 = tk.Frame(root, height=5)
frame3.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
frame3.columnconfigure(0, weight=1)
frame3.columnconfigure(1, weight=1)
frame3.columnconfigure(2, weight=1)

total_words_label = tk.Label(frame3, text="Liczba wszystkich słów: 0")
total_words_label.grid(row=2, column=0, padx=10, sticky=tk.W)

unique_words_label = tk.Label(frame3, text="Liczba różnych słów: 0")
unique_words_label.grid(row=2, column=1, padx=10, sticky=tk.E)

result_label = tk.Label(frame3, text="Liczba liter: 0")
result_label.grid(row=2, column=2, padx=10, sticky="w")

check_text_button = tk.Button(
    frame3,
    text="Sprawdz tekst",
    command=check_text,
    width=20,
    height=2,
)
check_text_button.grid(row=2, column=3, padx=10, sticky="w")

frame4 = tk.Frame(root)
frame4.grid(row=3, column=0, columnspan=4, padx=10, sticky="nsew")
frame4.columnconfigure(0, weight=1)
frame4.columnconfigure(1, weight=1)
frame4.columnconfigure(2, weight=1)
frame4.columnconfigure(3, weight=1)
frame4.columnconfigure(4, weight=1)

analyze_button = tk.Button(
    frame4,
    text="Analizuj tekst",
    command=analyze_text,
    width=20,
    height=2,
)
analyze_button.grid(row=3, column=0, padx=5)

analyze_button = tk.Button(
    frame4,
    text="Analizuj liczbę słów",
    command=plot_word_distribution,
    width=20,
    height=2,
)
analyze_button.grid(row=3, column=1, padx=4)

analyze_button = tk.Button(
    frame4,
    text="Analizuj liczbę liter",
    command=plot_letter_distribution,
    width=20,
    height=2,
)
analyze_button.grid(row=3, column=2, padx=4)

analyze_digits_button = tk.Button(
    frame4,
    text="Analizuj liczbę cyfr",
    command=plot_digit_distribution,
    width=20,
    height=2,
)
analyze_digits_button.grid(row=3, column=3, padx=4)

analyze_button = tk.Button(
    frame4,
    text="Chmura punktów",
    command=plot_word_cloud,
    width=20,
    height=2,
)
analyze_button.grid(row=3, column=4, pady=10, padx=4)

root.mainloop()
