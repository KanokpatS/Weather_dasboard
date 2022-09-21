import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

def choose_webpage(month: str, day: str):
    """
    Choose webpage html from month and date
    :param month: Month that you want a weather data
    :param day: Day that you want a weather data
    :return: HTML of webpage
    """
    driver = webdriver.Chrome(executable_path=r'D:\AltoTech\weather\chromedriver.exe')
    driver.get('https://www.tmd.go.th/climate/climate.php?FileID=1')
    month_select = Select(driver.find_element_by_xpath("/html/body/center/div[1]/div[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/select[2]"))
    month_select.select_by_value(month)
    day_select = Select(driver.find_element_by_xpath("/html/body/center/div[1]/div[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/select[1]"))
    day_select.select_by_value(day)
    data = driver.page_source
    return data

def scrape_data(data: str, month: str, day:str) -> dict:
    """
    Scrape webpage and clean data
    :param data: HTML of webpage
    :param month: Month that you want a weather data
    :param day: Day that you want a weather data
    :return: Dictionary of weather data
    """
    soup = BeautifulSoup(data, "html.parser")
    values = soup.find_all('tr', {"class": ["RDS", "RADS"]})
    weather_dict = dict()
    for div in values:
        province = div.find('td').text
        temp_high = div.find('td').findNext('td').text
        temp_low = div.find('td').findNext('td').findNext('td').text
        wind = div.find('td').findNext('td').findNext('td').findNext('td').findNext('td').text
        rain = div.find('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').text
        date = month + '-' + day
        check = div.find('td').findNext('td').findNext('td').findNext('td').text
        weather_dict[province] = [date, temp_high, temp_low, wind, rain]
        if temp_high == '- ยังไม่ได้รับรายงาน -':
            weather_dict[province] = [date, '', '', '', '']
        if check == '- ได้รับรายงานบางส่วน -':
            rain = div.find('td').findNext('td').findNext('td').findNext('td').findNext('td').text
            weather_dict[province] = [date, temp_high, temp_low, '', rain]
    return weather_dict

def dict_to_df(weather_dict: dict) -> pd.DataFrame:
    """
    Transform dictionary to dataframe
    :param weather_dict: Dictionary of weather data
    :return: Weather dataframe
    """
    df = pd.DataFrame.from_dict(weather_dict, orient='index', columns=['date', 'temp_high', 'temp_low', 'wind', 'rain'])
    return df

if __name__ == "__main__":
    month = "2022-07"
    days = list(range(1,32))
    df_all = pd.DataFrame()
    for day in days:
        print(f'Start {month}-{day}')
        data = choose_webpage(month, str(day))
        weather_dict = scrape_data(data, month, str(day))
        df = dict_to_df(weather_dict)
        df_all = pd.concat([df_all, df])
        print(df.shape)
        print(f'Finish {month}-{day}')
        time.sleep(5)
    print(df_all)
    df_all.to_excel("weather_data3.xlsx")