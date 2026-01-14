# void.opus configuration
# copy this to config.py and fill in your values

# Anthropic API key
ANTHROPIC_API_KEY = "your-api-key-here"

# how often to generate entries (in seconds)
# 300 = 5 minutes (recommended)
# 60 = 1 minute (for testing)
ENTRY_INTERVAL_SECONDS = 300

# how many previous entries to include as context
# 300 entries ≈ 25 hours of memory
# higher = more continuity but higher API costs
CONTEXT_WINDOW_SIZE = 300

# model to use
# "claude-sonnet-4-20250514" — cheaper, good for testing
# "claude-opus-4-5-20251101" — full experiment, more expensive
MODEL = "claude-sonnet-4-20250514"
