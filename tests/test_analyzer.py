from pathlib import Path

from resume_analyser.analyzer import analyse, find_skills
from resume_analyser.report import render_html, render_text
from resume_analyser.skills import SKILLS

BY_NAME = {s.name: s for s in SKILLS}
SAMPLE = Path(__file__).parent.parent / "samples" / "sample_resume.txt"


def names(skills):
    return {s.name for s in skills}


def test_aliases_match():
    found = names(find_skills("Built pipelines with PySpark, Airflow and k8s on AWS."))
    assert {"Apache Spark", "Python", "Apache Airflow", "Kubernetes", "AWS"} <= found


def test_word_boundaries():
    # "git" inside "digital" or "sql" inside "nosqlish" must not match
    found = names(find_skills("digital marketing"))
    assert "Git" not in found
    assert "Scala" not in names(find_skills("scalable systems"))


def test_symbols_in_terms():
    assert "CI/CD" in names(find_skills("Set up CI/CD with Jenkins"))


def test_scores_range():
    empty = analyse("")
    assert empty.score == 0
    assert len(empty.skills_to_learn) == len(SKILLS)
    full = analyse(" ".join(s.name for s in SKILLS))
    assert round(full.score) == 100
    assert not full.missing


def test_skills_to_learn_sorted_by_demand():
    demands = [s.demand for s in analyse("Python").skills_to_learn]
    assert demands == sorted(demands, reverse=True)


def test_sample_resume_and_reports():
    result = analyse(SAMPLE.read_text())
    assert {"SQL", "Python", "Snowflake", "dbt"} <= names(result.matched)
    assert "Apache Kafka" in names(result.missing)
    assert "Overall Data Engineer match" in render_text(result)
    html = render_html(result, "sample_resume.txt")
    assert "<title>Resume Analysis Report</title>" in html
    assert "Skills to learn next" in html
    assert "Data Engineer Skills Map" in render_html(None)


def test_plurals_match():
    found = names(find_skills("Set up data lakes and engaged senior stakeholders"))
    assert {"Data Lake / Lakehouse", "Communication & Collaboration"} <= found


def test_job_mode_only_scores_requested_skills():
    result = analyse("Python and SQL", job_text="We need Python, SQL and Kafka", job_name="jd.txt")
    assert names(result.matched) == {"Python", "SQL"}
    assert names(result.missing) == {"Apache Kafka"}
    assert {c.category for c in result.categories} == {"Programming", "Streaming"}
    assert "jd.txt" in render_text(result)


def test_market_demand():
    from resume_analyser.market import measure

    market = measure(SAMPLE.parent / "jobs")
    assert market.job_count == 5
    assert market.percent(BY_NAME["Databricks"]) == 80
    ranked = [pct for _, pct in market.ranked()]
    assert ranked == sorted(ranked, reverse=True)


def test_ai_terms_do_not_match_inside_words():
    assert "Generative AI & LLMs" not in names(find_skills("Maintained email campaigns"))
    assert "Generative AI & LLMs" in names(find_skills("Built AI-ready data platforms"))
