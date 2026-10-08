"""Measure skill demand across a folder of collected job descriptions."""

from dataclasses import dataclass
from pathlib import Path

from .analyzer import find_skills
from .extract import extract_text
from .skills import SKILLS, Skill

JOB_SUFFIXES = {".txt", ".md", ".pdf", ".docx"}


@dataclass(frozen=True)
class MarketDemand:
    job_count: int
    counts: dict[Skill, int]  # number of jobs mentioning each skill

    def percent(self, skill: Skill) -> float:
        return 100 * self.counts.get(skill, 0) / self.job_count if self.job_count else 0.0

    def ranked(self) -> list[tuple[Skill, float]]:
        """Skills mentioned at least once, most frequent first."""
        return sorted(((s, self.percent(s)) for s in SKILLS if self.counts.get(s)),
                      key=lambda pair: (-pair[1], -pair[0].demand))


def measure(job_dir: str | Path) -> MarketDemand:
    files = sorted(p for p in Path(job_dir).iterdir() if p.suffix.lower() in JOB_SUFFIXES)
    counts: dict[Skill, int] = {}
    for f in files:
        for skill in find_skills(extract_text(f)):
            counts[skill] = counts.get(skill, 0) + 1
    return MarketDemand(job_count=len(files), counts=counts)
