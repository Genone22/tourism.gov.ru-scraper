import pandas as pd
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import logging


data_list = []
base_url = 'https://tourism.gov.ru/reestry/reestr-gostinits-i-inykh-sredstv-razmeshcheniya/'


def extract_information_from_card(card_url):
    try:
        # Extract information from the opened card
        driver.get(card_url)
        time.sleep(1)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        info = extract_information(soup)
        data_list.append(info)
        driver.back()
        time.sleep(1)
        logging.info(f"Информация извлечена из карточки: {card_url}")
    except Exception as e:
        logging.error(f"Ошибка при извлечении информации из карточки {card_url}: {e}")


def navigate_to_next_page(page_number):
    try:
        next_page_url = f'{base_url}?ysclid=lmaljgb5nd407848580&PAGEN_1={page_number}'
        driver.get(next_page_url)
        time.sleep(2)
        logging.info(f"Переход на следующую страницу: {page_number}")
    except Exception as e:
        logging.error(f"Ошибка при переходе на следующую страницу {page_number}: {e}")


def extract_information(card):
    info = {}
    main_info_section = card.find('p', class_='info__title', string='Основная информация')
    if main_info_section:
        main_info_section = main_info_section.find_next('div', class_='info-part')
        while main_info_section:
            name_element = main_info_section.find('p', class_='info__name')
            text_element = main_info_section.find('p', class_='info__text')
            if name_element and text_element:
                name = name_element.text.strip()
                text = text_element.text.strip()
                info[name] = text
            main_info_section = main_info_section.find_next('div', class_='info-part')
    return info


def update_label_counter(current_page, total_pages):
    label_counter.config(text=f"Страница {current_page} из {total_pages}")


def start_extraction():
    num_pages = int(entry_num_pages.get())
    if 1 <= num_pages <= 20000:
        driver.get(base_url)
        data_list.clear()
        for page_number in range(1, num_pages + 1):
            update_label_counter(page_number, num_pages)  # Update the label counter
            window.update()
            print(f"Обработка страницы {page_number}")
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            cards = soup.find_all('div', class_='result-item')
            for card in cards:
                card_link = card['data-link']
                card_url = f'https://tourism.gov.ru{card_link}'
                extract_information_from_card(card_url)

            try:
                next_page_link = driver.find_element(By.CSS_SELECTOR, 'a.link__btn')
                if 'disabled' in next_page_link.get_attribute('class'):
                    break
            except NoSuchElementException:
                break

            navigate_to_next_page(page_number + 1)

        df = pd.DataFrame(data_list)
        output_file = 'Туризм_извлеченные_данные.xlsx'
        df.to_excel(output_file, index=False)
        driver.quit()
        messagebox.showinfo("Извлечение завершено", f"Данные успешно сохранены в {output_file}")
        window.destroy()
    else:
        messagebox.showerror("Неверный ввод", "Пожалуйста, введите число от 1 до 20000.")


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

logging.basicConfig(filename='логи.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

window = ThemedTk(theme="vista")
window.title("Tourism Scraping GUI By @Georgeousus")
window.geometry("300x150")

window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window.winfo_width()) // 2
y = (screen_height - window.winfo_height()) // 2
window.geometry("+{}+{}".format(x, y))

label_num_pages = ttk.Label(window, text="Введите количество страниц (1-20000):")
label_num_pages.pack(pady=10)
entry_num_pages = ttk.Entry(window)
entry_num_pages.pack(ipadx=50, ipady=5)

label_counter = ttk.Label(window, text="", font=('Arial', 8))
label_counter.pack(pady=5)

start_button = ttk.Button(window, text="Начать парсинг", command=start_extraction)
start_button.pack(pady=5)

window.mainloop()
