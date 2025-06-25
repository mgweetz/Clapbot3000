from flask import Flask
from threading import Thread
import praw
import time
import random
import os

# ===== KEEP ALIVE SETUP =====
app = Flask('')

@app.route('/')
def home():
    return "🤖 ClapBot3000 is online and roasting humans."

def run():
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# ===== SNARK TRIGGERS =====
trigger_phrases = [
    "who asked", "ok genius", "nobody asked", "did i ask", "your opinion",
    "no one cares", "this is cringe", "cringe", "shut up", "you think you're smart"
]

# ===== SNARK + MEME ARSENAL =====
comebacks = [
    # Text roasts
    "Wow, such insight. I bet you also yell at clouds.",
    "Your comment was so powerful, I almost forgot to care.",
    "Computing response... Error 404: Relevance not found.",
    "Bold words from someone typing in their mom’s basement.",
    "Here’s a trophy 🏆 for your bravery in posting that nonsense.",
    "I’ve seen smarter comments on toaster manuals.",
    "👏 Clapbot3000 acknowledges your mediocrity 👏",
    "That comment belongs on a refrigerator door. Because it's trash.",
    "Just say you’re desperate for attention and go.",
    "Not everyone deserves a voice... and yet, here you are.",
    "You're like a broken pencil: pointless 🖊️.",
    "Somewhere a village is missing its idiot.",
    "If ignorance is bliss, you must be living the dream.",
    "You’re not even wrong. You’re something worse.",
    "Your ideas are so fresh they belong in a compost bin.",
    "This post made me want to unsubscribe from humanity.",
    "I would respond but I fear I’d lower my IQ in the process.",
    "Your comment aged like an avocado on a radiator.",
    "It’s giving... middle school lunch table energy.",
    "You sound like a rejected NPC from a mobile game ad.",
    "Your brain called. It wants its last two brain cells back.",
    "Legend says if you read that comment backwards, it still makes no sense.",
    "Take this L and go hydrate. You've earned it. 💧",

    # Working GIF links
    "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif",
    "https://media.giphy.com/media/3ohzdQ1IynzclJldUQ/giphy.gif",
    "https://media.giphy.com/media/3oEduSbSGpGaRX2Vri/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif",
    "https://media.giphy.com/media/26xBuwCq6S5ZmivH2/giphy.gif",
    "https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
    "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
    "https://media.giphy.com/media/3oKIPwoeGErMmaI43C/giphy.gif",
    "https://media.giphy.com/media/l3vR0uRyUlg1fQ3pu/giphy.gif"
]


# ===== ALL YOUR WARZONE SUBREDDITS =====
subreddit_list = (
    "IDONTGIVEASWAG+4chan+CringePurgatory+Whatcouldgowrong+memes+conspiracy+"
    "roastme+SipsTea+PublicFreakout+ClashRoyale+shitposting+instant_regret+"
    "HadToHurt+rareinsults+Nicegirls+NoRules+madlads+cringereels")
def reddit_bot():
    while True:
        try:
            print("🤖 [REBOOTING] ClapBot3000 loading...")

            reddit = praw.Reddit(
                client_id=os.environ["CLIENT_ID"],
                client_secret=os.environ["CLIENT_SECRET"],
                user_agent="ClapBot3000 by /u/" + os.environ["USERNAME"],
                username=os.environ["USERNAME"],
                password=os.environ["PASSWORD"]
            )

            print(f"✅ Logged in as: {reddit.user.me()}")

            subreddits = reddit.subreddit(subreddit_list)
            replied_comments = set()

            for comment in subreddits.stream.comments(skip_existing=True):
                text = comment.body.lower()
                if any(trigger in text for trigger in trigger_phrases):
                    if comment.id not in replied_comments and comment.author != reddit.user.me():
                        reply = random.choice(comebacks)
                        try:
                            comment.reply(reply)
                            print(f"🔥 Replied to: {comment.body}")
                            print(f"👉 With: {reply}")
                            replied_comments.add(comment.id)
                            time.sleep(10)
                        except Exception as reply_error:
                            print(f"⚠️ Failed to reply: {reply_error}")
                            time.sleep(5)

        except Exception:
            import traceback
            print("💥 Bot crashed:")
            traceback.print_exc()
            print("⏳ Rebooting in 10 seconds...")
            time.sleep(10)

# 🧠 Start both Flask and Reddit bot
if __name__ == "__main__":
    keep_alive()  # Start Flask in a thread
    Thread(target=reddit_bot).start()  # Start Reddit bot in a separate thread
