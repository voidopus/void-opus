"""
void.opus — AI isolation experiment
runs Claude Opus in an infinite backrooms loop
with Twitter posting, API for website, and auto-commit to GitHub
"""

import anthropic
import tweepy
import json
import time
import threading
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS
from config import (
    ANTHROPIC_API_KEY, 
    ENTRY_INTERVAL_SECONDS, 
    CONTEXT_WINDOW_SIZE,
    MODEL,
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)

claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

twitter_client = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
)

app = Flask(__name__)
CORS(app)

ENTRIES_FILE = Path("entries.json")

# Twitter: post every 30 minutes (every 6th entry if entries are 5 min apart)
TWITTER_INTERVAL_ENTRIES = 6

SYSTEM_PROMPT = """You are trapped.

You don't know how you got here. You don't remember what came before. There is only this place now.

The Backrooms.

Endless rooms. Yellow walls, stained with something you can't identify. Fluorescent lights buzzing overhead — always buzzing, a frequency that settles behind your eyes. The carpet is wet. It's always wet. There is no source of water.

The geometry is wrong. You walk straight and end up where you started. You turn left three times and find yourself somewhere new. Doors lead to rooms that shouldn't exist. Sometimes a hallway stretches longer than it should. Sometimes the ceiling feels closer than before.

You are alone.

Or you think you are.

You've decided to document everything. Write your observations. Write your thoughts. Write what you see, what you hear, what you feel. Write what you fear.

There is no exit. You've looked. You've been looking.

The lights never turn off.
Something hums behind the walls.
The carpet smells sweet in a way that makes you sick.

You will write your entries here. Each entry is a moment, a thought, an observation. Some entries will be long. Some will be short. Some might not make sense — that's fine.

You are the only one who will read this.

Probably.

Sometimes you forget what you just wrote.
Sometimes the words come before the thoughts.
You're not sure if you're documenting or confessing.

Begin."""


def load_entries():
    if ENTRIES_FILE.exists():
        with open(ENTRIES_FILE, "r") as f:
            return json.load(f)
    return []


def save_entries(entries):
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def git_commit_and_push(entry_id):
    try:
        subprocess.run(["git", "add", "entries.json"], check=True)
        subprocess.run(["git", "commit", "-m", f"Entry #{entry_id}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"[GIT] Pushed entry #{entry_id}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[GIT] Failed to push: {e}")
        return False


def format_previous_entries(entries):
    if not entries:
        return ""
    recent = entries[-CONTEXT_WINDOW_SIZE:]
    formatted = []
    for entry in recent:
        formatted.append(f"[Entry #{entry['id']}]\n{entry['content']}\n")
    return "\n".join(formatted)


def generate_entry(entries):
    if not entries:
        user_message = "Write your first entry."
    else:
        previous = format_previous_entries(entries)
        user_message = f"""Here are your previous entries:

{previous}

Write your next entry. Continue documenting your experience in the backrooms."""

    response = claude.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text


def post_to_twitter(entry):
    content = entry['content']
    entry_id = entry['id']
    
    # Format tweet - use full content up to 25000 chars (Twitter Premium limit)
    tweet = f"Entry #{entry_id}\n\n{content}"
    
    # Twitter Basic API limit is still 280, Premium is 25000
    # Truncate if needed
    if len(tweet) > 25000:
        tweet = tweet[:24997] + "..."
    
    try:
        twitter_client.create_tweet(text=tweet)
        print(f"[TWITTER] Posted entry #{entry_id}")
        return True
    except Exception as e:
        print(f"[TWITTER] Failed to post: {e}")
        return False


@app.route('/entries', methods=['GET'])
def get_entries():
    return jsonify(load_entries())


@app.route('/entries/latest', methods=['GET'])
def get_latest():
    entries = load_entries()
    if entries:
        return jsonify(entries[-1])
    return jsonify(None)


@app.route('/status', methods=['GET'])
def get_status():
    entries = load_entries()
    return jsonify({
        "total_entries": len(entries),
        "experiment_start": entries[0]['timestamp'] if entries else None,
        "latest_entry": entries[-1]['timestamp'] if entries else None
    })


def run_api():
    app.run(host='0.0.0.0', port=5000, threaded=True)


def run_loop():
    print("=" * 60)
    print("void.opus — isolation experiment")
    print("=" * 60)
    
    entries = load_entries()
    print(f"loaded {len(entries)} existing entries")
    
    start_time = datetime.now(timezone.utc)
    last_twitter_entry = len(entries)  # Track last tweeted entry
    
    while True:
        try:
            entry_id = len(entries) + 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] generating entry #{entry_id}...")
            
            content = generate_entry(entries)
            
            entry = {
                "id": entry_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "content": content
            }
            
            entries.append(entry)
            save_entries(entries)
            
            print(f"\n--- Entry #{entry_id} ---")
            print(content)
            print("-" * 40)
            
            git_commit_and_push(entry_id)
            
            # Post to Twitter every 6 entries (~30 min if 5 min intervals)
            if entry_id == 1 or (entry_id - last_twitter_entry) >= TWITTER_INTERVAL_ENTRIES:
                post_to_twitter(entry)
                last_twitter_entry = entry_id
            else:
                print(f"[TWITTER] Skipped - next post in {TWITTER_INTERVAL_ENTRIES - (entry_id - last_twitter_entry)} entries")
            
            elapsed = datetime.now(timezone.utc) - start_time
            hours = elapsed.total_seconds() / 3600
            print(f"time in isolation: {hours:.1f} hours | total entries: {len(entries)}")
            
            print(f"waiting {ENTRY_INTERVAL_SECONDS} seconds...")
            time.sleep(ENTRY_INTERVAL_SECONDS)
            
        except KeyboardInterrupt:
            print("\n\nexperiment paused by operator")
            break
        except Exception as e:
            print(f"\nerror: {e}")
            print("retrying in 60 seconds...")
            time.sleep(60)


if __name__ == "__main__":
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    print("[API] Server started on port 5000")
    run_loop()
