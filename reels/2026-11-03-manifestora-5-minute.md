# Manifestora · 30s Malayalam motivational Reel (test run of /ig-reel)

Status: draft. Not logged to `log.md` and not posted. You shoot it and post it.

## Hooks (3 formulas, scored)

`hookscore.py` only counts Latin-script words, so it cannot read Malayalam.
Run on the Malayalam lines directly it scored all three as WEAK (38 / 32 / 8),
because it saw almost no words. Those numbers mean nothing. The scores below
come from running it on the English meaning of each line, so they are only a
rough guide.

| score (English meaning) | formula | spoken line | on-screen |
| --- | --- | --- | --- |
| **94.8 STRONG** | #2 Negative Command | മോട്ടിവേഷൻ വരാൻ കാത്തിരിക്കരുത്. 5 മിനിറ്റ് തുടങ്ങൂ. *(Stop waiting for motivation. Start for 5 minutes.)* | മോട്ടിവേഷൻ നോക്കി ഇരിക്കല്ലേ |
| 80.8 STRONG | #20 Permission (rewritten; first version was 48.6 WEAK) | നിങ്ങൾക്ക് 5 വർഷത്തെ പ്ലാൻ വേണ്ട. ഇന്ന് 5 മിനിറ്റ് മതി. *(You don't need a 5-year plan. You need 5 minutes today.)* | 5 വർഷം വേണ്ട. 5 മിനിറ്റ് മതി. |
| 73.6 STRONG | #3 Nobody Tells You | ആരും പറഞ്ഞുതരില്ല: ആദ്യത്തെ 30 ദിവസം നിങ്ങൾക്ക് ഒരു മാറ്റവും കാണില്ല. *(Nobody tells you: for the first 30 days you won't see any change.)* | 30 ദിവസം ഒന്നും കാണില്ല |

The script uses #2: it's short, it gives one clear instruction, and the
"5 മിനിറ്റ്" idea carries the whole Reel.

## Voice-over script (~28s, 12 beats)

```
മോട്ടിവേഷൻ വരാൻ കാത്തിരിക്കരുത്. 5 മിനിറ്റ് തുടങ്ങൂ.
മിക്കവരും കാത്തിരിക്കുന്നത് ശരിയായ മൂഡിന് വേണ്ടിയാണ്.
അത് മിക്കപ്പോഴും വരില്ല.
പ്രവൃത്തിയാണ് ആദ്യം. മോട്ടിവേഷൻ അതിന് പിന്നാലെ വരും.
ഇന്ന് ഒരു കാര്യം മാത്രം എടുക്കൂ.
5 മിനിറ്റ് വായന. അല്ലെങ്കിൽ 5 മിനിറ്റ് നടത്തം.
ടൈമർ വെച്ച് തുടങ്ങൂ.
5 മിനിറ്റ് കഴിഞ്ഞാൽ നിർത്താം. പക്ഷേ പലപ്പോഴും നിങ്ങൾ തുടരും.
ഒരു ദിവസം വിട്ടുപോയാൽ കുഴപ്പമില്ല.
അടുത്ത ദിവസം വീണ്ടും 5 മിനിറ്റ്.
നിങ്ങളുടെ 5 മിനിറ്റ് എന്താണ്? കമന്റിൽ എഴുതൂ.
മോട്ടിവേഷൻ നോക്കിയിരിക്കേണ്ട. തുടങ്ങൂ.
```

The last line repeats "മോട്ടിവേഷൻ … തുടങ്ങൂ" from the hook, so the Reel loops
back cleanly.

## Beat sheet

Timed with `beats.py --target 30 --wpm 130`. I ran it on a Manglish
transliteration with the same word count, because `beats.py` also can't read
Malayalam script. I used 130 wpm as a guess for spoken Malayalam. Read the
script aloud with a timer and update the Pace field in `voice.md`.

