import requests
import pyautogui
from httpcore import TimeoutException
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from monad_bot.data.config import PROFILE


import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)



class AdsPowerProfile:
    API_URL = "http://local.adspower.net:50325"

    def __init__(self, user_id, address):
        self.user_id = user_id
        self.address = address
        self.driver = None

    def OpenProfile(self):
        try:
            response = requests.get(self.API_URL + f"/api/v1/browser/start?user_id={self.user_id}", timeout=10)
            response.raise_for_status()
        except (requests.exceptions.RequestException, TimeoutException) as e:
            logging.error(f"Ошибка подключения к API: {e}")
            return

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            logging.error("Ошибка: API вернул некорректный JSON")
            return

        if data.get("code") != 0:
            print(f"Ошибка API: {data.get('msg', 'Неизвестная ошибка')}")
            return


        chrome_driver = data["data"]["webdriver"]
        debugg = data["data"]["ws"]["selenium"]

        options = webdriver.ChromeOptions()
        options.debugger_address = debugg

        service = Service(chrome_driver)


        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_window_size(1620, 1080)

        logging.info(f"Браузер AdsPower {self.user_id} запущен!")

    def FaucetBot(self, error_selector=None):
        if self.driver is None:
            logging.error("Ошибка: браузер не запущен!")
            return

        url = "https://testnet.monad.xyz/"


        logging.info(f"Открываем {url} для {self.address}...")
        self.driver.get(url)

        try:
            try:
                back_element = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome to Monad Testnet')]")
                logging.info("Заголовок найден!")

                try:
                    button_accept = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "terms-accepted"))
                    )
                    button_accept.click()
                    logging.info("Успешно поставлена галочка")

                    button_continue = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
                    )
                    button_continue.click()
                    logging.info("Нажали продолжить")

                except TimeoutException:
                    logging.warning("Кнопки не найдены, продолжаем выполнение...")

            except NoSuchElementException:
                logging.info("Заголовок не найден, пропускаем этот шаг.")


            self.driver.execute_script("window.scrollBy(0, 800);")

            time.sleep(5)
            input_element = self.driver.find_element(By.XPATH, "//input[contains(@class, 'rounded-md')]")
            input_element.send_keys(self.address)
            logging.info(f"Вставили адрес: {self.address}")

            time.sleep(10)
            x, y = int("1005"), int("620")
            pyautogui.click(x=x, y=y)
            logging.info("Поставили галочку")

            time.sleep(1)
            continue2_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Get Testnet MON')]")
            continue2_button.click()
            logging.info("Нажали на Get Testnet MON")

            time.sleep(2)
            logging.info("Успешно получили тестовые токены!")



            if error_selector:
                try:
                    error_message = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, error_selector))
                    ).text
                    logging.info(f"Ошибка: {error_message}")
                except:
                    logging.info("Ошибок нет")

        except Exception as e:
            logging.info(f"Ошибка в процессе: {e}")
            pass


    def NFTclaim(self, password, error_selector=None):
        if self.driver is None:
            logging.error("Браузер не запущен!")

        try:
            try:
                url1 = "https://testnet.freee.xyz/prime/monadt/PricklyPals"
                self.driver.get(url1)
                logging.info(f"Переходим по ссылке...: {url1}")

                time.sleep(5)
                wallet_button = self.driver.find_element(By.CLASS_NAME, "MuiButtonBase-root")
                wallet_button.click()
                logging.info("Кнопка PUBLIC FREE MINT прожата")

                time.sleep(3)
                metamask_button = self.driver.find_element(By.XPATH, "//div[contains(text(), 'MetaMask')]")
                metamask_button.click()
                logging.info("Кнопка METAMASK прожата")
            except TimeoutException:
                return



            try:
                time.sleep(5)
                pyautogui.write(password, interval=0.1)
                logging.info("Ввели пароль")

                pyautogui.press("enter")
                logging.info("MetaMask разблокирован")

                # for handle in self.driver.window_handles:
                #     self.driver.switch_to.window(handle)
                #     if "MetaMask" in self.driver.title:
                #         logging.info("Нашли окно ")
                #         break

                # connect_button = WebDriverWait(self.driver, 20).until(
                #                      EC.presence_of_element_located((By.XPATH, "//button[@data-testid='confirm-btn']"))
                #                  )
                #                  connect_button.click()

                time.sleep(5)
                button_location = pyautogui.locateCenterOnScreen("C:\\Users\\memor1u\\PycharmProjects\\mainproject\\monad_bot\\data\\connect_button.png", confidence=0.8)

                time.sleep(5)
                button_confirm_location = pyautogui.locateCenterOnScreen("C:\\Users\\memor1u\\PycharmProjects\\mainproject\\monad_bot\\data\\confirm_button.png", confidence=0.8)

                if button_location and button_confirm_location:
                    pyautogui.click(button_location)
                    logging.info("Connect прожат")
                    pyautogui.click(button_confirm_location)
                    logging.info("Confirm прожат")
                else:
                    print("Кнопка не найдена!")
                    return

                self.driver.refresh()
                time.sleep(6)

                wallet_buttons = self.driver.find_element(By.CSS_SELECTOR, "button.css-1wzdqo4")
                wallet_buttons.click()

                logging.info("1")

                wallet2_buttons = self.driver.find_element(By.CSS_SELECTOR, "button.css-10064sn")
                wallet2_buttons.click()
                logging.info("2")


                time.sleep(12)
                pyautogui.click(button_confirm_location)




                # Для дальнейших ссылок
                # url2 = ("")
                # url3 = ("")


            except Exception as e:
                logging.error("Произошла ошибка: ", e)
            # try:
            #     self.driver.switch_to.window(self.driver.window_handles[-1])
            #     logging.info("Переключились на основное окно...")
            #     mint_element = WebDriverWait(self.driver, 10).until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, ".tw-bg-button-primary"))
            #     )
            #
            #     mint_element.click()
            #     logging.info("Кнопка минта прожата")
            #     if error_selector:
            #         try:
            #             error_message = WebDriverWait(self.driver, 5).until(
            #                 EC.presence_of_element_located((By.CSS_SELECTOR, error_selector))
            #             )
            #             logging.error(f"Произошла ошибка: {error_message}")
            #         except:
            #             logging.info("Ошибок нет.")
            #
            #     for handle in self.driver.window_handles:
            #         self.driver.switch_to.window(handle)
            #         if "MetaMask" in self.driver.title():
            #             break
            #     self.driver.send_keys(By.CSS_SELECTOR, '[data-testid="confirm-footer-button"]')
            #     logging.info("Успешно заминтили NFT!")
            # except Exception as e:
            #     logging.error("Во время выполнение входа в метамаск, что-то пошло не так!: ", e)

        except Exception as e:
            logging.error("Произошла критическая ошибка", e)

    def SwapDefi(self):
        url = ""


    def run(self):
        self.OpenProfile()
        self.FaucetBot()


users = ""
address = ""
user = AdsPowerProfile(user_id=users, address=address)
user.run()