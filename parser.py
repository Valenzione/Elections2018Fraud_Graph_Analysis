import contextlib
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# Utility Function to wait for page to load.
@contextlib.contextmanager
def wait_for_page_load(driver_, timeout=30):
    old_page = driver_.find_element_by_tag_name('html')
    yield
    WebDriverWait(driver_, timeout).until(staleness_of(old_page))


driver = webdriver.Firefox()

# Root presidential elections link
driver.get(
    "http://www.vybory.izbirkom.ru/region/izbirkom?action=show&root_a=12000009&vrn=100100084849062&region=0&global=true&type=0&prver=0&pronetvd=null")

# Iterate over every region
dropRegion = Select(driver.find_element(By.NAME, "gs"))
for i in range(1, len(dropRegion.options) - 1):
    dropRegion = Select(driver.find_element(By.NAME, "gs"))
    dropRegion.select_by_index(i)
    region_name = dropRegion.first_selected_option.text
    driver.find_element(By.NAME, "go").click()

    # Iterate over every subregion
    dropSubRegion = Select(driver.find_element(By.NAME, "gs"))
    for j in range(1, len(dropSubRegion.options) - 1):
        dropSubRegion = Select(driver.find_element(By.NAME, "gs"))
        dropSubRegion.select_by_index(j)
        subregion_name = dropSubRegion.first_selected_option.text
        driver.find_element(By.NAME, "go").click()
        driver.find_element(By.LINK_TEXT, "сайт избирательной комиссии субъекта Российской Федерации").click()
        wait_for_page_load(driver)
        try:
            driver.find_element(By.LINK_TEXT, "Сводная таблица итогов голосования").click()
        except Exception:
            driver.find_element(By.LINK_TEXT, "Сводная таблица предварительных итогов голосования").click()
        wait_for_page_load(driver)
        try:
            table_xpath = """/html/body/table[3]/tbody/tr[4]/td/table[6]/tbody/tr/td[2]/div/table/tbody"""
            result_table = driver.find_element(By.XPATH, table_xpath)
        except Exception:
            table_xpath = """/html/body/table[4]/tbody/tr[4]/td/table[6]/tbody/tr/td[2]/div/table/tbody"""
            result_table = driver.find_element(By.XPATH, table_xpath)

        rows = result_table.find_elements(By.TAG_NAME, "tr")

        # Save subregion table with results as csv file
        with open(f"""tables\{region_name.replace(" ", "_")}__{subregion_name.replace(" ", "_")}.csv', 'w+""",
                  encoding='utf8') as csvfile:
            csvwriter = csv.writer(csvfile)
            for row in rows:
                cell_numbers = [cell_number.text for cell_number in row.find_elements(By.TAG_NAME, "nobr")]
                csvwriter.writerow(cell_numbers)

        driver.back()  # Get back from table view
        driver.back()  # Get back from subregion website
        driver.back()  # Get back from subregion on main website
    driver.back()  # Get back to root to change region
driver.close()
