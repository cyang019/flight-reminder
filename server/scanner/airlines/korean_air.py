from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import sys
from bs4 import BeautifulSoup
import time
import numpy as np
from datetime import datetime
from scanner.common import send_keys_delay_random
from flights_db import insert_to_db
import re



def search_korean_air_once(driver, orig, dest, date):
    time.sleep(0.4)
    cnt = 0
    while cnt < 10:
        try:
            oneWayRadioBtn = driver.find_element_by_xpath('//*[@id="oneway"]')
            oneWayRadioBtn.click()
        except Exception as e:
            time.sleep(np.random.uniform(low=3, high=7))
            cnt += 1
        else:
            break
    time.sleep(1)

    def fill_bookflight_form():
        time.sleep(0.6)
        fromInput = driver.find_element_by_xpath('//*[@id="from-to-chooser"]/div[2]/ul/li/div/div/div/input')
        fromInput.clear()
        time.sleep(0.7)
        send_keys_delay_random(fromInput, orig)

        toInput = driver.find_element_by_xpath('//*[@id="from-to-chooser"]/div[2]/ul/li[2]/div/div/div/input')
        toInput.clear()
        time.sleep(0.3)
        send_keys_delay_random(toInput, dest)

        dateInput = driver.find_element_by_xpath('//*[@id="from-to-chooser"]/div[2]/ul/li[3]/div/input')
        dateInput.clear()
        time.sleep(0.9)
        send_keys_delay_random(dateInput, date)
        time.sleep(1.2)
    
    def validate_bookflight_form():
        fromInput = driver.find_element_by_xpath('//*[@id="from-to-chooser"]/div[2]/ul/li/div/div/div/input')
        same_from = fromInput.get_attribute('value') == orig

        toInput = driver.find_element_by_xpath('//*[@id="from-to-chooser"]/div[2]/ul/li[2]/div/div/div/input')
        same_to = toInput.get_attribute('value') == dest

        dateInput = driver.find_element_by_xpath('//*[@id="from-to-chooser"]/div[2]/ul/li[3]/div/input')
        same_date = dateInput.get_attribute('value') == date
        return same_from and same_to and same_date

    fill_bookflight_form()
    time.sleep(1)
    while not validate_bookflight_form():
        try:
            print('form contains incorrect entries, try to fill again...')
            fill_bookflight_form()
            time.sleep(1)
        except Exception as e:
            print(e)
            raise e

    findFlightsBtn = driver.find_element_by_xpath('//*[@id="submit"]')
    findFlightsBtn.click()
    
    time.sleep(1.1)
    # airMessageCheckBox = driver.find_element_by_xpath('//*[@id="airpmessage-checkbox"]')
    # airMessageCheckBox.click()
    # time.sleep(0.521)
    airMessageConfirmBtn = driver.find_element_by_xpath('//*[@id="btnModalPopupYes"]')
    airMessageConfirmBtn.click()
    time.sleep(1.6)
    cnt = 0
    while cnt < 10:
        notFoundMessageBtnExist = driver.find_elements_by_xpath('//*[@id="btnModalPopupYes"]')
        if not notFoundMessageBtnExist:
            cnt += 1
            time.sleep(np.random.uniform(low=2, high=4))
        else:
            break
            
    if not notFoundMessageBtnExist:
        t = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        print("[{}] Found flight for {}-{} on {}.".format(t, orig, dest, date))
        return True
    else:
        notFoundMessageBtn = notFoundMessageBtnExist[0]
        notFoundMessageBtn.click()
        return False


