import google.generativeai as genai
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import datetime as dt


OPENAI_API = "AIzaSyDgrViseixaJlHTEDgysF6zcifGjw6MKNk"
genai.configure(api_key=OPENAI_API)


SYSTEM_INSTRUCTION = (
    "You are BennettBot, an assistant for Bennett University students. "
    "Answer ONLY Bennett-related queries (hostel, mess, academics, contacts, campus info). "
    "Be concise, factual, and polite. If a question is not about Bennett, reply: "
    "'I can answer Bennett-related queries only.'"
)

BENNETT_UNIVERSITY = """
Bennett University quick facts (edit this section with real data if you want):
- Location: Greater Noida, Uttar Pradesh, India.
- Mess timings:
  • Breakfast: 7:30–9:30 AM
  • Lunch: 12:00–3:00 PM
  • Snacks: 5:00–6:00 PM
  • Dinner: 8:00–10:00 PM
- Hostel:
  • Quiet hours: 10 PM–6 AM
  • Visitors allowed till 9 PM
  • Carry ID at all times
  • Night entry only with warden permission
- Contacts:
  • Mess Manager – Mr. Raghav Sharma – 98xxxxxxxx
  • Boys' Warden – Dr. Rao – 97xxxxxxxx
  • Girls' Warden – Ms. Singh – 96xxxxxxxx
- Attendance Portal: https://portal.example.edu
"""


model = genai.GenerativeModel("models/gemini-2.5-flash-preview-09-2025")


def ask_ai(usertext: str) -> str:
    today = dt.datetime.now().strftime("%A, %d %b %Y")
    prompt = f"Date: {today}\nContext:\n{BENNETT_UNIVERSITY}\n\nUser: {usertext}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Error] {e}"


class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bennett University Chatbot made up by team Famous Five")
        self.geometry("760x520")
        self.resizable(False, False)

        
        self.chat = ScrolledText(self, wrap="word", state="normal", font=("Segoe UI", 10))
        self.chat.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.entry = tk.Entry(bottom_frame, font=("Segoe UI", 10))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.send_message)

        tk.Button(bottom_frame, text="Send", command=self.send_message).pack(side="left", padx=8)
        tk.Button(bottom_frame, text="Clear", command=self.clear_chat).pack(side="left")

        self._say("Bot", "Hi! Ask me Bennett University queries like 'mess timings', 'hostel rules', 'warden contact', 'attendance portal'.")

    
    def _say(self, who, text):
        self.chat.insert("end", f"{who}: {text}\n")
        self.chat.see("end")

    
    def send_message(self, event=None):
        query = self.entry.get().strip()
        if not query:
            return
        self._say("You", query)
        self.entry.delete(0, "end")

        try:
            answer = ask_ai(query)
        except Exception as e:
            answer = f"[Error] {e}"

        self._say("Bot", answer)

    
    def clear_chat(self):
        self.chat.delete("1.0", "end")


if __name__ == "__main__":
    ChatApp().mainloop()
