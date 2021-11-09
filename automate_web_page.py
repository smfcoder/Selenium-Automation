from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome('../Driver/chromedriver')

driver.get('https://demoqa.com/books')

def searchBook():
    #driver.find_element_by_id('gotoStore').click()
    
    #(//ul[@class="menu-list"]/li)[32]

    menu = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[6]/span/div/div[1]").click()
    hidden_submenu = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[6]/div/ul/li[3]").click()
    
    # actions = ActionChains(driver)
    # actions.move_to_element(menu)
    # actions.click(menu)
    # actions.click(hidden_submenu)
    # actions.perform()
    # time.sleep(5)
    # driver.find_element_by_xpath('(//*[text()="Profile"])[2]').click()
    # #driver.get('https://demoqa.com/profile')
    
    # searchBox = driver.find_element_by_xpath('//input[@id="searchBox"]')
    # searchBox.send_keys('speaking')
    # driver.find_element_by_xpath('//*[@id="delete-record-undefined"]').click()
    #time.sleep(5)


try:
    driver.implicitly_wait(10)
    driver.find_element_by_id('login').click()

    driver.find_element_by_xpath('//input[@id="userName"]').send_keys('shreyas')
    driver.find_element_by_xpath('//input[@id="password"]').send_keys('Qwerty@123')

    driver.find_element_by_id('login').click()

    logged_username = driver.find_element_by_id('userName-value')
    if logged_username.text == 'shreyas':
        print("logged successfully")

        #searching the book
        searchBook()

    else:
        print("Error in logging - Inavlid Credentials")
        driver.close()
        exit(1)
except Exception as e:
    print(e)
    print("Error at Login")
    driver.close()