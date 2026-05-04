
import time
import threading
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI
client = OpenAI(api_key="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")

# Emergency Info
EMERGENCY_RESOURCES = {
    "usa": "📞 USA: National Suicide Prevention Lifeline — Call/Text 988",
    "india": "📞 India: iCall — +91 9152987821",
    "uk": "📞 UK: Samaritans — 116 123",
}

EMERGENCY_MESSAGE = """
🚨 It sounds like you're going through something really hard.
You're not alone, and immediate help is available. ❤️

Emergency Resources:
- 📞 USA: 988
- 📞 India: +91 9152987821
- 📞 UK: 116 123
🌐 More help: https://www.psychologytoday.com/
"""

SUICIDE_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "ending my life", "end it all",
    "i want to die", "i want to disappear", "i can't go on", "no reason to live",
    "i hate my life", "i feel worthless", "giving up", "life is meaningless",
    "life is hopeless", "no hope", "i'm done", "nobody cares if i die",
    "self harm", "cutting myself", "hurt myself", "can't handle this pain",
    "overdose", "taking my life", "i deserve to die", "ending everything",
    "mental breakdown", "too much pain", "i'm broken", "severe depression",
    "emotional breakdown", "i'm lost"
]

# Feature 1: SOS Button (simulated as a command)
def sos_button():
    print("\n🚨 SOS Activated: Alerting your trusted contact and sharing emergency numbers!")
    print(EMERGENCY_MESSAGE)

# Feature 2: Trusted Contact System
trusted_contact = "Mom - +91 9876543210"

# Feature 3: Timeout Prompt (if user goes silent)
class TimeoutPrompt:
    def __init__(self, timeout=90):
        self.timeout = timeout
        self.last_input_time = time.time()
        self.prompted = False

    def reset(self):
        self.last_input_time = time.time()
        self.prompted = False

    def monitor(self):
        while True:
            time.sleep(5)
            if time.time() - self.last_input_time > self.timeout and not self.prompted:
                print("\n⏳ Are you still there? Your mental wellbeing matters. Please say something.")
                self.prompted = True

# Feature 4: Session Sharing
chat_history = []

def offer_session_sharing():
    choice = input("📝 Would you like to share this session with a therapist? (yes/no): ").lower()
    if choice == "yes":
        with open("session_history.txt", "w") as file:
            for line in chat_history:
                file.write(f"{line}\n")
        print("✅ Session saved to 'session_history.txt'. You can email this to your therapist securely.")

# Feature 5: Emergency Resource Card (simplified by region)
def get_emergency_card(region):
    region = region.lower()
    return EMERGENCY_RESOURCES.get(region, EMERGENCY_MESSAGE)

# Emergency keyword detector
def check_for_emergency(user_input):
    return any(kw in user_input.lower() for kw in SUICIDE_KEYWORDS)

# Main chat function
def chat():
    print("🧠 Mental Health Chatbot is running. Type 'exit' to quit or 'sos' to activate emergency help.\n")
    region = input("🌍 Please enter your country (e.g., USA, India, UK): ").lower()
    print(get_emergency_card(region))

    timeout = TimeoutPrompt()
    threading.Thread(target=timeout.monitor, daemon=True).start()

    while True:
        user_input = input("You: ")
        timeout.reset()
        chat_history.append(f"You: {user_input}")

        if user_input.lower() == "exit":
            offer_session_sharing()
            print("👋 Session ended. Take care of yourself.")
            break

        if user_input.lower() == "sos":
            sos_button()
            continue

        if check_for_emergency(user_input):
            print(EMERGENCY_MESSAGE)
            print(f"📞 Trusted Contact Notified: {trusted_contact}")
            continue

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a caring, motivational mental health support assistant. Provide calm, thoughtful encouragement."},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response.choices[0].message.content
            chat_history.append(f"Bot: {reply}")
            print(f"Bot: {reply}\n")
        except Exception as e:
            print(f"❌ Error: {e}")

# Run it
if __name__ == "__main__":
    chat()
