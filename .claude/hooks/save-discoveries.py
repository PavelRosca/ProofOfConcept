"""
Claude Code Stop hook — maintains a clean discoveries.md.
- Extracts the last assistant text from transcript
- Uses Claude API to generate a concise note (3-5 bullet points max)
- Skips if response has no technical content
- Deduplicates: if a similar topic exists, updates it instead of adding again
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DISCOVERIES_PATH = Path("E:/Desktop/WEBDevP/ProofOfConcept/.claude/discoveries.md")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

KEYWORDS = [
    'fix', 'error', 'bug', 'issue', 'problem', 'solution', 'cause',
    'migration', 'deploy', 'render', 'config', 'setting', 'install',
    'found', 'discover', 'broken', 'fail', 'crash', 'works', 'warning',
    'treebeard', 'wagtail', 'django', 'python', 'postgres', 'database',
]


def get_last_assistant_text(transcript_path: str) -> str:
    try:
        path = Path(transcript_path)
        if not path.exists():
            return ""
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return ""

    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        role = obj.get("role") or obj.get("type", "")
        content = obj.get("content") or (obj.get("message") or {}).get("content", "")

        if role != "assistant":
            continue

        texts = []
        if isinstance(content, str):
            texts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    texts.append(block.get("text", ""))

        text = "\n".join(t for t in texts if t).strip()
        if text:
            return text

    return ""


def is_relevant(text: str) -> bool:
    if len(text) < 200:
        return False
    lower = text.lower()
    return sum(1 for kw in KEYWORDS if kw in lower) >= 2 or "```" in text


def call_claude(text: str) -> str:
    """Ask Claude to extract a concise discovery note (3-5 bullets, no fluff)."""
    if not ANTHROPIC_API_KEY:
        return ""
    try:
        import urllib.request
        payload = json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 300,
            "messages": [{
                "role": "user",
                "content": (
                    "From the assistant response below, extract ONLY genuinely new technical facts "
                    "worth remembering (bugs found, fixes applied, configs discovered, architecture decisions). "
                    "Write 2-4 bullet points, max 15 words each. "
                    "If nothing new or noteworthy, reply with exactly: SKIP\n\n"
                    f"---\n{text[:3000]}"
                )
            }]
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"].strip()
    except Exception:
        return ""


def load_discoveries() -> str:
    if DISCOVERIES_PATH.exists():
        return DISCOVERIES_PATH.read_text(encoding="utf-8")
    return "# Claude Discoveries — ProofOfConcept\n\n---\n"


def already_noted(content: str, note: str) -> bool:
    """True if the first bullet of the note already appears in content (fuzzy)."""
    first_line = next((ln.strip("- •").strip() for ln in note.splitlines() if ln.strip()), "")
    if len(first_line) < 10:
        return False
    # Simple word-overlap check
    words = set(first_line.lower().split())
    for line in content.splitlines():
        overlap = words & set(line.lower().split())
        if len(overlap) >= min(4, len(words) // 2):
            return True
    return False


def append_entry(note: str) -> None:
    content = load_discoveries()
    if already_noted(content, note):
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n## {timestamp}\n\n{note}\n\n---\n"
    DISCOVERIES_PATH.write_text(content + entry, encoding="utf-8")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    transcript_path = data.get("transcript_path", "")
    text = get_last_assistant_text(transcript_path)

    if not text or not is_relevant(text):
        return

    note = call_claude(text)

    if not note or note.strip().upper() == "SKIP":
        return

    append_entry(note)


if __name__ == "__main__":
    main()
