"""
J.A.R.V.I.S. Voice System
---------------------------
Paul Bettany's JARVIS voice via ElevenLabs.
Falls back to macOS Daniel voice if no API key.

Human element:
- Lower stability (0.35) = natural variation, not robotic
- Style boost (0.25) = subtle expressiveness
- Sentence-aware pacing with real pauses
- Emphasis on key words via SSML-style breaks

Usage:
    from systems.voice import speak
    speak("All systems online, sir.")
"""

import os
import subprocess
import tempfile
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# ElevenLabs config
ELEVENLABS_API_KEY  = os.environ.get("ELEVENLABS_API_KEY", "")
JARVIS_VOICE_ID     = "WWtyH2oxeOp9yZwK8ERD"   # ElevenLabs JARVIS (Paul Bettany)
ELEVENLABS_API_URL  = f"https://api.elevenlabs.io/v1/text-to-speech/{JARVIS_VOICE_ID}"

# Voice settings — tuned for human JARVIS feel
VOICE_SETTINGS = {
    "stability":          0.38,   # Lower = more natural variation (not robotic)
    "similarity_boost":   0.78,   # High = stays close to Paul Bettany's voice
    "style":              0.25,   # Subtle expressiveness — not overdone
    "use_speaker_boost":  True,   # Enhances clarity
}

# macOS fallback
MACOS_VOICE = "Daniel"
MACOS_RATE  = 162   # Words per minute — Paul Bettany speaks ~155-170 wpm as JARVIS


def _add_human_pauses(text: str) -> str:
    """
    Add natural pauses and pacing to text before speaking.
    Replicates how JARVIS actually delivers lines — not monotone.
    """
    # Pause after "sir" — signature JARVIS beat
    text = re.sub(r"\bsir\b([,.]?)", r"sir\1", text)

    # Slight pause before key phrases
    for phrase in ["I've taken the liberty", "Shall I", "With respect",
                   "I would advise", "I should note", "Might I suggest"]:
        text = text.replace(phrase, f"... {phrase}")

    # Ensure ellipses become real pauses
    text = text.replace("...", " ... ")

    # Clean up multiple spaces
    text = re.sub(r"  +", " ", text).strip()

    return text


def _speak_elevenlabs(text: str) -> bool:
    """Speak using ElevenLabs JARVIS voice. Returns True if successful."""
    try:
        import urllib.request
        import urllib.error
        import json as _json

        payload = _json.dumps({
            "text":           _add_human_pauses(text),
            "model_id":       "eleven_turbo_v2_5",
            "voice_settings": VOICE_SETTINGS,
        }).encode("utf-8")

        req = urllib.request.Request(
            ELEVENLABS_API_URL,
            data=payload,
            headers={
                "xi-api-key":    ELEVENLABS_API_KEY,
                "Content-Type":  "application/json",
                "Accept":        "audio/mpeg",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            audio_data = resp.read()

        # Write to temp file and play
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name

        subprocess.run(["afplay", tmp_path], check=True)
        os.unlink(tmp_path)
        return True

    except Exception:
        return False


def _speak_macos(text: str):
    """Fallback: macOS say with Daniel (British) voice."""
    clean = _add_human_pauses(text)
    # macOS say interprets [[...]] as embedded speech commands
    # Add subtle pitch modulation for human feel
    cmd = ["say", "-v", MACOS_VOICE, "-r", str(MACOS_RATE), clean]
    subprocess.run(cmd)


def speak(text: str, force_local: bool = False):
    """
    Speak text as JARVIS.

    Uses ElevenLabs (Paul Bettany voice) if API key is set.
    Falls back to macOS Daniel voice otherwise.
    """
    if not text or not text.strip():
        return

    if ELEVENLABS_API_KEY and not force_local:
        success = _speak_elevenlabs(text)
        if success:
            return

    _speak_macos(text)


def speak_briefing(lines: list):
    """Speak a multi-line briefing with natural pauses between sections."""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip decorative lines
        if all(c in "━─═╔╗╚╝║│ " for c in line):
            continue
        # Strip JARVIS prefix for TTS
        for prefix in ["  JARVIS │ ", "  ⚠ ALERT │ ", "  ◈ INSIGHT │ ",
                       "  ↺ ADVISORY │ ", "  ✓ CONFIRMED │ ", "  ✖ PRIORITY │ "]:
            if line.startswith(prefix):
                line = line[len(prefix):]
                break
        if line.strip():
            speak(line.strip())


def set_api_key(key: str):
    """Set ElevenLabs API key at runtime."""
    global ELEVENLABS_API_KEY
    ELEVENLABS_API_KEY = key


def is_elevenlabs_configured() -> bool:
    return bool(ELEVENLABS_API_KEY)
