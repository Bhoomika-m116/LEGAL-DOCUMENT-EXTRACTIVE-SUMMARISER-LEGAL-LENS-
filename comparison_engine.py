"""Text-based clause comparison for LegalLens.

This module compares clause text directly. It deliberately does not use the
summarizer's extracted category names as a proxy for clause equality.
"""
import re
from difflib import SequenceMatcher


def _split_clauses(text):
    """Split a contract into reasonably-sized clause units while preserving text."""
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    # First respect paragraph and numbered-clause boundaries, then sentence ends.
    units = []
    for paragraph in re.split(r"\n\s*\n|\n(?=\s*(?:\d+(?:\.\d+)*[.)]|(?:\([a-zA-Z0-9]+\))|ARTICLE\s+|SECTION\s+))", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\"'])", paragraph)
        for piece in pieces:
            piece = piece.strip(" \t\n;")
            if piece and len(re.findall(r"\w+", piece)) >= 3:
                units.append(piece)
    # Remove duplicate units without changing their order.
    seen, result = set(), []
    for unit in units:
        key = _normalize(unit)
        if key and key not in seen:
            seen.add(key)
            result.append(unit)
    return result


def _normalize(text):
    text = (text or "").lower()
    text = re.sub(r"[\W_]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _similarity(left, right):
    a, b = _normalize(left), _normalize(right)
    if not a or not b:
        return 0.0
    seq = SequenceMatcher(None, a, b).ratio()
    wa, wb = set(a.split()), set(b.split())
    jaccard = len(wa & wb) / max(1, len(wa | wb))
    # Token overlap helps detect a small numeric/date/amount change.
    return 0.65 * seq + 0.35 * jaccard


def _change_note(old, new):
    old_tokens = re.findall(r"\w+|[^\w\s]", old)
    new_tokens = re.findall(r"\w+|[^\w\s]", new)
    matcher = SequenceMatcher(None, old_tokens, new_tokens)
    changes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            before = " ".join(old_tokens[i1:i2]).strip()
            after = " ".join(new_tokens[j1:j2]).strip()
            if before and after:
                changes.append(f"'{before}' changed to '{after}'")
            elif before:
                changes.append(f"'{before}' was removed")
            elif after:
                changes.append(f"'{after}' was added")
    return "; ".join(changes) if changes else "Wording modified"


def compare_contracts(original_text, revised_text):
    """Return exact shared, removed, added and likely modified clause units."""
    original = _split_clauses(original_text)
    revised = _split_clauses(revised_text)

    unmatched_old = set(range(len(original)))
    unmatched_new = set(range(len(revised)))
    shared, modified = [], []

    # Match exact clauses first.
    new_by_key = {}
    for j, clause in enumerate(revised):
        new_by_key.setdefault(_normalize(clause), []).append(j)
    for i, clause in enumerate(original):
        candidates = new_by_key.get(_normalize(clause), [])
        j = next((idx for idx in candidates if idx in unmatched_new), None)
        if j is not None:
            unmatched_old.remove(i)
            unmatched_new.remove(j)
            shared.append({"baseline": clause, "revision": revised[j]})

    # Pair remaining clauses by textual similarity. Threshold avoids pairing
    # unrelated provisions merely because they share generic legal vocabulary.
    candidates = []
    for i in unmatched_old:
        for j in unmatched_new:
            score = _similarity(original[i], revised[j])
            if score >= 0.48:
                candidates.append((score, i, j))
    candidates.sort(reverse=True)
    for score, i, j in candidates:
        if i in unmatched_old and j in unmatched_new:
            unmatched_old.remove(i)
            unmatched_new.remove(j)
            modified.append({
                "baseline": original[i],
                "revision": revised[j],
                "similarity": round(score * 100, 1),
                "change": _change_note(original[i], revised[j]),
            })

    removed = [original[i] for i in sorted(unmatched_old)]
    added = [revised[j] for j in sorted(unmatched_new)]
    return {
        "shared_clauses": shared,
        "modified_clauses": modified,
        "only_in_1": removed,
        "only_in_2": added,
        "counts": {
            "shared": len(shared),
            "modified": len(modified),
            "removed": len(removed),
            "added": len(added),
        },
    }
