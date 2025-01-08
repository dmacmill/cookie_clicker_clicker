import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.building import BuildingElement


class CookieClickerClicker:
    def __init__(self):
        """
        CookieClickerClicker, a complete bot for the game Cookie Clicker.

        On init, will automatically start selenium webdriver for Chrome, and will assure the 
        page loads.
        """
        # start webdriver
        self.driver = webdriver.Chrome()
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        assert "Cookie Clicker" in self.driver.title
        assert "No results found" not in self.driver.page_source

        # Generic errors selenium throws
        self.errors = [
            NoSuchElementException, 
            ElementNotInteractableException,
            StaleElementReferenceException
        ]

    def lang_select(self, lang):
        """
        Waits for the language select screen to appear in cookie clicker, then clicks on the 
        element with the desired language id.

        Args:
            lang (str): The desired language id. "langSelect-EN" is the english option.
        """
        # Wait for lang box, then click english
        wait = WebDriverWait(
            self.driver, 
            timeout=5, 
            poll_frequency=0.5,
            ignored_exceptions=self.errors
        )
        wait.until(lambda d : d.find_element(By.ID, lang).click() or True)

    def ready_elements(self):
        """
        Gets us past React loading and initializes elements such as the cookie, store, and 
        upgrades.
        """
        wait = WebDriverWait(
            self.driver, 
            timeout=5, 
            poll_frequency=0.5,
            ignored_exceptions=self.errors
        )

        # Wait for cookie to first appear
        wait = WebDriverWait(
            self.driver,
            timeout=30,
            poll_frequency=0.5, 
            ignored_exceptions=self.errors
        )
        wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))
        self.cookie = self.driver.find_element(By.ID, "bigCookie")

        # wait until everything else shows up
        wait.until(EC.presence_of_element_located((By.ID, "upgrades")))
        wait.until(EC.presence_of_element_located((By.ID, "shimmers")))
        wait.until(EC.presence_of_element_located((By.ID, "products")))

        # Hard wait for longer because there is recreation of elements happening in React.
        # TODO: find a better way to handle this.
        time.sleep(1)

        # Cookie (again because it might be stale)
        wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))
        self.cookie = self.driver.find_element(By.ID, "bigCookie")

        # Shimmers
        wait.until(EC.presence_of_element_located((By.ID, "shimmers")))
        self.shimmers = self.driver.find_element(By.ID, "shimmers")

        # Store
        wait.until(EC.presence_of_element_located((By.ID, "store")))
        self.store = self.driver.find_element(By.ID, "store")

        # Upgrades
        wait.until(EC.presence_of_element_located((By.ID, "upgrades")))
        self.upgrades_box = self.store.find_element(By.ID, "upgrades")

    def prepare_buildings(self):
        # Prepare the store and buildings list
        self.buildings = {}

        # Initialize the buildings
        for i in range(0, 20):
            be = BuildingElement()
            be.element = self.store.find_element(By.ID, "product"+str(i))
            be.owned = be.element.find_element(By.ID, "productOwned"+str(i))
            # be.price = be.element.find_element(By.ID, "productPrice"+str(i))
            self.buildings[i] = be

    def update_buildings(self):
        """Called to update self.buildings in run loop.

        TODO: productPrice needs to convert text numbers to int, or get another way somehow.
        """
        elements_cheap = self.store.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled")
        elements_disabled = self.store.find_elements(By.CSS_SELECTOR, "div.product.unlocked.disabled")
        for e in elements_cheap:
            id = int(e.get_attribute("id").split("product")[1])
            self.buildings[id].element = e
            productOwned = e.find_element(By.ID, "productOwned"+str(id)).text
            productPrice = e.find_element(By.ID, "productPrice"+str(id)).text
            self.buildings[id].owned = 0 if productOwned == '' else int(productOwned)
            self.buildings[id].is_enabled = True
            # the cases "1,248", "1.2 million" need to be addressed
            # self.buildings[id].price = int(productPrice)
        for e in elements_disabled:
            id = int(e.get_attribute("id").split("product")[1])
            self.buildings[id].element = e
            productOwned = e.find_element(By.ID, "productOwned"+str(id)).text
            productPrice = e.find_element(By.ID, "productPrice"+str(id)).text
            self.buildings[id].owned = 0 if productOwned == '' else int(productOwned)
            self.buildings[id].is_enabled = False
            # the cases "1,248", "1.2 million" need to be addressed
            # self.buildings[id].price = int(productPrice)

    def run(self):
        """
        Start a thread for checking + buying buildings, and the main thread to handle everything else for now.
        """
        # Threaded function to handle buying buildings
        def handle_buildings(self):
            # buy the buildings, buy the most expensive first
            self.update_buildings()
            expensive_first_buildings = list(self.buildings.values())
            expensive_first_buildings.reverse()
            for b in expensive_first_buildings:
                if b.is_enabled:
                    if 30 > b.owned:
                        b.element.click()

        def buildings_loop(self):
            while True:
                handle_buildings(self)
                time.sleep(0.5)
        
        thread = threading.Thread(target=buildings_loop, args=(self,))

        thread.start()

        # Main Game Loop
        while(True):
            # click the cookie
            self.cookie.click()
            time.sleep(0.01)

            # buy the upgrades
            upgrades_list = self.upgrades_box.find_elements(By.TAG_NAME, "div")
            for upgrade in upgrades_list:
                try:
                    if "enabled" in upgrade.get_attribute("class"):
                        upgrade.click()
                except (StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException) as e:
                    pass

            # click the golden cookies if they are there
            goldenCookies = self.shimmers.find_elements(By.TAG_NAME, "div")
            for gc in goldenCookies:
                try:
                    gc.click()
                except (StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException) as e:
                    pass
    
    def close(self):
        self.driver.close()


if __name__ == "__main__":
    cca = CookieClickerClicker()
    cca.lang_select("langSelect-EN")
    cca.ready_elements()
    cca.prepare_buildings()
    cca.run()  # should just run forever or crash
    cca.close()