import requests
from bs4 import BeautifulSoup

black_list = []
functions = []


def process_page(url, stopurl):
    base_url = url.split('/')
    base_url = '/'.join(base_url[:-1])+'/'
    response = requests.get(url)
    if response.status_code != 200:
        print("无法访问页面:", url)
        return
    soup = BeautifulSoup(response.text, 'html.parser')

    function = soup.find_all('code')
    for i in function:
        functions.append(i.text)
    a_tag = soup.find('a', attrs={'aria-label': 'Next'})
    if a_tag:
        next_url = a_tag['href']
        next_url = base_url + next_url
        if next_url == stopurl:
            return None
        else:
            print("下一个页面:", next_url)
            process_page(next_url, stopurl)
    else:
        print("未找到下一个页面")


def make_black_for_mysql8_function():
    f = open("mysql83_functions_operators.txt", "w")
    stopurl = "https://dev.mysql.com/doc/refman/8.3/en/type-conversion.html"
    url = "https://dev.mysql.com/doc/refman/8.3/en/built-in-function-reference.html"
    process_page(url, stopurl)
    for i in functions:
        f.write(i + "\n")
    f = open("mysql83_functions_operators.txt", "r")
    all = f.readlines()
    s = []
    for i in all:
        if '_' in i:
            b = i.split("_")
            if b[0] + '\n' not in s:
                s.append(b[0] + '\n')
        else:
            s.append(i)
    o = open("black_mysql8.txt", "w")
    for i in s:
        o.write(i)


if __name__ == "__main__":
    make_black_for_mysql8_function()
