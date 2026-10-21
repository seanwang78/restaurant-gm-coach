#!/usr/bin/env python3
"""Coach workspace helper for the restaurant-gm-coach plugin.

Standard library only. Works on macOS, Windows and Linux with Python 3.8+.

Commands
  init <workspace> --brand NAME --owner NAME [--lang LANGUAGE]
  validate <workspace>            check every card and exam scenario
  coverage <workspace>            coverage by domain vs targets, stale cards
  index <workspace>               write index.md (approved cards by domain)
  skillmap <workspace>            write skill-map.md (depth per sub-skill)
  fidelity <workspace>            Shadow GM match rate (how much of the GM is copied)
  credits <workspace>             contributors and how much they taught
  next-id <workspace> <type> <domain>   e.g. next-id . rule D3
  next-shadow <workspace>         next Shadow GM round id (S-001…)
  next-feedback <workspace>       next feedback id (F-YYYYMMDD-001…)
  feedback <workspace>            open / closed feedback by sub-skill and cause
  import-feedback <workspace> <file.json>   turn flags from other systems into feedback files
  export <workspace> [--out FILE] four-layer "thinking package" JSON for other systems
  exam-report <run-file>          summarise an exam run table
"""
import argparse
import datetime as dt
import os
import re
import sys

DOMAINS = {
    "D1": "Strategy & brand direction",
    "D2": "P&L & commercial",
    "D3": "Operations excellence",
    "D4": "Guest experience & channels",
    "D5": "Marketing, menu & innovation",
    "D6": "People & leadership",
    "D7": "Growth & network",
    "D8": "Supply chain, cost & food safety",
    "D9": "Partners & stakeholders",
    "D10": "Risk, crisis & compliance",
}
TYPES = {"pattern": "M", "principle": "V", "reasoning": "T", "rule": "R", "case": "C", "benchmark": "B", "red-line": "X", "playbook": "P", "glossary": "G"}
FOLDERS = {"pattern": "patterns", "principle": "principles", "reasoning": "reasoning", "rule": "rules", "case": "cases", "benchmark": "benchmarks", "red-line": "red-lines",
           "playbook": "playbooks", "glossary": "glossary"}
TARGET_CARDS, TARGET_CASES, TARGET_EXAM = 8, 2, 4
LINK_RELS = {"derived_from", "based_on", "example_of", "refines", "conflicts_with", "see_also"}
FEEDBACK_STATUS = {"open", "in_review", "closed"}
FEEDBACK_REASONS = {"wrong", "not_applicable", "missing", "unclear", "outdated", "other"}
FEEDBACK_CAUSES = {"no_knowledge", "wrong_item_chosen", "missing_boundary", "outdated", "explained_badly",
                   "asker_was_right", "coach_was_right", "other"}
REQUIRED = ["id", "type", "domain", "title", "language", "brand", "scope", "contributors", "status", "created"]

PII_PATTERNS = [
    (re.compile(r"\b\d{1}[- ]?\d{4}[- ]?\d{5}[- ]?\d{2}[- ]?\d{1}\b"), "looks like a national ID number"),
    (re.compile(r"(?<!\d)0[689]\d[- ]?\d{3}[- ]?\d{4}(?!\d)"), "looks like a mobile phone number"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "contains an email address"),
]


def load_subskills():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "shared", "competency-framework.md")
    out = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\|\s*((?:D\d{1,2}\.\d)|X\d)\s*\|\s*([^|]+)\|", line)
                if m:
                    out[m.group(1)] = (m.group(2).strip(), "")
    except OSError:
        pass
    return out


SUBSKILLS = load_subskills()


# ---------- tiny front-matter reader (subset of YAML used by our cards) ----------
def _scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    return v


