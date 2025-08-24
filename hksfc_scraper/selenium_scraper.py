# we are not using this method of scrapping currently 
from selenium import webdriver
from bs4 import BeautifulSoup

def extract_individual_details(ceref):
    """Extract details of an individual license using Selenium and return JSON"""
    url = f"https://apps.sfc.hk/publicregWeb/indi/{ceref}/details"
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    data = {}

    tables = soup.find_all("table", {"class": "x-field"})
    for table in tables:
        label = table.find("label")
        value = table.find("div", {"class": "x-form-display-field"})
        if label and value:
            field_name = label.get_text(strip=True).replace(":", "")
            field_value = value.get_text(strip=True)
            data[field_name] = field_value

    grid_table = soup.find("table", {"class": "x-grid-table"})
    grid_data = []
    if grid_table:
        headers = []
        header_container = soup.find("div", {"id": "headercontainer-1022"})  
        if header_container:
            headers = [
                h.get_text(" ", strip=True)
                for h in header_container.find_all("span", {"class": "x-column-header-text"})
            ]

        for row in grid_table.find_all("tr", {"class": "x-grid-row"}):
            row_data = {}
            cells = row.find_all("td")
            for i, cell in enumerate(cells):
                value = cell.get_text(" ", strip=True)
                if headers and i < len(headers):
                    row_data[headers[i]] = value
                else:
                    row_data[f"col_{i}"] = value  
            grid_data.append(row_data)

    if grid_data:
        data["LicenseDetails"] = grid_data

    driver.quit()
    return data
