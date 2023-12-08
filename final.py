# from selenium import webdriver

# browser = webdriver.Chrome()
# browser.get('http://selenium.dev/')
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# browser = webdriver.Chrome()

# # browser.get('http://www.yahoo.com')
# # assert 'Yahoo' in browser.title

# # elem = browser.find_element(By.NAME, 'p') 
# # elem.send_keys('seleniumhq' + Keys.RETURN)
# # browser.quit()

# while(True):
#        pass


# launchBrowser()
# import unittest
# from selenium import webdriver

# class GoogleTestCase(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Chrome()
#         self.addCleanup(self.browser.quit)

#     def test_page_title(self):
#         self.browser.get('http://www.google.com')
#         self.assertIn('Google', self.browser.title)

# if __name__ == '__main__':
#     unittest.main(verbosity=2)



# while(True):
#        pass    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector

def get_choice():
    while True:
        choice =input("Enter 'artist' to search for an artist or 'song' to search for a song: ").lower()
        if choice in ('artist','song'):
            return choice
        else:
            print("Invalid choice.")

def close_banner(driver):
     banner_close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="YQRQdqiQ_iT0eo0owsJL"]')))
     banner_close_button.click()    

driver = webdriver.Chrome()

def scraping(query,search_type):
    driver.get('https://open.spotify.com')
    # search_s = driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[2]/nav/div[1]/ul/li[2]/a')
    search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/div/div[2]/div[2]/nav/div[1]/ul/li[2]/a')))
    search_button.click()
    # search_s.send_keys(Keys.RETURN)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/nav/div[1]/ul/li[2]/a"))).click()
    db_connection = mysql.connector.connect(user = 'root',
                                            host = 'localhost',
                                            password = 'Himan1234@',
                                            database = 'db'
                                                    )
    
    cursor = db_connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS songs (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), artist VARCHAR(255), duration VARCHAR(20), album VARCHAR(255))')

    search_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/form/input')))
    # search_input = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/form/input')
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)


    if search_type=='artist':
        artist_result = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchPage"]/div/div/section[1]/div[2]/div/div/div/div[4]')))
        artist_result.click()
        time.sleep(3)

        top_5_songs = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-testid="tracklist-row"]')))[:5]
        # print
        for index, result in enumerate(top_5_songs, start=1):
            title = result.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[2]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div/a/div').text
            artist = query.capitalize()
            duration = result.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[2]/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div[4]/div').text
            player_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[2]/div[3]/div[1]/div/div[1]/div/div/div[2]/div[1]/div/div[1]/div/span')))
            player_link.click()
            time.sleep(10)
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[2]/div[3]/div[1]/div/div[1]/div/div/div[2]/div[1]/div/div[1]/div/span')))

            current_url = driver.current_url

            cursor.execute("INSERT INTO songs (title, artist, duration, songs) VALUES (%s, %s, %s, %s)", (title, artist, duration, current_url))
            db_connection.commit()

            print(f"Top {index} Song:")
            print(f"Title: {title}")
            print(f"Artist: {artist}")
            print(f"Duration: {duration}")
            print(f"Player: {current_url}")
            print("-" * 30)

            
            close_banner(driver)
            time.sleep(2)
        db_connection.close()
    
    else:
    
        search_songs = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[1]/div/div/div/div/div/a[3]/button/span')))
        search_songs.click()
        time.sleep(3)
        # search_songs.send_keys(Keys.RETURN)
        # driver.maximize_window()
        # wait = WebDriverWait(driver, 20)
        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='search-input']"))).send_keys('Let me')
        # search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "form[role='search'] input")))
        # search_input.send_keys('Let me')
        # search_input.send_keys(Keys.RETURN)
        # //*[@id="searchPage"]/div/div/div/div[1]/div[1]/div/div[3]
        search_results = driver.find_elements(By.XPATH, '//div[@data-testid="tracklist-row"]')[:5]
        for index, result in enumerate(search_results, start=1):
            title = result.find_element(By.XPATH, '//*[@id="searchPage"]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/a/div').text
            artist = result.find_element(By.XPATH, './/span[@class="Type__TypeElement-sc-goli3j-0 bDHxRN rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line"]').text   
            duration = result.find_element(By.XPATH, './/div[@class="Type__TypeElement-sc-goli3j-0 bDHxRN Btg2qHSuepFGBG6X0yEN"]').text 
            # album = result.find_element(By.XPATH,'//*[@id="searchPage"]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[3]').text
            player_link = result.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[2]/div[3]/div[1]/div/div[1]/div/div/div[2]/div[1]/div/div[1]/div/span')
            player_link.click()
            current_url = driver.current_url
            cursor.execute("INSERT INTO songs (title, artist, duration, songs) VALUES (%s, %s, %s, %s)",(title,artist,duration,current_url))

            db_connection.commit()

            print(f"Top {index} Song:")
            print(f"Title: {title}")
            print(f"Artist: {artist}")
            print(f"Duration: {duration}")
            print(f"Player: {current_url}")
            print("-" * 30)  

        db_connection.close()


    

if __name__ == "__main__":
    user_choice = get_choice()
    query = input(f"Enter the {user_choice} you want to search: ")
    scraping(query,user_choice)

    driver.quit()
   