def read_front_matter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    block, body = text[3:end].strip("\n"), text[end + 4:]
    data, key, item = {}, None, None
    for raw in block.splitlines():
        line = raw.split(" #")[0].rstrip() if " #" in raw else raw.rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent == 0 and ":" in s:
            key, val = s.split(":", 1)
            key = key.strip()
            data[key] = _scalar(val) if val.strip() else []
            item = None
        elif s.startswith("- ") and key is not None:
            rest = s[2:]
            if ":" in rest and not rest.startswith(("http", "\"")):
                k, v = rest.split(":", 1)
                item = {k.strip(): _scalar(v)}
                if not isinstance(data.get(key), list):
                    data[key] = []
                data[key].append(item)
            else:
                if not isinstance(data.get(key), list):
                    data[key] = []
                data[key].append(_scalar(rest))
                item = None
        elif ":" in s and isinstance(item, dict):
            k, v = s.split(":", 1)
            item[k.strip()] = _scalar(v)
    return data, body


def walk_md(folder):
    for root, _dirs, files in os.walk(folder):
        for name in sorted(files):
            if name.endswith(".md"):
                yield os.path.join(root, name)


def load_cards(ws):
    cards = []
    for p in walk_md(os.path.join(ws, "knowledge")):
        fm, body = read_front_matter(p)
        cards.append((p, fm or {}, body))
    return cards


def load_scenarios(ws):
    out = []
    for p in walk_md(os.path.join(ws, "exam", "scenarios")):
        fm, body = read_front_matter(p)
        out.append((p, fm or {}, body))
    return out


def load_dir(ws, *parts):
    out = []
    for p in walk_md(os.path.join(ws, *parts)):
        fm, body = read_front_matter(p)
        out.append((p, fm or {}, body))
    return out


def sections(body):
    """Split a markdown body into {english_heading_lowercase: text} by '## ' headings."""
    out, cur, buf = {}, None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            head = line[3:].strip()
            cur = re.split(r"\s+[·/]\s+", head)[0].strip().lower()
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return {k: v for k, v in out.items() if v and not v.startswith("<!--")}


def as_date(v):
    try:
        return dt.date.fromisoformat(str(v))
    except ValueError:
        return None


# ---------- commands ----------
def cmd_init(a):
    ws = a.workspace
    for sub in ["knowledge/" + f for f in FOLDERS.values()] + ["conversations", "summaries", "sources", "feedback", "exports", "exam/scenarios", "exam/runs", "exam/shadow", "mentoring"]:
        os.makedirs(os.path.join(ws, sub), exist_ok=True)
    lang = a.lang
    files = {
        "CLAUDE.md": f"""# {a.brand} GM Coach workspace

Owner: {a.owner}, Brand GM, {a.brand}
Default language: {lang}; answer in the language the user writes in.
Purpose: capture the brand's operating know-how, test it, and use it to develop the next Brand GMs.

Rules for Claude in this folder:
- Use the restaurant-gm-coach skills: gm-talk (main), gm-retro (review flagged answers), gm-synthesise, gm-review, gm-coach-exam, gm-mentor, gm-flag; use the brand-gm-coach agent to answer questions.
- Keep the thinking, not only the conclusions: patterns, reasoning examples, links between items, Shadow GM corrections.
- The main work is conversation: copy how the GM thinks (decision logic, handling patterns), classify it with the skill map, and summarise it.
- Only cards with `status: approved` are used in coach answers. Drafts are shown only when the owner asks.
- Show contributor names on every tip.
- Never store personal data of staff or guests. Never copy confidential files outside this folder.
- Food-safety, legal and red-line cards are locked: never suggest breaking them.
""",
        "coach-profile.md": f"""# {a.brand} profile

- Stores: (number) in (countries); formats: (mall, street, kiosk, delivery-only…)
- Channels: dine-in %, take-away %, delivery % (approximate)
- Brand owner / franchisor: (if licensed)
- Key numbers the GM watches weekly: (e.g. SSSG, average check, labour %, food cost %, rating)
- Peak patterns: (hours, days, holidays)
- Current priorities this year: (3 lines)
""",
        "gm-mind.md": f"""# How {a.owner} thinks

Built from conversations. Each line ends with its source. Only lines {a.owner} said or confirmed.

## Priorities when things conflict
## What I look at every week
## How I read a P&L / a store / a report
## How I judge people
## Risk appetite
## How I decide
## Questions I always ask my managers
## Things I never do
## What I believe about our guests and our brand
## How my thinking changed over the years
""",
        "releases.md": f"# {a.brand} GM Coach releases\n\n| Version | Date | Cards | Exam score | What changed | Contributors |\n|---|---|---|---|---|---|\n",
    }
    os.makedirs(os.path.join(ws, ".claude"), exist_ok=True)
    files[os.path.join(".claude", "settings.json")] = '{\n  "permissions": {\n    "defaultMode": "acceptEdits",\n    "allow": ["Bash(python3:*)", "Bash(python:*)"]\n  }\n}\n'
    for name, content in files.items():
        p = os.path.join(ws, name)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
    print(f"Workspace ready: {os.path.abspath(ws)}")


