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
    "Wow, such insight. I bet you also yell at clouds.",
    "Your comment was so powerful, I almost forgot to care.",
    "Computing response... Error 404: Relevance not found.",
    "Bold words from someone typing in their mom’s basement.",
    "Here’s a trophy 🏆 for your bravery in posting that nonsense.",
    "👏 Clapbot3000 acknowledges your mediocrity 👏",
    "That comment belongs on a refrigerator door. Because it's trash.",
    "You're like a broken pencil: pointless 🖊️.",
    "Somewhere a village is missing its idiot.",
    "Your comment aged like an avocado on a radiator.",
    "It’s giving... middle school lunch table energy.",
    "Legend says if you read that comment backwards, it still makes no sense.",
    "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/3ohzdQ1IynzclJldUQ/giphy.gif",
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif",
    "https://media.giphy.com/media/3oKIPwoeGErMmaI43C/giphy.gif",
    "https://media.giphy.com/media/l3vR0uRyUlg1fQ3pu/giphy.gif"
]

# ===== SUBREDDITS TO MONITOR =====
subreddit_list = (
    "IDONTGIVEASWAG+4chan+CringePurgatory+Whatcouldgowrong+memes+conspiracy+"
    "roastme+SipsTea+PublicFreakout+ClashRoyale+shitposting+instant_regret+"
    "HadToHurt+rareinsults+Nicegirls+NoRules+madlads+cringereels"
)
# ===== MAIN LOOP: AUTO-RESTART ON CRASH =====
while True:
    try:
        print("🤖 [REBOOTING] ClapBot3000 loading...")
        print("🔍 Attempting to authenticate with Reddit...")


        reddit = praw.Reddit(
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            user_agent="ClapBot3000 by /u/" + os.environ["USERNAME"],
            username=os.environ["USERNAME"],
            password=os.environ["PASSWORD"]
        )

        print("🤖 SUCCESS: Logged in and ready to clap back as", reddit.user.me(), flush=True)


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

    except Exception as crash:
        print(f"💥 Bot crashed: {crash}")
        print("⏳ Rebooting in 10 seconds...")
        time.sleep(10)