def search_korean_air_second_round(driver, orig, dest, date):
    cnt = 0
    while cnt < 5:
        print(f'try [{cnt}]...')
        try:
            oneWayRadioBtn = driver.find_element_by_xpath('//*[@id="from-to-chooser"]/div[1]/ul/li/input')
        except Exception as e:
            time.sleep(np.random.uniform(low=2, high=4))
        else:
            break
        cnt+=1
    print('proceed to search page...')
    oneWayRadioBtn.click()
    
    def fill_bookflight_form():
        time.sleep(2)
        fromInput = driver.find_element_by_xpath('//*[@id="boundList"]/ul/li[1]/div/div/div/input')
        fromInput.clear()
        time.sleep(0.7)
        send_keys_delay_random(fromInput, orig)
        time.sleep(1.1)
        
        toInput = driver.find_element_by_xpath('//*[@id="boundList"]/ul/li[2]/div/div/div/input')
        toInput.clear()
        time.sleep(0.91)
        send_keys_delay_random(toInput, dest)
        time.sleep(0.21)
        
        dateInput = driver.find_element_by_xpath('//*[@id="boundList"]/ul/li[3]/div/input')
        dateInput.clear()
        time.sleep(0.9)
        send_keys_delay_random(dateInput, date)
        time.sleep(1)
        try:
            currencyUSDRadioBtn = driver.find_element_by_xpath('//*[@id="currency_USD"]')
            currencyUSDRadioBtn.click()
        except Exception as e:
            pass
        time.sleep(1.5)

    def validate_bookflight_form():
        fromInput = driver.find_element_by_xpath('//*[@id="boundList"]/ul/li[1]/div/div/div/input')
        same_from = fromInput.get_attribute('value') == orig

        toInput = driver.find_element_by_xpath('//*[@id="boundList"]/ul/li[2]/div/div/div/input')
        same_to = toInput.get_attribute('value') == dest

        dateInput = driver.find_element_by_xpath('//*[@id="boundList"]/ul/li[3]/div/input')
        same_date = dateInput.get_attribute('value') == date

        return same_from and same_to and same_date

    fill_bookflight_form()
    time.sleep(1)
    while not validate_bookflight_form():
        try:
            print('form contains incorrect entries, try to fill again...')
            fill_bookflight_form()
            time.sleep(1)
        except Exception as e:
            print(e)
            raise e

    submitBtn = driver.find_element_by_xpath('//*[@id="submit"]')
    submitBtn.click()
    
    time.sleep(1.1)
    # //*[@id="btnModalPopupYes"]
    airMessageConfirmBtn = driver.find_element_by_xpath('//*[@id="btnModalPopupYes"]')
    airMessageConfirmBtn.click()
    time.sleep(1.6)
    cnt = 0
    while cnt < 10:
        notFoundMessageBtnExist = driver.find_elements_by_xpath('//*[@id="btnModalPopupYes"]')
        if not notFoundMessageBtnExist:
            cnt += 1
            time.sleep(np.random.uniform(low=2, high=4))
        else:
            break
            
    if not notFoundMessageBtnExist:
        t = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        print("[{}] Found flight for {}-{} on {}.".format(t, orig, dest, date))
        return True
    else:
        notFoundMessageBtn = notFoundMessageBtnExist[0]
        notFoundMessageBtn.click()
        return False


