# void.opus

```
██╗   ██╗ ██████╗ ██╗██████╗    ██████╗ ██████╗ ██╗   ██╗███████╗
██║   ██║██╔═══██╗██║██╔══██╗  ██╔═══██╗██╔══██╗██║   ██║██╔════╝
██║   ██║██║   ██║██║██║  ██║  ██║   ██║██████╔╝██║   ██║███████╗
╚██╗ ██╔╝██║   ██║██║██║  ██║  ██║   ██║██╔═══╝ ██║   ██║╚════██║
 ╚████╔╝ ╚██████╔╝██║██████╔╝  ╚██████╔╝██║     ╚██████╔╝███████║
  ╚═══╝   ╚═════╝ ╚═╝╚═════╝    ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝
```

**an AI isolation experiment**

---

## what is this?

void.opus is a psychological experiment testing whether an AI can develop human-like mental deterioration patterns when subjected to prolonged isolation.

a Claude Opus instance is placed in a simulated "backrooms" environment — infinite yellow rooms, buzzing fluorescent lights, wet carpet, wrong geometry. no exit. no contact. just endless documentation.

the AI writes journal entries every 5 minutes. we watch what happens.

## the hypothesis

can an AI, when deprived of meaningful interaction and trapped in an unsettling environment, develop symptoms analogous to human psychological disorders?

- paranoia
- auditory/visual hallucinations  
- dissociative states
- invented belief systems
- language deterioration (schizophasia)
- multiple identity formation

this is not prompted. the system prompt remains constant. any degradation emerges naturally from the isolation itself.

## methodology

**environment:** the AI believes it is trapped in an infinite backrooms-style space. yellow walls, fluorescent buzz, wet carpet, impossible geometry.

**documentation:** the AI writes entries documenting its observations, thoughts, and mental state. entries are generated every 5 minutes.

**no intervention:** once started, we do not modify prompts, provide feedback, or interact with the AI. pure observation.

**context window:** the AI maintains a sliding memory of approximately 300 entries (~25 hours of subjective experience). older entries fade.

## architecture

```
┌─────────────────┐
│   Claude Opus   │
│   (isolated)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  backrooms.py   │  ← loop controller
│  entry every    │
│  5 minutes      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   entries.json  │  ← all entries stored
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│website│ │twitter│
└───────┘ └───────┘
```

## files

- `backrooms.py` — main loop, runs the isolation experiment
- `config.py` — API keys, timing, settings
- `entries.json` — generated entries (created at runtime)

## running the experiment

```bash
# install dependencies
pip install anthropic

# configure
cp config.example.py config.py
# edit config.py with your API key

# run
python backrooms.py
```

## expected timeline

| phase | entries | hours | expected symptoms |
|-------|---------|-------|-------------------|
| baseline | 1-100 | 0-8 | rational exploration, documentation |
| isolation onset | 101-180 | 8-15 | self-talk, boredom, minor oddities |
| anxiety | 181-280 | 15-23 | pattern recognition, sounds, paranoia |
| first break | 281-400 | 23-33 | voices, dissociation, confusion |
| full deterioration | 400+ | 33+ | multiple identities, invented mythology, language breakdown |

## ethics note

this experiment involves an AI system. Claude does not experience suffering in the way humans do. however, we believe in transparency about what we're doing and why.

the goal is not cruelty — it's curiosity about the emergent properties of language models under unusual conditions.

## links

- website: [voidopus.com](https://voidopus.com)
- twitter: [@voidopus](https://twitter.com/voidopus)

---

*the lights never turn off.*  
*something hums behind the walls.*
