import requests
from bs4 import BeautifulSoup


def find_html(soup, s):
    description = soup.find_all('tr')
    flag = False
    for row in description:
        if s in row.text.strip():
            flag = True
        elif flag:
            description_text = row.td.text.strip()
            return description_text


def scrape_cve_info(cve_id):
    url = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        Description = find_html(soup, "Description")
        References = find_html(soup, "References")
        MISC_links = []
        URL_links = []
        for i in References.split('\n'):
            if i.startswith("MISC"):
                MISC_links.append(i[5:])
            else:
                URL_links.append(i[4:])
        new_cve_info = {'CVE': cve_id, 'Description': Description, 'References': {
            "MISC_links": MISC_links,
            "URL_links": URL_links
        }}
        return new_cve_info
    else:
        print("Failed to retrieve CVE information")
        return None


def exploit_management(exp, exp_type):
    Static_exp_type = ["Message", "Command", "Script", "Script to Modify", "Multiple"]

