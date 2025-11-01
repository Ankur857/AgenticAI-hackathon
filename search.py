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

# Extract all keywords (split by commas, spaces, and/or 'and'/'or')
keywords = re.split(r"[, ]+| and | or ", query)
keywords = [k.strip() for k in keywords if k.strip()]

# -------------------------------
# 3️⃣ Filter jobs - match ANY keyword + must have link
# -------------------------------
filtered_jobs = []
for job in jobs:
    text = f"{job.get('job_title', '')} {job.get('job_summary', '')}".lower()
    link = job.get("apply_link") or job.get("url")
    
    # ✅ Match if ANY keyword matches AND job has a valid link
    if link and any(keyword in text for keyword in keywords):
        job["link"] = link  # store final link field
        filtered_jobs.append(job)

# -------------------------------
# 4️⃣ Display top 10 results with links
# -------------------------------
if not filtered_jobs:
    print(f"\n❌ No jobs found for: {query}")
else:
    print(f"\n✅ Found {len(filtered_jobs)} job(s) with apply links for keywords: {', '.join(keywords)}\n")
    for i, job in enumerate(filtered_jobs[:10], 1):  # show top 10
        print(f"{i}. Title: {job.get('job_title', 'N/A')}")
        print(f"   Company: {job.get('company_name', 'N/A')}")
        print(f"   Location: {job.get('job_location', 'N/A')}")
        print(f"   Employment Type: {job.get('job_employment_type', 'N/A')}")
        print(f"   Salary: {job.get('job_base_pay_range', 'N/A')}")
        print(f"   Applicants: {job.get('job_num_applicants', 'N/A')}")
        print(f"   🔗 Link: {job['link']}")
        print(f"   Posted: {job.get('job_posted_time', 'N/A')}")
        print("-" * 80)
