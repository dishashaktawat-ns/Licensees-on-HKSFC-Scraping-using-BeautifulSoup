from selenium import webdriver
from bs4 import BeautifulSoup

def extract_individual_details(ceref):
    """Extract details of an individual license using Selenium"""
    url = f"https://apps.sfc.hk/publicregWeb/indi/{ceref}/details"
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", {"class": "x-grid-table"})
    rows = []

    if table:
        for tr in table.find_all("tr", {"class": "x-grid-row"}):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
            rows.append(cells)

    driver.quit()
    return rows
