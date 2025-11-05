import json
import re
from typing import List, Dict, Iterable


def _load_jobs(data_path: str) -> List[Dict]:
    """Load and normalize jobs JSON from the given path.

    Returns a list of job dictionaries (even when the source is a single object).
    """
    with open(data_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("Invalid JSON format. Must be an object or list.")


def extract_keywords_from_text(text: str) -> List[str]:
    """Extract simple lowercase keywords from free text.

    Splits by commas, whitespace, and the words 'and'/'or'.
    """
    query = (text or "").lower().strip()
    parts = re.split(r"[, ]+| and | or ", query)
    return [p.strip() for p in parts if p and p.strip()]


def filter_jobs_by_keywords(
    keywords: Iterable[str],
    data_path: str = "job_data.json",
    limit: int = 10,
) -> List[Dict]:
    """Filter jobs whose title or summary contains ANY of the keywords.

    Only returns jobs that have a valid apply link (from `apply_link` or `url`).
    Adds a unified `link` field to each returned job.
    """
    keywords_normalized = [k.lower().strip() for k in keywords if k and str(k).strip()]
    if not keywords_normalized:
        return []

    jobs = _load_jobs(data_path)
    filtered: List[Dict] = []
    for job in jobs:
        text = f"{job.get('job_title', '')} {job.get('job_summary', '')}".lower()
        link = job.get("apply_link") or job.get("url")
        if link and any(k in text for k in keywords_normalized):
            job_copy = dict(job)
            job_copy["link"] = link
            filtered.append(job_copy)

    if limit is not None and limit > 0:
        return filtered[:limit]
    return filtered


if __name__ == "__main__":
    # Simple CLI fallback for quick testing
    query_input = input("Enter job query (e.g. 'cloud react android'): ")
    kws = extract_keywords_from_text(query_input)
    results = filter_jobs_by_keywords(kws)
    if not results:
        print(f"\n❌ No jobs found for: {', '.join(kws) or '(empty query)'}")
    else:
        print(
            f"\n✅ Found {len(results)} job(s) with apply links for keywords: {', '.join(kws)}\n"
        )
        for i, job in enumerate(results, 1):
            print(f"{i}. Title: {job.get('job_title', 'N/A')}")
            print(f"   Company: {job.get('company_name', 'N/A')}")
            print(f"   Location: {job.get('job_location', 'N/A')}")
            print(f"   Employment Type: {job.get('job_employment_type', 'N/A')}")
            print(f"   Salary: {job.get('job_base_pay_range', 'N/A')}")
            print(f"   Applicants: {job.get('job_num_applicants', 'N/A')}")
            print(f"   🔗 Link: {job['link']}")
            print(f"   Posted: {job.get('job_posted_time', 'N/A')}")
            print("-" * 80)