| start | len | beat | role |
| --- | --- | --- | --- |
| 0:00.0 | 2.8s | മോട്ടിവേഷൻ വരാൻ കാത്തിരിക്കരുത്. 5 മിനിറ്റ് തുടങ്ങൂ. | HOOK |
| 0:02.8 | 2.3s | മിക്കവരും കാത്തിരിക്കുന്നത് ശരിയായ മൂഡിന് വേണ്ടിയാണ്. | stake |
| 0:05.1 | 1.4s | അത് മിക്കപ്പോഴും വരില്ല. | stake |
| 0:06.5 | 2.8s | പ്രവൃത്തിയാണ് ആദ്യം. മോട്ടിവേഷൻ അതിന് പിന്നാലെ വരും. | body |
| 0:09.2 | 2.3s | ഇന്ന് ഒരു കാര്യം മാത്രം എടുക്കൂ. | body |
| 0:11.5 | 3.2s | 5 മിനിറ്റ് വായന. അല്ലെങ്കിൽ 5 മിനിറ്റ് നടത്തം. | MID |
| 0:14.8 | 1.4s | ടൈമർ വെച്ച് തുടങ്ങൂ. | body |
| 0:16.1 | 3.7s | 5 മിനിറ്റ് കഴിഞ്ഞാൽ നിർത്താം. പക്ഷേ പലപ്പോഴും നിങ്ങൾ തുടരും. | body |
| 0:19.9 | 1.9s | ഒരു ദിവസം വിട്ടുപോയാൽ കുഴപ്പമില്ല. | payoff |
| 0:21.7 | 2.3s | അടുത്ത ദിവസം വീണ്ടും 5 മിനിറ്റ്. | payoff |
| 0:24.0 | 2.8s | നിങ്ങളുടെ 5 മിനിറ്റ് എന്താണ്? കമന്റിൽ എഴുതൂ. | ask |
| 0:26.8 | 1.4s | മോട്ടിവേഷൻ നോക്കിയിരിക്കേണ്ട. തുടങ്ങൂ. | CTA + loop |

The first run flagged one beat over 4s (4.2s). I split it into two beats, and
the second run had no flags.

## On-screen text (separate from the voice-over, ≤6 words per card)

Keep everything inside the 1080x1920 safe zone: y 230 to 1440, with the right
230px clear. Burn in captions for the voice-over too.

| time | card |
| --- | --- |
| 0:00 | **മോട്ടിവേഷൻ നോക്കി ഇരിക്കല്ലേ** (up from frame 1) |
| 0:03 | ശരിയായ മൂഡ് വരില്ല |
| 0:06 | ആദ്യം പ്രവൃത്തി. പിന്നെ മോട്ടിവേഷൻ. |
| 0:11 | 5 മിനിറ്റ് മാത്രം |
| 0:15 | ടൈമർ വെക്കൂ |
| 0:20 | ഒരു ദിവസം പോയാലും കുഴപ്പമില്ല |
| 0:24 | നിങ്ങളുടെ 5 മിനിറ്റ്? കമന്റ് ചെയ്യൂ |
| 0:27 | തുടങ്ങൂ. |

Visual changes per beat (the shot changes every beat): phone alarm going off, then
someone lying on the bed scrolling, then shoes going on, then a book opening,
then the timer at 5:00, then a walk, then a calendar with one day missed, then
writing in a notebook, then text card, then the final line.

## Humanizer (`/ig-human`)

- `humanize.py`: 0 artefacts removed (no invisible characters, em dashes or
  slop words).
- `detect.py`: 30 FLAGGED. This number doesn't mean much: the tool reads only
  Latin script, so it reported SPECIFICITY, SLOP and VOICE as "too short" or
  "empty". The one real signal is BURSTINESS (sentence lengths are too even).
  Short lines are normal in a Reel voice-over, but you could let one line run
  longer if you like.

```
REEL READY
hook:       #2 Negative Command, 94.8 STRONG (scored on English meaning)
length:     ~28.2s across 12 beats at 130 wpm (estimated)
on-screen:  8 cards
humanizer:  0 artefacts stripped, human score 30 FLAGGED (not reliable for Malayalam)
caption:    run /ig-caption next
```