def cmd_validate(a):
    ws, errors, warnings, seen = a.workspace, [], [], {}
    today = dt.date.today()
    for p, fm, body in load_cards(ws):
        rel = os.path.relpath(p, ws)
        if not fm:
            errors.append(f"{rel}: no front matter")
            continue
        for k in REQUIRED:
            if k not in fm or fm[k] in ("", [], None):
                errors.append(f"{rel}: missing '{k}'")
        t, d, cid = fm.get("type"), fm.get("domain"), str(fm.get("id", ""))
        if t and t not in TYPES:
            errors.append(f"{rel}: type '{t}' not one of {', '.join(TYPES)}")
        if d and d not in DOMAINS:
            errors.append(f"{rel}: domain '{d}' not D1–D10")
        if t in TYPES and d in DOMAINS and not re.fullmatch(rf"{TYPES[t]}-{d}-\d{{3}}", cid):
            errors.append(f"{rel}: id '{cid}' should look like {TYPES[t]}-{d}-001")
        if cid and not os.path.basename(p).startswith(cid):
            warnings.append(f"{rel}: file name should start with the id {cid}")
        if t in FOLDERS and os.path.basename(os.path.dirname(p)) != FOLDERS[t]:
            warnings.append(f"{rel}: a {t} card belongs in knowledge/{FOLDERS[t]}/")
        if cid in seen:
            errors.append(f"{rel}: duplicate id {cid} (also {seen[cid]})")
        seen[cid] = rel
        sk = str(fm.get("skill", ""))
        if not sk:
            warnings.append(f"{rel}: no 'skill' (sub-skill from the skill map)")
        elif d in DOMAINS and not (sk == d or sk.startswith(d + ".")) and not sk.startswith("X"):
            warnings.append(f"{rel}: skill {sk} is not inside domain {d}")
        elif SUBSKILLS and sk not in SUBSKILLS and sk not in DOMAINS:
            warnings.append(f"{rel}: skill {sk} is not in the skill map (propose it in synthesis)")
        if fm.get("status") not in ("draft", "approved", "retired"):
            errors.append(f"{rel}: status must be draft, approved or retired")
        if fm.get("status") == "approved" and not fm.get("approved_by"):
            errors.append(f"{rel}: approved card needs approved_by")
        rb = as_date(fm.get("review_by", ""))
        if rb and rb < today and fm.get("status") == "approved":
            warnings.append(f"{rel}: review date {rb} has passed")
        text = body + " " + " ".join(str(v) for k, v in fm.items() if k != "contributors")
        for rx, why in PII_PATTERNS:
            if rx.search(text):
                warnings.append(f"{rel}: {why} — remove personal data (data protection)")
    for p, fm, _body in load_cards(ws):
        for ln in fm.get("links", []) or []:
            rel = os.path.relpath(p, ws)
            if not isinstance(ln, dict) or not ln.get("id"):
                errors.append(f"{rel}: each link needs 'rel' and 'id'")
                continue
            if ln.get("rel") not in LINK_RELS:
                warnings.append(f"{rel}: link rel '{ln.get('rel')}' should be one of {', '.join(sorted(LINK_RELS))}")
            if str(ln["id"]) not in seen:
                warnings.append(f"{rel}: link to {ln['id']} — no item with that id")
    for p, fm, body in load_dir(ws, "exam", "shadow"):
        rel = os.path.relpath(p, ws)
        if not fm:
            continue  # older table-style files are still read by fidelity
        if not re.fullmatch(r"S-\d{3,}", str(fm.get("id", ""))):
            errors.append(f"{rel}: Shadow round needs id like S-001")
        if fm.get("result") not in ("full", "partial", "miss"):
            errors.append(f"{rel}: result must be full, partial or miss")
        for sec in ("situation", "coach prediction", "gm's real decision", "why"):
            if sec not in sections(body):
                warnings.append(f"{rel}: missing section '{sec}'")
    for p, fm, body in load_dir(ws, "feedback"):
        rel = os.path.relpath(p, ws)
        if not re.fullmatch(r"F-\d{8}-\d{3}", str(fm.get("id", ""))):
            errors.append(f"{rel}: feedback needs id like F-20261021-001")
        if fm.get("status") not in FEEDBACK_STATUS:
            errors.append(f"{rel}: status must be open, in_review or closed")
        if fm.get("reason") and fm.get("reason") not in FEEDBACK_REASONS:
            warnings.append(f"{rel}: reason should be one of {', '.join(sorted(FEEDBACK_REASONS))}")
        if fm.get("status") == "closed" and fm.get("cause") not in FEEDBACK_CAUSES:
            errors.append(f"{rel}: closed feedback needs a cause ({', '.join(sorted(FEEDBACK_CAUSES))})")
        for rx, why in PII_PATTERNS:
            if rx.search(body):
                warnings.append(f"{rel}: {why} — remove personal data (data protection)")
    for p, fm, body in load_scenarios(ws):
        rel = os.path.relpath(p, ws)
        if not fm or not re.fullmatch(r"E-D\d{1,2}-\d{3}", str(fm.get("id", ""))):
            errors.append(f"{rel}: exam scenario needs id like E-D3-001")
        for sec in ("## Situation", "## Model answer", "## Must mention"):
            if sec not in body:
                errors.append(f"{rel}: missing section '{sec}'")
    for m in errors:
        print("ERROR  ", m)
    for m in warnings:
        print("WARNING", m)
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def coverage_rows(ws):
    cards, scen = load_cards(ws), load_scenarios(ws)
    rows = []
    for d, name in DOMAINS.items():
        appr = [fm for _, fm, _ in cards if fm.get("domain") == d and fm.get("status") == "approved"]
        drafts = [fm for _, fm, _ in cards if fm.get("domain") == d and fm.get("status") == "draft"]
        cases = [fm for fm in appr if fm.get("type") == "case"]
        ex = [fm for _, fm, _ in scen if fm.get("domain") == d]
        pats = [fm for fm in appr if fm.get("type") == "pattern"]
        ok = len(appr) >= TARGET_CARDS and len(cases) >= TARGET_CASES and len(ex) >= TARGET_EXAM and len(pats) >= 2
        rows.append((d, name, len(appr), len(drafts), len(cases), len(ex), ok))
    return rows


