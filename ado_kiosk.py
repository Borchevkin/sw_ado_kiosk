import time
import os
from dotenv import load_dotenv
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains

class AdoDashboard():
    def __init__(self, login, password, url):
        self.login = login
        self.password = password
        self.url = url

        self.InitWebdriver()

    def InitWebdriver(self):
        '''
        Setup driver for start in kiosk mode

        (None) -> None
        '''

        chrome_options = webdriver.ChromeOptions()

        # Disable "Controlled by automation popup" and "Developer mode extensions" popup
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'load-extension'])

        # Start chromium in kiosk mode
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument("--disable-password-manager-reauthentication")

        # Disable popup "Save credentials"
        prefs = {"profile.password_manager_enabled" : False, "credentials_enable_service": False}
        chrome_options.add_experimental_option("prefs", prefs)
    
        self.driver = webdriver.Chrome(options=chrome_options)

    def InputLogin(self):
        '''
        Input login to login form

        (None) -> None
        '''

        try:
            loginField = self.driver.find_element_by_name('loginfmt')
            loginField.send_keys(self.login)
            loginField.send_keys(Keys.RETURN)
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def InputPassword(self):
        '''
        Input pass to login form

        (None) -> None
        '''

        try:
            passField = self.driver.find_element_by_name('passwd')
            passField.send_keys(self.password)
            passField.send_keys(Keys.RETURN)
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def Goto(self, url):
        '''
        Go to specific url

        (str) -> None
        '''

        self.driver.get(url)

    def Maximize(self):
        '''
        Maximize dashboard by clicking approtiate button on UI

        (None) -> None
        '''

        # fullscreen-dashboard-button class
        try:
            buttons = self.driver.find_elements_by_class_name('fullscreen-dashboard-button')
            if len(buttons) >= 1:
                buttons[0].click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def Refresh(self):
        '''
        Refresh the dashboard using approtiate button

        (None) -> None
        '''

        # refresh-dashboard-button class
        try:
            buttons = self.driver.find_elements_by_class_name('refresh-dashboard-button')
            if len(buttons) >= 1:
                buttons[0].click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def HideMouseCursor(self):
        '''
        Hide mouse cursor

        (None) -> None
        '''

        import pyautogui
        max_x, max_y = pyautogui.size()
        pyautogui.moveTo(max_x - 1, max_y - 1)

    def Open(self):
        '''
        Open dashboard in browser
        '''

        self.HideMouseCursor()

        self.Goto(self.url)
        time.sleep(10)
        self.InputLogin()
        time.sleep(10)
        self.InputPassword()
        time.sleep(10)
        self.Maximize()
        time.sleep(10)
        self.Refresh()

def main():
    load_dotenv()

    url = os.getenv("ADO_KIOSK_URL")
    login = os.getenv("ADO_KIOSK_LOGIN")
    password = os.getenv("ADO_KIOSK_PASSWORD")
    refresh_rate = int(os.getenv("ADO_KIOSK_REFRESH_RATE_SEC"))

    #TODO add env checking 

    dashboard = AdoDashboard(login, password, url)
    dashboard.Open()

    while(1):
        time.sleep(refresh_rate)
        dashboard.Refresh()

if __name__ == "__main__":
    main()