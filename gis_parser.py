import contextlib
import multiprocessing as mp
import sys

import numpy as np
import pandas as pd
from fuzzywuzzy import process
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import Select, WebDriverWait


def parse_response(text):
    lines = text.split("\n")
    uik_num = lines[1][lines[1].find("№") + 1:].strip()
    uik_address = lines[3][lines[3].find(":") + 1:].strip()
    uik_phone = lines[4][lines[4].find(":") + 1:].strip()
    return uik_num, uik_address, uik_phone


def retrieve_adress(df: pd.DataFrame, file_chunk: int):
    errors = 0
    driver = webdriver.Firefox()
    driver.get(ROOT_URL)
    dropRegion = Select(driver.find_element(By.NAME, "subject"))
    regions = [x.text for x in dropRegion.options][1:]
    geo_uik_data = pd.DataFrame(columns=['uik', 'region', 'address', 'phone'])

    for i, ( _ , row) in enumerate(df.iterrows()):
        try:
            driver.get(ROOT_URL)
            input_uik = driver.find_element(By.NAME, "uik")
            input_uik.send_keys(row['уик'])
            dropRegion = Select(driver.find_element(By.NAME, "subject"))
            region = process.extractOne(row['регион'], regions)[0]
            dropRegion.select_by_visible_text(region)
            send_request_button = driver.find_element(By.LINK_TEXT, "Отправить запрос")
            send_request_button.click()
            result = driver.find_element(By.CLASS_NAME, 'dotted')
            if not NO_DATA_WARNING in result.text:
                parsed_data = parse_response(result.text)
                geo_uik_data.loc[i] = (parsed_data[0], region, parsed_data[1], parsed_data[2])
                geo_uik_data.to_csv(f"geo_data_{file_chunk}.csv", encoding='utf8')
            else:
                print(f"WARNING! {region} {row['уик']} is missing!", file=sys.stderr)
                errors += 1
        except Exception as inst:
            print(type(inst), file=sys.stderr)
            try:
                driver.close()
            except Exception as inst2:
                print(type(inst), file=sys.stderr)
            driver = webdriver.Firefox()

    return geo_uik_data


NO_DATA_WARNING = """Информируем Вас, что сведения об избирательном участке по введенным Вами данным в системе ГАС "ВЫБОРЫ" на момент создания запроса отсутствуют."""
ROOT_URL = "http://cikrf.ru/services/lk_address/?do=find_by_uik"
uik_data = pd.read_csv("final_table.csv", encoding='utf8')
uik_chunks = np.array_split(uik_data, 3)

if __name__ == '__main__':
    pool = mp.Pool(processes=3)
    results = [pool.apply_async(retrieve_adress, args=(uik_chunks[x], x)) for x in range(3)]
    output = [p.get() for p in results]
    output = pd.concat(output)
    output.to_csv("addresses.csv", encoding='utf8')
