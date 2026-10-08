"""Render analysis results as terminal bar charts or a self-contained HTML report."""

from html import escape

from .analyzer import AnalysisResult
from .market import MarketDemand
from .skills import CATEGORIES, SKILLS, Skill

BAR_WIDTH = 30


def _bar(pct: float, width: int = BAR_WIDTH) -> str:
    filled = round(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def render_text(result: AnalysisResult | None) -> str:
    lines: list[str] = []
    if result is not None:
        target = f"job '{result.job_name}'" if result.job_name else "Data Engineer"
        lines += [
            f"Overall {target} match: {result.score:.0f}%  {_bar(result.score)}",
            "",
            "Coverage by category (demand-weighted)",
            "-" * 72,
        ]
        for c in result.categories:
            lines.append(f"{c.category:<34} {_bar(c.coverage)} {c.coverage:5.0f}%")
        lines.append("")

    found = set(result.matched) if result else set()
    shown = SKILLS if result is None else result.matched + result.missing
    heading = "Skills the job asks for" if result and result.job_name else "Data Engineer skills"
    lines += [f"{heading} by job-market demand (% of postings)", "-" * 72]
    for category in CATEGORIES:
        skills = sorted((s for s in shown if s.category == category), key=lambda s: -s.demand)
        if not skills:
            continue
        lines.append(f"\n{category}")
        for s in skills:
            mark = "" if result is None else ("  ✓ have" if s in found else "  ✗ learn")
            lines.append(f"  {s.name:<34} {_bar(s.demand)} {s.demand:3d}%{mark}")

    if result is not None:
        lines += ["", "Skills to learn next (highest demand first)", "-" * 72]
        for i, s in enumerate(result.skills_to_learn, 1):
            lines.append(f"{i:2d}. {s.name:<34} {s.demand:3d}%  {s.tier:<13} {s.category}")
    return "\n".join(lines)


_CSS = """
:root {
  color-scheme: light;
  --surface: #fcfcfb; --surface-2: #f3f2ef; --border: #e2e1dc;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --text-muted: #6f6e69;
  --bar: #2a78d6; --track: #ebeae6;
  --good: #008300; --critical: #c62f2f;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --surface: #1a1a19; --surface-2: #232321; --border: #383835;
    --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #9a998f;
    --bar: #3987e5; --track: #2c2c2a;
    --good: #3fb950; --critical: #f07171;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface: #1a1a19; --surface-2: #232321; --border: #383835;
  --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #9a998f;
  --bar: #3987e5; --track: #2c2c2a;
  --good: #3fb950; --critical: #f07171;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--surface); color: var(--text-primary);
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 920px; margin: 0 auto; padding: 32px 16px 64px; }
h1 { font-size: 28px; margin: 0 0 4px; }
h2 { font-size: 19px; margin: 40px 0 4px; }
h3 { font-size: 13px; text-transform: uppercase; letter-spacing: .06em;
  color: var(--text-secondary); margin: 24px 0 8px; }
p.note { color: var(--text-secondary); margin: 0 0 16px; }
.hero { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 24px; }
.tile { flex: 1 1 160px; background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 12px; padding: 16px; }
.tile .v { font-size: 34px; font-weight: 650; font-variant-numeric: tabular-nums; }
.tile .k { color: var(--text-secondary); font-size: 13px; }
.row { display: grid; grid-template-columns: minmax(120px, 270px) 1fr 48px 96px;
  align-items: center; gap: 12px; padding: 4px 0; }
.row:hover { background: var(--surface-2); }
.name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.track { height: 12px; background: var(--track); border-radius: 0 4px 4px 0; }
.fill { height: 100%; background: var(--bar); border-radius: 0 4px 4px 0; min-width: 2px; }
.pct { text-align: right; font-variant-numeric: tabular-nums; color: var(--text-secondary); }
.status { font-size: 12px; white-space: nowrap; min-width: 64px; }
.status.have { color: var(--good); }
.status.learn { color: var(--critical); }
.cols-3 .row { grid-template-columns: minmax(120px, 270px) 1fr 48px; }
ol.learn { padding-left: 24px; }
ol.learn li { margin: 6px 0; }
.tier { font-size: 12px; color: var(--text-muted); border: 1px solid var(--border);
  border-radius: 999px; padding: 1px 8px; margin-left: 6px; }
footer { margin-top: 48px; color: var(--text-muted); font-size: 13px; }
@media (max-width: 560px) {
  .row { grid-template-columns: 1fr 44px 88px; }
  .row > * { min-width: 0; }
  .row .name { grid-column: 1 / -1; }
  .cols-3 .row { grid-template-columns: 1fr 44px; }
}
"""


def _row(name: str, pct: float, status: str | None = None, tip: str = "") -> str:
    status_html = ""
    if status == "have":
        status_html = '<span class="status have">✓ On resume</span>'
    elif status == "learn":
        status_html = '<span class="status learn">✗ To learn</span>'
    title = escape(tip or f"{name}: {pct:.0f}%")
    return (
        f'<div class="row" title="{title}"><span class="name">{escape(name)}</span>'
        f'<div class="track" role="img" aria-label="{title}">'
        f'<div class="fill" style="width:{pct:.1f}%"></div></div>'
        f'<span class="pct">{pct:.0f}%</span>{status_html}</div>'
    )


def _skill_rows(skills: list[Skill], found: set[Skill] | None) -> str:
    rows = []
    for s in sorted(skills, key=lambda s: -s.demand):
        status = None if found is None else ("have" if s in found else "learn")
        rows.append(_row(s.name, s.demand, status, f"{s.name}: in ~{s.demand}% of postings · {s.tier}"))
    return "\n".join(rows)


def render_html(result: AnalysisResult | None, resume_name: str = "",
                market: MarketDemand | None = None) -> str:
    found = set(result.matched) if result else None
    body: list[str] = []

    if result is None:
        body.append("<h1>Data Engineer Skills Map</h1>")
        body.append('<p class="note">Every skill a Data Engineer needs, ranked by how often it '
                    "appears in job postings.</p>")
    else:
        title = f"Resume Analysis{': ' + escape(resume_name) if resume_name else ''}"
        must = [s for s in result.skills_to_learn if s.tier == "Must-have"]
        target = (f"the skills the job description <strong>{escape(result.job_name)}</strong> asks for"
                  if result.job_name else "the Data Engineer skill catalog")
        body.append(f"<h1>{title}</h1>")
        body.append(f'<p class="note">Scored against {target}, weighted by job-market demand.</p>')
        body.append('<div class="hero">'
                    f'<div class="tile"><div class="v">{result.score:.0f}%</div>'
                    '<div class="k">Overall match (demand-weighted)</div></div>'
                    f'<div class="tile"><div class="v">{len(result.matched)}/{len(result.matched) + len(result.missing)}</div>'
                    '<div class="k">Skills found on resume</div></div>'
                    f'<div class="tile"><div class="v">{len(must)}</div>'
                    '<div class="k">Must-have skills missing</div></div></div>')
        body.append("<h2>Coverage by category</h2>")
        body.append('<p class="note">Share of each category\'s demand-weighted skills found on the resume.</p>')
        body.append('<div class="cols-3">' + "\n".join(
            _row(c.category, c.coverage,
                 tip=f"{c.category}: {c.coverage:.0f}% · {len(c.matched)} of "
                     f"{len(c.matched) + len(c.missing)} skills")
            for c in result.categories) + "</div>")

    if market is not None and market.job_count:
        body.append(render_market_html(market, found))

    body.append("<h2>Skills by job-market demand</h2>")
    body.append('<p class="note">Bar = approximate % of Data Engineer job postings that mention the skill. '
                "Must-have ≥ 40%, Important 20–39%, Nice-to-have &lt; 20%.</p>")
    wrap = "" if found is not None else ' class="cols-3"'
    shown = SKILLS if result is None else result.matched + result.missing
    for category in CATEGORIES:
        skills = [s for s in shown if s.category == category]
        if not skills:
            continue
        body.append(f"<h3>{escape(category)}</h3><div{wrap}>{_skill_rows(skills, found)}</div>")

    if result is not None:
        body.append("<h2>Skills to learn next</h2>")
        body.append('<p class="note">Missing skills, highest demand first — start at the top.</p>')
        items = "".join(
            f"<li><strong>{escape(s.name)}</strong> — {s.demand}% of postings"
            f'<span class="tier">{s.tier}</span> <span class="note">· {escape(s.category)}</span></li>'
            for s in result.skills_to_learn)
        body.append(f'<ol class="learn">{items}</ol>' if items else "<p>Nothing missing — great job!</p>")

    body.append("<footer>Demand percentages are rounded estimates from public job-market analyses; "
                "use them as relative guidance.</footer>")
    page_title = "Data Engineer Skills Map" if result is None else "Resume Analysis Report"
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{page_title}</title><style>{_CSS}</style></head>"
        f"<body><main>{''.join(body)}</main></body></html>\n"
    )


def render_market_text(market: MarketDemand, found: set[Skill] | None = None) -> str:
    lines = [f"Skills mentioned across your {market.job_count} collected job ads (% of ads)", "-" * 72]
    for s, pct in market.ranked():
        mark = "" if found is None else ("  ✓ have" if s in found else "  ✗ learn")
        lines.append(f"  {s.name:<34} {_bar(pct)} {pct:3.0f}%{mark}")
    return "\n".join(lines)


def render_market_html(market: MarketDemand, found: set[Skill] | None = None) -> str:
    """HTML section: bars = share of the collected job ads that mention each skill."""
    rows = []
    for s, pct in market.ranked():
        status = None if found is None else ("have" if s in found else "learn")
        n = market.counts[s]
        rows.append(_row(s.name, pct, status, f"{s.name}: in {n} of {market.job_count} of your job ads"))
    wrap = "" if found is not None else ' class="cols-3"'
    return (f"<h2>What your {market.job_count} collected job ads ask for</h2>"
            '<p class="note">Bar = % of your saved job descriptions that mention the skill.</p>'
            f"<div{wrap}>{''.join(rows)}</div>")
