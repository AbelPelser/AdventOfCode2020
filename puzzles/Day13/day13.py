import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from util import read_input_as_lines


def parse_input(lines):
    return int(lines[0]), lines[1].split(',')


def part2():
    _, bus_ids = parse_input(read_input_as_lines())
    input_components = [f'(t + {i}) mod {int(bus_id)} = 0' for i, bus_id in enumerate(bus_ids) if bus_id != 'x']
    input_str = ', '.join(input_components)

    # Make sure you have the latest geckodriver (https://github.com/mozilla/geckodriver/releases) and add it to PATH
    # Also make sure to replace os.environ[...] with the path to a valid Firefox profile,
    # such as /home/username/.mozilla/firefox/a123bc45.Selenium
    os.environ['SELENIUM_FP'] = '/home/abel/.mozilla/firefox/i523wi41.Selenium'
    fp = webdriver.FirefoxProfile(os.environ['SELENIUM_FP'])
    driver = webdriver.Firefox(fp)
    try:
        driver.get('https://www.wolframalpha.com/')

        input_elem = driver.find_element_by_class_name('_2oXzi')
        input_elem.send_keys(input_str)
        driver.find_element_by_css_selector('button._10um4._2DVTv.HuMWM').click()
        header_xpath = "//h2[contains(text(),'Integer solution:')]"
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, header_xpath)))
        elem = driver.find_element_by_xpath(header_xpath)
        while elem.tag_name != 'section':
            elem = elem.find_element_by_xpath('./..')
        result_img_elem = elem.find_element_by_tag_name('img')
        result_str = result_img_elem.get_attribute('alt')
        result = result_str.split(',')[0].split('+')[-1].strip()
        return int(result)
    finally:
        driver.quit()


def part1():
    earliest_leave, bus_ids = parse_input(read_input_as_lines())
    bus_ids = sorted(list(map(lambda s: int(s), filter(lambda s: s.isdigit(), bus_ids))))
    leave_minute = earliest_leave
    buses_leaving = []
    while len(buses_leaving) != 1:
        leave_minute += 1
        buses_leaving = list(filter(lambda bus_id: leave_minute % bus_id == 0, bus_ids))
    return buses_leaving[0] * (leave_minute - earliest_leave)


if __name__ == '__main__':
    print(part1())
    print(part2())
