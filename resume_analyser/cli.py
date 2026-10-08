"""Command-line entry point: python -m resume_analyser <resume> [--html report.html]"""

import argparse
import sys
from pathlib import Path

from .analyzer import analyse
from .extract import extract_text
from .market import measure
from .report import render_html, render_market_text, render_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="resume-analyser",
        description="Analyse a resume against the skills a Data Engineer needs.",
    )
    parser.add_argument("resume", nargs="?", help="Resume file (.pdf, .docx, .txt). "
                        "Omit to just show the Data Engineer skills map.")
    parser.add_argument("--job", metavar="PATH", help="Job description file (.txt, .pdf, .docx): "
                        "score only against the skills this job asks for.")
    parser.add_argument("--market", metavar="DIR", help="Folder of saved job descriptions: show the %% "
                        "of those ads that mention each skill.")
    parser.add_argument("--html", metavar="PATH", help="Also write an HTML report with bar charts.")
    args = parser.parse_args(argv)

    result = None
    if args.resume:
        try:
            text = extract_text(args.resume)
        except (OSError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if not text.strip():
            print("error: no text could be extracted (is the PDF a scanned image?)", file=sys.stderr)
            return 1
        job_text = None
        if args.job:
            try:
                job_text = extract_text(args.job)
            except (OSError, ValueError) as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
        result = analyse(text, job_text, Path(args.job).name if args.job else "")

    market = None
    if args.market:
        try:
            market = measure(args.market)
        except (OSError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(render_market_text(market, set(result.matched) if result else None) + "\n")

    print(render_text(result))
    if args.html:
        name = Path(args.resume).name if args.resume else ""
        Path(args.html).write_text(render_html(result, name, market), encoding="utf-8")
        print(f"\nHTML report written to {args.html}")
    return 0
