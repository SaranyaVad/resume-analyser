"""Match resume text against the Data Engineer skill catalog and score it."""

import re
from dataclasses import dataclass

from .skills import CATEGORIES, SKILLS, Skill


@dataclass(frozen=True)
class CategoryScore:
    category: str
    matched: tuple[Skill, ...]
    missing: tuple[Skill, ...]

    @property
    def coverage(self) -> float:
        """Demand-weighted share of this category's skills found in the resume (0-100)."""
        total = sum(s.demand for s in self.matched + self.missing)
        return 100 * sum(s.demand for s in self.matched) / total if total else 0.0


@dataclass(frozen=True)
class AnalysisResult:
    matched: tuple[Skill, ...]
    missing: tuple[Skill, ...]
    categories: tuple[CategoryScore, ...]
    job_name: str = ""  # set when scored against a specific job description

    @property
    def score(self) -> float:
        """Overall demand-weighted match score (0-100)."""
        total = sum(s.demand for s in self.matched + self.missing)
        return 100 * sum(s.demand for s in self.matched) / total if total else 0.0

    @property
    def skills_to_learn(self) -> tuple[Skill, ...]:
        """Missing skills, highest market demand first."""
        return tuple(sorted(self.missing, key=lambda s: -s.demand))


def _compile(term: str) -> re.Pattern[str]:
    # Word-ish boundaries that still allow symbols like "ci/cd", plus simple plurals ("data lakes").
    return re.compile(r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?:e?s)?(?![a-z0-9])")


_PATTERNS = {skill: tuple(_compile(p) for p in skill.patterns) for skill in SKILLS}


def find_skills(text: str) -> set[Skill]:
    lowered = text.lower()
    # Also try with hyphens as spaces so "data-quality" matches "data quality".
    variants = (lowered, lowered.replace("-", " "))
    return {skill for skill, patterns in _PATTERNS.items()
            if any(p.search(v) for p in patterns for v in variants)}


def analyse(text: str, job_text: str | None = None, job_name: str = "") -> AnalysisResult:
    """Score resume text against all Data Engineer skills, or only those a job description asks for."""
    found = find_skills(text)
    wanted = SKILLS if job_text is None else tuple(s for s in SKILLS if s in find_skills(job_text))
    matched = tuple(s for s in wanted if s in found)
    missing = tuple(s for s in wanted if s not in found)
    categories = tuple(
        CategoryScore(
            category=c,
            matched=tuple(s for s in matched if s.category == c),
            missing=tuple(s for s in missing if s.category == c),
        )
        for c in CATEGORIES
        if any(s.category == c for s in wanted)
    )
    return AnalysisResult(matched=matched, missing=missing, categories=categories, job_name=job_name)
