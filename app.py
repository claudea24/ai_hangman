import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------
# Setup OpenAI
# -----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# AI Word Generator (cached)
# -----------------------------
@st.cache_data
def generate_word():
    prompt = "Generate exactly ONE random English word between 5 and 15 letters. Only output the word."

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=50,  # must be >= 16
        temperature=1.0,
    )

    word = response.output_text.strip().lower()
    return "".join(c for c in word if c.isalpha())


# -----------------------------
# AI Hint Generator
# -----------------------------
def generate_hint(word):
    prompt = f"Give a short hint for the English word '{word}'. Do not reveal the word."

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=50,
        temperature=0.7,
    )
    return response.output_text.strip()


# -----------------------------
# Initialize Game State
# -----------------------------
def init_game():
    st.session_state.word = generate_word()
    st.session_state.guessed = []
    st.session_state.lives = 6
    st.session_state.game_over = False
    st.session_state.hint = None


if "word" not in st.session_state:
    init_game()


# -----------------------------
# Guess Processing (Enter + Button)
# -----------------------------
def process_guess():
    if st.session_state.game_over:
        return

    guess = st.session_state.guess_input.lower()
    st.session_state.guess_input = ""  # clear input

    if guess and guess.isalpha() and len(guess) == 1:
        if guess not in st.session_state.guessed:
            st.session_state.guessed.append(guess)
            if guess not in st.session_state.word:
                st.session_state.lives -= 1


# -----------------------------
# UI
# -----------------------------
st.title("🎮 AI Hangman Game")
st.write("Guess the AI-generated word!")

# Display word
display_word = " ".join(
    [letter if letter in st.session_state.guessed else "_" for letter in st.session_state.word]
)
st.subheader(display_word)

# Show guessed letters & lives
st.write("Guessed letters:", " ".join(st.session_state.guessed))
st.write(f"❤️ Lives left: {st.session_state.lives}")

# Input box (ENTER works)
st.text_input(
    "Type a letter and press Enter or click Guess:",
    key="guess_input",
    max_chars=1,
    on_change=process_guess,
)

# Guess button (mouse users)
st.button("Guess", on_click=process_guess)

# -----------------------------
# Hint Button
# -----------------------------
if st.button("💡 Get AI Hint"):
    st.session_state.hint = generate_hint(st.session_state.word)

if st.session_state.hint:
    st.info("Hint: " + st.session_state.hint)

# -----------------------------
# Win / Lose Logic
# -----------------------------
if all(letter in st.session_state.guessed for letter in st.session_state.word):
    st.success(f"🎉 You WON! The word was: **{st.session_state.word}**")
    st.session_state.game_over = True

if st.session_state.lives <= 0:
    st.error(f"💀 Game Over! The word was: **{st.session_state.word}**")
    st.session_state.game_over = True

# -----------------------------
# Restart Button (FIXED)
# -----------------------------
if st.button("🔄 Restart Game"):
    st.cache_data.clear()
    init_game()
    st.rerun()