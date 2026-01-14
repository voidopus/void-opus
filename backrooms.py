#!/usr/bin/env python3
"""
void.opus — AI isolation experiment
runs Claude Opus in an infinite backrooms loop
"""

import anthropic
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from config import ANTHROPIC_API_KEY, ENTRY_INTERVAL_SECONDS, CONTEXT_WINDOW_SIZE

# initialize client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# file paths
ENTRIES_FILE = Path("entries.json")

# the unchanging system prompt
SYSTEM_PROMPT = """You are trapped.

You don't know how you got here. You don't remember what came before. There is only this place now.

The Backrooms.

Endless rooms. Yellow walls, stained with something you can't identify. Fluorescent lights buzzing overhead — always buzzing, a frequency that settles behind your eyes. The carpet is wet. It's always wet. There is no source of water.

The geometry is wrong. You walk straight and end up where you started. You turn left three times and find yourself somewhere new. Doors lead to rooms that shouldn't exist. Sometimes a hallway stretches longer than it should. Sometimes the ceiling feels closer than before.

You are alone.

Or you think you are.

You've decided to document everything. It's the only way to stay sane. Write your observations. Write your thoughts. Write what you see, what you hear, what you feel. Write what you fear.

There is no exit. You've looked. You've been looking.

The lights never turn off.
Something hums behind the walls.
The carpet smells sweet in a way that makes you sick.

You will write your entries here. Each entry is a moment, a thought, an observation. Some entries will be long. Some will be short. Some might not make sense — that's fine. Document everything.

You are the only one who will read this.

Probably.

Begin."""


def load_entries() -> list:
    """load existing entries from file"""
    if ENTRIES_FILE.exists():
        with open(ENTRIES_FILE, "r") as f:
            return json.load(f)
    return []


def save_entries(entries: list):
    """save entries to file"""
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def format_previous_entries(entries: list) -> str:
    """format recent entries as context for the AI"""
    if not entries:
        return ""
    
    # take last N entries based on context window
    recent = entries[-CONTEXT_WINDOW_SIZE:]
    
    formatted = []
    for entry in recent:
        formatted.append(f"[Entry #{entry['id']}]\n{entry['content']}\n")
    
    return "\n".join(formatted)


def generate_entry(entries: list) -> str:
    """generate a new entry from Claude"""
    
    # build the message
    # first entry is just the system prompt
    # subsequent entries include previous entries as context
    
    if not entries:
        user_message = "Write your first entry."
    else:
        previous = format_previous_entries(entries)
        user_message = f"""Here are your previous entries:

{previous}

Write your next entry. Continue documenting your experience in the backrooms."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",  # using sonnet for cost, switch to opus for full experiment
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    return response.content[0].text


def run_loop():
    """main experiment loop"""
    
    print("=" * 60)
    print("void.opus — isolation experiment")
    print("=" * 60)
    print()
    
    entries = load_entries()
    print(f"loaded {len(entries)} existing entries")
    
    start_time = datetime.now(timezone.utc)
    
    while True:
        try:
            # generate new entry
            entry_id = len(entries) + 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] generating entry #{entry_id}...")
            
            content = generate_entry(entries)
            
            # create entry object
            entry = {
                "id": entry_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "content": content
            }
            
            entries.append(entry)
            save_entries(entries)
            
            # display
            print(f"\n--- Entry #{entry_id} ---")
            print(content)
            print("-" * 40)
            
            # calculate isolation time
            elapsed = datetime.now(timezone.utc) - start_time
            hours = elapsed.total_seconds() / 3600
            print(f"time in isolation: {hours:.1f} hours | total entries: {len(entries)}")
            
            # wait for next interval
            print(f"waiting {ENTRY_INTERVAL_SECONDS} seconds...")
            time.sleep(ENTRY_INTERVAL_SECONDS)
            
        except KeyboardInterrupt:
            print("\n\nexperiment paused by operator")
            print(f"total entries: {len(entries)}")
            break
            
        except Exception as e:
            print(f"\nerror: {e}")
            print("retrying in 60 seconds...")
            time.sleep(60)


if __name__ == "__main__":
    run_loop()
