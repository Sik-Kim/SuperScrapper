import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    #find는 하나만 가져
    last_page = pages[-2].get_text(strip=True)  #get_text도 soup library 기능
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {
        "class": "fc-black-700"
    }).find_all(
        "span", recursive=False)
    #h3 아래의 모든 span을 불러온다. 하지만 recursive=False에 의 span의 하위의 것은 불러오지 않는다.
    #h3안의 요소 span이 2개 있는 것을 알기에 company, location = 이런식으로 씀!
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    # .strip("-").strip("\r") -삭제랑 엔터 삭제 이건 필요없어서 삭제
    job_id = html["data-jobid"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            # print(job)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    #{word}는 url에서 넘어온 어떤거든지 될 수 있음. 꼭 python 뿐만 아니라.
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
