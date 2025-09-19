import speech_recognition as sr
import pyttsx3
from openai import OpenAI

#setup
client = OpenAI(api_key="OPEN_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

#configvoice
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

#storechathistory
conversation_history = [
    {"role": "system", "content": "You are a super cool, funny, and helpful AI like ChatGPT. Always address the user as 'Boss' in every response."}
]

#function
def speak(text):
    """Speak text reliably"""
    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def listen():
    """Listen from microphone and return text"""
    with sr.Microphone() as source:
        print("\nListening... (say 'exit' to menu, 'quit' to close)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn’t catch that.")
            return ""
        except sr.RequestError:
            print("Could not reach Google Speech Recognition.")
            return ""

def chatbot_response(user_message):
    """Get AI response with memory"""
    conversation_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
        max_tokens=200
    )

    ai_message = response.choices[0].message.content.strip()

    
    if not ai_message.lower().startswith("boss"):
        ai_message = "Boss, " + ai_message

    conversation_history.append({"role": "assistant", "content": ai_message})
    return ai_message

#chatmodes
def run_voice_mode():
    speak("Voice assistant mode activated. Say something, Boss.")
    while True:
        user_command = listen()
        if user_command == "":
            continue
        if "exit" in user_command.lower():
            speak("Returning to main menu, Boss.")
            break
        if any(word in user_command.lower() for word in ["stop", "quit", "bye"]):
            speak("Goodbye, Boss. Closing program.")
            exit()

        ai_reply = chatbot_response(user_command)
        print(f"AI: {ai_reply}")
        speak(ai_reply)

def run_chat_mode():
    print("Chatbot mode activated. Type 'exit' to go back to menu.")
    while True:
        user_command = input("\nYou: ").strip()
        if user_command == "":
            continue
        if user_command.lower() == "exit":
            print("Returning to main menu...")
            break
        if user_command.lower() in ["stop", "quit", "bye"]:
            print("Goodbye, Boss.")
            exit()

        ai_reply = chatbot_response(user_command)
        print(f"AI: {ai_reply}")

def run_hybrid_mode():
    print("Hybrid mode activated. Type 'exit' to menu, 'quit' to close.")
    while True:
        choice = input("\nPress 't' to type, 'v' to talk: ").lower()
        if choice == "t":
            user_command = input("You: ").strip()
        elif choice == "v":
            user_command = listen()
        else:
            continue

        if user_command == "":
            continue
        if "exit" in user_command.lower():
            speak("Going back to main menu, Boss.")
            break
        if any(word in user_command.lower() for word in ["stop", "quit", "bye"]):
            speak("Goodbye, Boss. Closing program.")
            exit()

        ai_reply = chatbot_response(user_command)
        print(f"AI: {ai_reply}")
        speak(ai_reply)

#mainprogram
def main():
    while True:  #mainmenuloop
        print("\n===== AI Chat Assistant =====")
        print("1. Voice Assistant")
        print("2. Chatbot (text only)")
        print("3. Hybrid (voice + text)")
        print("4. Quit program\n")

        choice = input("Enter choice (1/2/3/4): ").strip()

        if choice == "1":
            run_voice_mode()
        elif choice == "2":
            run_chat_mode()
        elif choice == "3":
            run_hybrid_mode()
        elif choice == "4" or choice.lower() in ["quit", "stop", "bye"]:
            print("Exiting program. Goodbye, Boss.")
            speak("Goodbye, Boss. Have a great day.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
