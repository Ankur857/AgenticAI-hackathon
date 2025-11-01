import json
import re

# -------------------------------
# 1️⃣ Load JSON file
# -------------------------------
with open("job_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Normalize to list
if isinstance(data, dict):
    jobs = [data]
elif isinstance(data, list):
    jobs = data
else:
    raise ValueError("Invalid JSON format. Must be an object or list.")

# -------------------------------
# 2️⃣ Get user input (flexible)
# -------------------------------
query = input("Enter job query (e.g. 'cloud react android'): ").lower().strip()

# Extract all keywords separated by space, comma, 'and', 'or'
keywords = re.split(r"[, ]+| and | or ", query)
keywords = [k.strip() for k in keywords if k.strip()]

# -------------------------------
# 3️⃣ Filter jobs - match ANY keyword
# -------------------------------
filtered_jobs = []
for job in jobs:
    text = f"{job.get('job_title', '')} {job.get('job_summary', '')}".lower()
    # ✅ Include if ANY keyword matches
    if any(keyword in text for keyword in keywords):
        filtered_jobs.append(job)

# -------------------------------
# 4️⃣ Display all matching jobs (top 10 max)
# -------------------------------
if not filtered_jobs:
    print(f"\n❌ No jobs found for: {query}")
else:
    print(f"\n✅ Found {len(filtered_jobs)} job(s) for keywords: {', '.join(keywords)}\n")
    for i, job in enumerate(filtered_jobs[:10], 1):  # show top 10 for readability
        print(f"{i}. Title: {job.get('job_title', 'N/A')}")
        print(f"   Company: {job.get('company_name', 'N/A')}")
        print(f"   Location: {job.get('job_location', 'N/A')}")
        print(f"   Employment Type: {job.get('job_employment_type', 'N/A')}")
        print(f"   Salary: {job.get('job_base_pay_range', 'N/A')}")
        print(f"   Applicants: {job.get('job_num_applicants', 'N/A')}")
        print(f"   Link: {job.get('apply_link', job.get('url', 'N/A'))}")
        print(f"   Posted: {job.get('job_posted_time', 'N/A')}")
        print("-" * 80)