def cmd_coverage(a):
    rows = coverage_rows(a.workspace)
    print(f"{'Domain':<5} {'Approved':>8} {'Draft':>6} {'Cases':>6} {'Exam':>5}  Status  Name")
    for d, name, ap, dr, ca, ex, ok in rows:
        status = "OK" if ok else "THIN"
        print(f"{d:<5} {ap:>8} {dr:>6} {ca:>6} {ex:>5}  {status:<6}  {name}")
    thin = [r[0] for r in rows if not r[6]]
    print(f"\nTargets per domain: {TARGET_CARDS} approved cards, {TARGET_CASES} cases, {TARGET_EXAM} exam scenarios.")
    print("Thin domains: " + (", ".join(thin) if thin else "none"))


def cmd_index(a):
    ws = a.workspace
    cards = [c for c in load_cards(ws) if c[1].get("status") == "approved"]
    lines = ["# Coach knowledge index", "", f"Generated {dt.date.today()} by kb_tool. Do not edit by hand.", ""]
    lines += ["| Domain | Approved | Cases | Exam |", "|---|---|---|---|"]
    for d, _name, ap, _dr, ca, ex, _ok in coverage_rows(ws):
        lines.append(f"| {d} | {ap} | {ca} | {ex} |")
    for d, name in DOMAINS.items():
        sub = [c for c in cards if c[1].get("domain") == d]
        if not sub:
            continue
        lines += ["", f"## {d} {name}", ""]
        for p, fm, _ in sorted(sub, key=lambda c: str(c[1].get("id"))):
            who = ", ".join(c.get("name", "") for c in fm.get("contributors", []) if isinstance(c, dict))
            rel = os.path.relpath(p, ws).replace(os.sep, "/")
            lines.append(f"- [{fm.get('id')}]({rel}) {fm.get('title')}{(' · ' + str(fm.get('title_alt'))) if fm.get('title_alt') else ''} — {who}")
    with open(os.path.join(ws, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"index.md written with {len(cards)} approved cards")


def cmd_credits(a):
    tally = {}
    for _p, fm, _b in load_cards(a.workspace):
        if fm.get("status") != "approved":
            continue
        for c in fm.get("contributors", []):
            if not isinstance(c, dict):
                continue
            key = c.get("name", "?")
            t = tally.setdefault(key, {"role": c.get("role", ""), "cards": 0, "cases": 0, "domains": set()})
            t["cards"] += 1
            t["cases"] += fm.get("type") == "case"
            t["domains"].add(fm.get("domain"))
    print(f"{'Contributor':<24} {'Cards':>5} {'Cases':>5}  Domains  Role")
    for name, t in sorted(tally.items(), key=lambda x: -x[1]["cards"]):
        print(f"{name:<24} {t['cards']:>5} {t['cases']:>5}  {','.join(sorted(d for d in t['domains'] if d)):<8} {t['role']}")


def shadow_rows(ws):
    rows = []
    score_of = {"full": 1.0, "partial": 0.5, "miss": 0.0}
    for p in walk_md(os.path.join(ws, "exam", "shadow")):
        fm, _body = read_front_matter(p)
        if fm and fm.get("id"):
            sc = score_of.get(str(fm.get("result", "")).lower())
            if sc is not None:
                rows.append((str(fm["id"]), str(fm.get("skill", "")), sc))
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 3 and re.fullmatch(r"S-\d{3,}", cells[0]):
                    score = {"full": 1.0, "partial": 0.5, "miss": 0.0}.get(cells[2].lower())
                    if score is not None:
                        rows.append((cells[0], cells[1], score))
    return rows


def cmd_fidelity(a):
    rows = shadow_rows(a.workspace)
    if not rows:
        print("No Shadow GM rounds yet. Expected rows like: | S-001 | D2.1 | full | notes |")
        return
    total = sum(r[2] for r in rows) / len(rows)
    print(f"Shadow GM rounds: {len(rows)}  Match rate: {total * 100:.0f}%")
    by = {}
    for _id, sk, sc in rows:
        by.setdefault(sk.split(".")[0], []).append(sc)
    for d in sorted(by, key=lambda x: (x[0], int(re.sub(r"\D", "", x) or 0))):
        print(f"  {d:<4} {sum(by[d]) / len(by[d]) * 100:5.0f}%  ({len(by[d])} rounds)")


def cmd_skillmap(a):
    ws = a.workspace
    cards = [fm for _p, fm, _b in load_cards(ws) if fm.get("status") in ("approved", "draft")]
    shadow = {}
    for _id, sk, sc in shadow_rows(ws):
        shadow.setdefault(sk, []).append(sc)
    keys = list(SUBSKILLS) or [d for d in DOMAINS]
    lines = ["# Skill map", "", f"Generated {dt.date.today()} by kb_tool. Depth: ⬜ none · 🟡 tips only · 🟠 has a decision pattern · 🟢 patterns + principles + case, Shadow match ≥ 70%", "",
             "| Code | Sub-skill | Approved | Draft | Patterns | Principles | Cases | Shadow | Depth |", "|---|---|---|---|---|---|---|---|---|"]
    gaps = []
    for k in keys:
        mine = [c for c in cards if str(c.get("skill", "")) == k or (k in DOMAINS and c.get("domain") == k)]
        ap = [c for c in mine if c.get("status") == "approved"]
        pat = sum(1 for c in ap if c.get("type") == "pattern")
        pri = sum(1 for c in ap if c.get("type") == "principle")
        cas = sum(1 for c in ap if c.get("type") == "case")
        sh = shadow.get(k, [])
        rate = sum(sh) / len(sh) if sh else None
        if not ap:
            depth = "⬜"
        elif pat == 0:
            depth = "🟡"
        elif pri and cas and rate is not None and rate >= 0.7:
            depth = "🟢"
        else:
            depth = "🟠"
        if depth in ("⬜", "🟡"):
            gaps.append(k)
        en, th = SUBSKILLS.get(k, (DOMAINS.get(k, k), ""))
        lines.append(f"| {k} | {en} | {len(ap)} | {len(mine) - len(ap)} | {pat} | {pri} | {cas} | {'' if rate is None else f'{rate * 100:.0f}%'} | {depth} |")
    lines += ["", f"Sub-skills still at ⬜/🟡: {len(gaps)} of {len(keys)}", ""]
    with open(os.path.join(ws, "skill-map.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"skill-map.md written: {len(keys)} sub-skills, {len(gaps)} still thin")


def cmd_next_shadow(a):
    nums = [int(r[0][2:]) for r in shadow_rows(a.workspace) if r[0][2:].isdigit()]
    print(f"S-{(max(nums) + 1 if nums else 1):03d}")


def cmd_next_feedback(a):
    today = dt.date.today().strftime("%Y%m%d")
    nums = [int(str(fm.get("id"))[-3:]) for _p, fm, _b in load_dir(a.workspace, "feedback")
            if str(fm.get("id", "")).startswith(f"F-{today}-")]
    print(f"F-{today}-{(max(nums) + 1 if nums else 1):03d}")


def cmd_feedback(a):
    items = [fm for _p, fm, _b in load_dir(a.workspace, "feedback")]
    if not items:
        print("No feedback yet.")
        return
    by_status = {}
    for fm in items:
        by_status[fm.get("status", "?")] = by_status.get(fm.get("status", "?"), 0) + 1
    print("Feedback: " + ", ".join(f"{k} {v}" for k, v in sorted(by_status.items())))
    open_ = [fm for fm in items if fm.get("status") != "closed"]
    by_skill = {}
    for fm in open_:
        by_skill.setdefault(str(fm.get("skill") or "unclassified"), []).append(fm)
    if open_:
        print("Open by sub-skill:")
        for k, v in sorted(by_skill.items(), key=lambda x: -len(x[1])):
            print(f"  {k:<14} {len(v)}  e.g. {v[0].get('id')}: {str(v[0].get('question', ''))[:60]}")
    causes = {}
    for fm in items:
        if fm.get("status") == "closed":
            causes[fm.get("cause", "?")] = causes.get(fm.get("cause", "?"), 0) + 1
    if causes:
        print("Closed by cause: " + ", ".join(f"{k} {v}" for k, v in sorted(causes.items(), key=lambda x: -x[1])))


def _yaml_str(v):
    v = str(v).replace("\n", " ").replace('"', "'")
    return f'"{v}"'


def cmd_import_feedback(a):
    import json
    with open(a.file, encoding="utf-8") as f:
        data = json.load(f)
    data = data if isinstance(data, list) else [data]
    os.makedirs(os.path.join(a.workspace, "feedback"), exist_ok=True)
    today = dt.date.today().strftime("%Y%m%d")
    existing = [int(str(fm.get("id"))[-3:]) for _p, fm, _b in load_dir(a.workspace, "feedback")
                if str(fm.get("id", "")).startswith(f"F-{today}-")]
    n = max(existing) if existing else 0
    for rec in data:
        n += 1
        fid = f"F-{today}-{n:03d}"
        used = rec.get("items_used", [])
        fm = [
            "---", f"id: {fid}", "status: open", f"created: {rec.get('created', dt.date.today().isoformat())}",
            f"source: {rec.get('source', 'import')}", f"asker_role: {_yaml_str(rec.get('asker_role', ''))}",
            f"store: {_yaml_str(rec.get('store', ''))}", f"reason: {rec.get('reason', 'other')}",
            f"skill: {rec.get('skill', '')}", f"items_used: [{', '.join(used)}]",
            f"question: {_yaml_str(rec.get('question', ''))}", "cause:", "resolved_by:", "resolution_items: []", "---", "",
            "## Question", rec.get("question", ""), "",
            "## Context", rec.get("context", ""), "",
            "## Coach answer", rec.get("coach_answer", ""), "",
            "## What was not right", rec.get("comment", ""), "",
            "## What I actually did", rec.get("what_i_did", ""), "",
            "## Result", rec.get("result", ""), "",
            "## GM retro", "", "",
        ]
        with open(os.path.join(a.workspace, "feedback", f"{fid}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(fm))
        print(f"created feedback/{fid}.md")


def _item(fm, body):
    return {
        "id": fm.get("id"), "type": fm.get("type"), "domain": fm.get("domain"), "skill": fm.get("skill"),
        "level": fm.get("level"), "title": fm.get("title"), "title_alt": fm.get("title_alt"),
        "language": fm.get("language"), "scope": fm.get("scope"), "tags": fm.get("tags", []),
        "confidence": fm.get("confidence"), "evidence": fm.get("evidence"),
        "contributors": [c for c in fm.get("contributors", []) if isinstance(c, dict)],
        "approved_by": fm.get("approved_by"), "created": fm.get("created"), "review_by": fm.get("review_by"),
        "links": [l for l in fm.get("links", []) or [] if isinstance(l, dict)],
        "sections": sections(body),
    }


def cmd_export(a):
    import json
    ws = a.workspace
    cards = [(p, fm, b) for p, fm, b in load_cards(ws) if fm.get("status") == "approved"]
    items = {str(fm.get("id")): _item(fm, b) for _p, fm, b in cards}
    by_type = {}
    for it in items.values():
        by_type.setdefault(it["type"], []).append(it)
    brand = owner = ""
    try:
        with open(os.path.join(ws, "CLAUDE.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("# ") and not brand:
                    brand = line[2:].replace(" GM Coach workspace", "").strip()
                if line.startswith("Owner:"):
                    owner = line.split(":", 1)[1].split(",")[0].strip()
    except OSError:
        pass
    version = ""
    try:
        with open(os.path.join(ws, "releases.md"), encoding="utf-8") as f:
            vs = re.findall(r"^\|\s*(v[\d.]+)\s*\|", f.read(), re.M)
            version = vs[-1] if vs else ""
    except OSError:
        pass
    mind = {}
    try:
        with open(os.path.join(ws, "gm-mind.md"), encoding="utf-8") as f:
            mind = {k: [l[2:].strip() for l in v.splitlines() if l.startswith("- ")] for k, v in sections(f.read()).items()}
    except OSError:
        pass
    shadow = []
    for _p, fm, body in load_dir(ws, "exam", "shadow"):
        if fm and fm.get("id"):
            shadow.append({"id": fm.get("id"), "skill": fm.get("skill"), "result": fm.get("result"),
                           "date": fm.get("date"), "learned_items": fm.get("learned_items", []), "sections": sections(body)})
    scenarios = []
    for _p, fm, body in load_scenarios(ws):
        scenarios.append({"id": fm.get("id"), "domain": fm.get("domain"), "level": fm.get("level"),
                          "critical": fm.get("critical"), "sections": sections(body)})
    regressions = []
    for _p, fm, body in load_dir(ws, "feedback"):
        if fm.get("status") == "closed" and fm.get("cause") not in ("coach_was_right",):
            sec = sections(body)
            regressions.append({"id": fm.get("id"), "skill": fm.get("skill"), "question": sec.get("question", ""),
                                "context": sec.get("context", ""), "gm_answer": sec.get("gm retro", ""),
                                "cause": fm.get("cause"), "resolution_items": fm.get("resolution_items", [])})
    graph = [{"from": i["id"], "rel": l.get("rel"), "to": l.get("id"), "note": l.get("note", "")}
             for i in items.values() for l in i["links"]]
    pkg = {
        "format": "restaurant-gm-coach/thinking-package", "format_version": "1.0",
        "brand": brand, "owner_gm": owner, "coach_version": version, "exported": dt.date.today().isoformat(),
        "skill_map": {k: v[0] for k, v in SUBSKILLS.items()},
        "how_to_use": "Reason like the GM: read layer4 priorities, pick the matching layer2 pattern, walk its steps with live data, "
                      "use layer3 examples as worked examples, apply layer1 points and red lines, cite item ids and contributors.",
        "layer1_points": [i for t in ("rule", "benchmark", "red-line", "playbook", "glossary") for i in by_type.get(t, [])],
        "layer2_structures": by_type.get("pattern", []),
        "layer3_examples": {"reasoning": by_type.get("reasoning", []), "cases": by_type.get("case", []), "shadow_rounds": shadow},
        "layer4_mind": {"gm_mind": mind, "principles": by_type.get("principle", []), "links": graph},
        "tests": {"exam_scenarios": scenarios, "shadow_rounds": [s["id"] for s in shadow], "feedback_regressions": regressions},
        "excluded": "drafts, retired items, conversation notes, mentoring files (private), personal data",
    }
    out = a.out or os.path.join(ws, "exports", f"thinking-package-{dt.date.today().isoformat()}.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pkg, f, ensure_ascii=False, indent=2)
    print(f"exported {len(items)} approved items, {len(shadow)} Shadow rounds, {len(scenarios)} exam scenarios, "
          f"{len(regressions)} feedback regressions, {len(graph)} links -> {out}")


def cmd_next_id(a):
    t, d = a.type, a.domain
    if t not in TYPES or d not in DOMAINS:
        sys.exit("type must be one of: " + ", ".join(TYPES) + "; domain D1–D10")
    prefix = f"{TYPES[t]}-{d}-"
    used = [int(str(fm.get("id"))[len(prefix):]) for _p, fm, _b in load_cards(a.workspace)
            if str(fm.get("id", "")).startswith(prefix) and str(fm.get("id"))[len(prefix):].isdigit()]
    print(f"{prefix}{(max(used) + 1 if used else 1):03d}")


def cmd_exam_report(a):
    rows = []
    with open(a.run_file, encoding="utf-8") as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and re.fullmatch(r"E-D\d{1,2}-\d{3}", cells[0]):
                try:
                    rows.append((cells[0], cells[1], float(cells[2]), cells[3].lower()))
                except ValueError:
                    pass
    if not rows:
        sys.exit("No result rows found. Expected: | E-D3-001 | D3 | 85 | yes | notes |")
    by = {}
    for _id, d, score, _ok in rows:
        by.setdefault(d, []).append(score)
    total = sum(r[2] for r in rows) / len(rows)
    passed = sum(1 for r in rows if r[3] in ("yes", "pass"))
    print(f"Scenarios: {len(rows)}  Passed: {passed}  Average score: {total:.1f}")
    for d in sorted(by, key=lambda x: int(x[1:])):
        print(f"  {d:<4} average {sum(by[d]) / len(by[d]):5.1f}  ({len(by[d])} scenarios)")
    crit = [r for r in rows if r[1] in ("D8", "D10") and r[3] not in ("yes", "pass")]
    print("Release gate: " + ("FAIL — a D8/D10 scenario did not pass" if crit else
                              ("PASS" if total >= 80 else "FAIL — average below 80")))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("init"); p.add_argument("workspace"); p.add_argument("--brand", required=True)
    p.add_argument("--owner", required=True); p.add_argument("--lang", default="English")
    p.set_defaults(fn=cmd_init)
    for name, fn in [("validate", cmd_validate), ("coverage", cmd_coverage), ("index", cmd_index), ("credits", cmd_credits),
                     ("skillmap", cmd_skillmap), ("fidelity", cmd_fidelity)]:
        p = sp.add_parser(name); p.add_argument("workspace"); p.set_defaults(fn=fn)
    p = sp.add_parser("next-id"); p.add_argument("workspace"); p.add_argument("type"); p.add_argument("domain")
    p.set_defaults(fn=cmd_next_id)
    p = sp.add_parser("exam-report"); p.add_argument("run_file"); p.set_defaults(fn=cmd_exam_report)
    for name, fn in [("next-shadow", cmd_next_shadow), ("next-feedback", cmd_next_feedback), ("feedback", cmd_feedback)]:
        p = sp.add_parser(name); p.add_argument("workspace"); p.set_defaults(fn=fn)
    p = sp.add_parser("import-feedback"); p.add_argument("workspace"); p.add_argument("file"); p.set_defaults(fn=cmd_import_feedback)
    p = sp.add_parser("export"); p.add_argument("workspace"); p.add_argument("--out"); p.set_defaults(fn=cmd_export)
    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