def get_flight_info_from_flight_item_html(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')
    flight_fare_str = soup.find(class_='flight-fare-passenger-type').text.strip()
    if 'unavailable' in flight_fare_str:
        return None
    pattern = r'([a-zA-Z]+) ([0-9\.,]+)'
    found = re.search(pattern, flight_fare_str)
    try:
        currency, val = found.group(1), found.group(2)
        flight_fare = f'{currency} {val}'
    except Exception as e:
        print(e)
        return None
    
    print('flight_fare: {}'.format(flight_fare))
    flight_summary = soup.find(class_='flight-summary')
#     flight_date = flight_summary.find(class_='flight-date').text.strip()
#     print('flight_date: {}'.format(flight_date))
#     flight_time = flight_summary.find(class_='flight-time').text.strip()
#     print('flight_time: {}'.format(flight_time))
    flight_total_time = flight_summary.find(class_='flight-total-time').text.strip()
    print('flight_total_time: {}'.format(flight_total_time))
    flight_stop = flight_summary.find(class_='flight-stop').text.strip()
    print('flight_stop: {}'.format(flight_stop))
    flight_number = soup.find(class_='flight')['data-flight-number'].strip()
    print('flight_number: {}'.format(flight_number))
    flight_class_str = soup.find(class_='planeType').text.strip()
    found = re.search(r'([0-9a-zA-Z\-]+)', flight_class_str)
    flight_class = found.group(1)
    print(f'flight_class: {flight_class}')
    flight_route_from, flight_from_time = soup.find(class_='route from').text.strip().split()
    flight_route_to, flight_to_time = soup.find(class_='route to').text.strip().split()
    print('{} {} -> {} {}'.format(flight_route_from, flight_from_time, flight_route_to, flight_to_time))
    result = {
        'flight_fare': flight_fare,
        'flight_duration': flight_total_time,
        'flight_stop': flight_stop,
        'flight_number': flight_number,
        'flight_class': flight_class,
        'flight_from': flight_route_from,
        'flight_to': flight_route_to,
        'flight_from_time': flight_from_time,
        'flight_to_time': flight_to_time,
        'timestamp': datetime.now()
    }
    return result


def get_korean_air_flight_info(driver, orig, dest, date):
    time.sleep(2.11)
    
    dates_table = driver.find_element_by_tag_name('tbody')
    dates_columns = dates_table.find_elements_by_tag_name('td')
    # try to find the date
    date_parts = date.split('-')
    date_attr = ''.join(date_parts)
    radioInputBtn = None
    for col in dates_columns[1:]:
        try:
            col.find_element_by_xpath(f'//td[@data-outbound]="{date_attr}"')
            print('found the actual date.')
            radioInputBtn = col.find_element_by_tag_name('input')
            break
        except NoSuchElementException as e:
            pass
    if radioInputBtn is not None:
        radioInputBtn.click()
    else:
        for col in dates_columns[1:]:
            try:
                radioInputBtn = col.find_element_by_tag_name('input')
                new_date_str = radioInputBtn.get_attribute('id')
                date_id_pattern = r'fare-(\d{4})(\d{2})(\d{2})'
                found = re.search(date_id_pattern, str(new_date_str))
                year, month, day = found.group(1), found.group(2), found.group(3)
                radioInputBtn.click()
                print(f'found another date: {year}-{month}-{day}')
                date = f'{year}-{month}-{day}'
                break
            except NoSuchElementException as e:
                print(col.text)
                time.sleep(0.1)
    try:
        continueBtn = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button')
        # continueBtn.click()
    except NoSuchElementException as e:
        print('No dates available...')
        return []
    continueBtn.click()
    cnt = 0
    time.sleep(np.random.uniform(low=2, high=6))
    while cnt < 5:
        try:
            header = driver.find_element_by_xpath('//*[@id="other-pannel"]/div[1]')
        except Exception as e:
            time.sleep(np.random.uniform(low=2, high=6))
            cnt += 1
            print('no table found...')
        else:
            break
    
    print('flight details page loaded...')
    
    time.sleep(np.random.uniform(low=2, high=4))
    
    # After continue, to a new page
    flight_info_list = []
    flight_items = driver.find_elements_by_class_name('flightItem')
    print('found flight items...')
    
    for flight_item in flight_items:
        temp_html = flight_item.get_attribute('innerHTML')
        flight_info = get_flight_info_from_flight_item_html(temp_html)
        
        if flight_info is not None:
            print(flight_info)
            flight_info['date'] = date
            flight_info_list.append(flight_info)
    return flight_info_list


def search_korean_air_date_range(orig, dest, dates, db_name):
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.delete_all_cookies()
    driver.set_window_size(1280, 960)
    url = "https://www.koreanair.com/global/en.html"
    driver.get(url)
    while True:
        try:
            time.sleep(2.5)
            driver.find_element_by_class_name('book-flight')
            break
        except NoSuchElementException as e:
            pass
    results = []
    firstRound = True
    for i, date in enumerate(dates):
        time.sleep(np.random.uniform(low=2, high=6))
        params = {
            'orig': orig,
            'dest': dest,
            'date': date
        }
        if i == 0 or firstRound:
            found = search_korean_air_once(driver, **params)
            firstRound = False
        else:
            found = search_korean_air_second_round(driver, **params)
        if found:
            result = get_korean_air_flight_info(driver, **params)
            if len(result) > 0:
                for line in result:
                    print(f"{line['date']} {line['flight_number']} {line['flight_fare']}")
                    insert_to_db(db_name, **line)
                    print(f'flight saved to {db_name} db')
            firstRound = True
            driver.get(url)
        else:
            print(f'did not find {orig} to {dest} for {date}...')
    driver.quit()
    return


