import requests

api_key="a76c64baf0mshc79fe98b2242d56p1a5223jsna7422320b483"

query="React js"

url="https://jsearch.p.rapidapi.com/search?query=developer%20jobs%20in%20chicago&page=1&num_pages=1&country=us&date_posted=all"

headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}

params = {
    "query": query,
    "page": "1",
    "num_pages": "1"
}

response=requests.get(url,params=params,headers=headers)

data=response.json()

for job in data.get("data",[]):
    print(f"Title:{job["job_title"]}")
    print(f"Company: {job['employer_name']}")
    print(f"Location: {job['job_city']}, {job['job_country']}")
    print(f"Link: {job['job_apply_link']}")
    print("-" * 60)