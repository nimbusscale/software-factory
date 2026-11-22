"""A command-line notes tool. Notes are saved in notes.json, next to this script."""

import json
import sys
from pathlib import Path

NOTES_FILE = Path(__file__).with_name("notes.json")


def load():
    if not NOTES_FILE.exists():
        return {"next_id": 1, "notes": []}
    return json.loads(NOTES_FILE.read_text())


def save(data):
    NOTES_FILE.write_text(json.dumps(data, indent=2))


def add(text):
    """Save a new note and print its ID (FR-1, TD-1)."""
    data = load()
    note_id = data["next_id"]
    data["notes"].append({"id": note_id, "text": text})
    data["next_id"] = note_id + 1
    save(data)
    print(note_id)


def list_notes():
    """Print every note with its ID, oldest first (FR-2)."""
    for note in load()["notes"]:
        print(f"{note['id']}: {note['text']}")


def delete(note_id):
    """Remove a note by its ID (FR-3)."""
    data = load()
    kept = [n for n in data["notes"] if n["id"] != note_id]
    if len(kept) == len(data["notes"]):
        print(f"no note {note_id}", file=sys.stderr)
        sys.exit(1)
    data["notes"] = kept
    save(data)


def main(args):
    if len(args) >= 2 and args[0] == "add":
        add(" ".join(args[1:]))
    elif args == ["list"]:
        list_notes()
    elif len(args) == 2 and args[0] == "delete" and args[1].isdigit():
        delete(int(args[1]))
    else:
        print("usage: notes.py add <text> | list | delete <id>", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
