from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from funcsforspo_l.fregex.functions_re import *
from src.exceptions.exceptions import *
import pandas as pd
import streamlit as st
import json
import os

# -- GLOBAL -- #
URL_SUPORTE = f'https://api.whatsapp.com/send?phone=5511985640273'
CONFIG_PATH = os.path.abspath('bin\config.json')
BASE = os.path.abspath('base')
# -- GLOBAL -- #


class Bot:    
    def __init__(self, headless, download_files) -> None:
        # --- CHROME OPTIONS --- #
        self._options = ChromeOptions()
        
        if download_files:
            # --- PATH BASE DIR --- #
            self.__DOWNLOAD_DIR =  cria_dir_no_dir_de_trabalho_atual(dir='downloads', print_value=False, criar_diretorio=True)
            limpa_diretorio(self.__DOWNLOAD_DIR)
            self._SETTINGS_SAVE_AS_PDF = {
                        "recentDestinations": [
                            {
                                "id": "Save as PDF",
                                "origin": "local",
                                "account": ""
                            }
                        ],
                        "selectedDestinationId": "Save as PDF",
                        "version": 2,
                    }


            self._PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self._SETTINGS_SAVE_AS_PDF),
                    "savefile.default_directory":  f"{self.__DOWNLOAD_DIR}",
                    "download.default_directory":  f"{self.__DOWNLOAD_DIR}",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "profile.managed_default_content_settings.images": 2,
                    "safebrowsing.enabled": True}
                
            self._options.add_experimental_option('prefs', self._PROFILE)
        
        if headless == True:
            self._options.add_argument('--headless')
            
        self._options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        self._options.add_experimental_option('useAutomationExtension', False)
            
        self._options.add_argument('--disable-gpu')
        # self._options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        # self._options.add_argument("--disable-web-security")
        # self._options.add_argument("--allow-running-insecure-content")
        # self._options.add_argument("--disable-extensions")
        # self._options.add_argument("--start-maximized")
        # self._options.add_argument("--no-sandbox")
        # self._options.add_argument("--disable-setuid-sandbox")
        # self._options.add_argument("--disable-infobars")
        # self._options.add_argument("--disable-webgl")
        # self._options.add_argument("--disable-popup-blocking")
        # self._options.add_argument('--disable-software-rasterizer')
        # self._options.add_argument('--no-proxy-server')
        # self._options.add_argument("--proxy-server='direct://'")
        # self._options.add_argument('--proxy-bypass-list=*')
        # self._options.add_argument('--disable-dev-shm-usage')
        # self._options.add_argument('--block-new-web-contents')
        # self._options.add_argument('--incognito')
        # self._options.add_argument('–disable-notifications')
        # self._options.add_argument("--window-size=1920,1080")
        
        self.__service = Service(ChromeDriverManager().install())
        
        # create DRIVER
        self.DRIVER = Chrome(service=self.__service, options=self._options)
        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW5 = WebDriverWait(self.DRIVER, timeout=5)
        self.WDW7 = WebDriverWait(self.DRIVER, timeout=7)
        self.WDW10 = WebDriverWait(self.DRIVER, timeout=10)
        self.WDW30 = WebDriverWait(self.DRIVER, timeout=30)
        self.WDW = self.WDW7

        self.DRIVER.maximize_window()
        return self.DRIVER

    def quit_web(self):
        self.DRIVER.quit()
        
# UTILS #
def faz_log_st(info):
    st.markdown(f'*`{info}`*')
# UTILS #