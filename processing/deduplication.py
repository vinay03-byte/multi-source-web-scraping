def deduplicate_records(records: list[dict]):
    """Keep first occurrence using source + normalized title/quote + source URL."""
    seen = set()
    unique = []
    duplicates = 0
    for record in records:
        key = (
            (record.get("source") or "").casefold().strip(),
            " ".join((record.get("name_or_title") or "").casefold().split()),
            (record.get("source_url") or "").casefold().strip().rstrip("/"),
        )
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append(record)
    return unique, duplicates
