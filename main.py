import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Настройка драйвера
driver = webdriver.Chrome()

try:
    driver.get("https://arealme.com/colors/ru/")
    logging.info("Сайт открыт")

    time.sleep(2)

    next_button = driver.find_element(By.XPATH, "//span[text()='Вперед!']/..")
    next_button.click()
    logging.info("Кнопка 'Вперед!' нажата")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'patra-color')]//div//span"))
    )

    # Начало отсчета времени
    start_time = time.time()
    timeout = 60

    while time.time() - start_time < timeout:
        spans = driver.find_elements(By.XPATH, "//div[contains(@class, 'patra-color')]//div//span")

        if spans:
            logging.info(f"Найдено {len(spans)} блоков <span> внутри вложенного <div> в <div class='patra-color'>")

            # Собрать background-color и их элементы
            background_counts = {}
            for span in spans:
                background_color = span.value_of_css_property('background-color')
                if background_color in background_counts:
                    background_counts[background_color].append(span)
                else:
                    background_counts[background_color] = [span]

            # Найти уникальный цвет
            unique_span = next((elements[0] for color, elements in background_counts.items() if len(elements) == 1),
                               None)

            # Нажать на уникальный цвет
            if unique_span:
                unique_span.click()
                logging.info("Нажат уникальный цвет")
            else:
                logging.warning("Уникальный цвет не найден, повторная попытка...")


finally:
    time.sleep(50)
    driver.quit()
    logging.info("Браузер закрыт")
