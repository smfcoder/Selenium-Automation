from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime
from Modules.create_excel import create_excel_sheet
from Modules.create_screenshot import take_screenshot
from Modules.create_screenshots_word import wordDocument



#global parameters

#1
#supress warning in cmd(to again view the warnings change ignore to default)
import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
#2
wd = wordDocument()




def document_process(image_heading):
    if os.path.isfile('./ss1.png'):
        if wd.insertImage(image_heading,'./ss1.png'):
            os.remove('./ss1.png')
    else:
        print("Error in saving screenshot")



def addBook(driver):

    add_book_to_profile = False
    go_to_store_button = driver.find_element_by_xpath('//button[@id="gotoStore"]')
    driver.execute_script("arguments[0].click();", go_to_store_button)
    
    searchBox = driver.find_element_by_xpath('//input[@id="searchBox"]')
    searchBox.send_keys('speaking')

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Speaking JavaScript"]')))
    driver.find_element_by_xpath('//a[text()="Speaking JavaScript"]').click()
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//button[@id="addNewRecordButton"])[2]')))
    add_to_collection_button = driver.find_element_by_xpath('(//button[@id="addNewRecordButton"])[2]')
    driver.execute_script("arguments[0].click();", add_to_collection_button)
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        
        take_screenshot(driver)
        document_process("Speaking JavaScript book added to profile from BookStore")
        
        add_book_to_profile = True
        print("Add Book to profile alert accepted")
    except:
        print("Unable to accept add book to profile alert")
        message = "Unable to accept add book to profile alert"
    
    #validate if book is successfully added to profile

    #moving to profile page
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[6]/div/ul/li[3]")))
    hidden_submenu = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[6]/div/ul/li[3]")
    driver.execute_script("arguments[0].click();", hidden_submenu)

    #searching the book
    try:
        searchBox = driver.find_element_by_xpath('//input[@id="searchBox"]')
        searchBox.send_keys('speaking')

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Speaking JavaScript"]')))
        driver.find_element_by_xpath('//a[text()="Speaking JavaScript"]').click()

        ISBN_number = driver.find_element_by_xpath('(//*[@id="userName-value"])[1]').text
        print(ISBN_number)
        if ISBN_number == '9781449365035':
            last_step = "Ok"
            print("Last step: " + last_step)
            take_screenshot(driver)
            document_process("Verifying ISBN number")
            driver.quit()
            return(True,"OK")
            
    except:
        print("Book not added to profile during validation")
        message = "Book not added to profile during validation"
    return False,message



def searchBook(driver):
    #moving to profile page
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[6]/div/ul/li[3]")))
    hidden_submenu = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[1]/div/div/div[6]/div/ul/li[3]")
    driver.execute_script("arguments[0].click();", hidden_submenu)


    #searcing the book in profile
    try:
        add_book_to_profile = False
        searchBox = driver.find_element_by_xpath('//input[@id="searchBox"]')
        searchBox.send_keys('speaking')
        driver.find_element_by_xpath('//*[@id="delete-record-undefined"]').click()
        
        try:
            driver.find_element_by_id('closeSmallModal-ok').click()
            WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert.accept()
            delete_book_from_profile = True
            take_screenshot(driver)
            document_process("Speaking JavaScript Book deleted from profile")
            print("Book delete alert accepted")
            
        except:
            print("Unable to accept book delete alert")
            message = "Unable to accept book delete alert"
    except Exception as e:
        print("Book not found")
        message = "Book not found"
        print(e)
        driver.quit()
    if delete_book_from_profile:
        stat,res = addBook(driver)
        if stat:
            return True,res
        else:
            return False,res

#execution of file - start

def perform_automation():
    try:
        time_start = time.perf_counter()
        

        driver = webdriver.Chrome(executable_path='./Driver/chromedriver')
        driver.implicitly_wait(10)

        #validation starts
        application_url = 'https://demoqa.com/books'
        driver.get('https://demoqa.com/books')
        get_title = driver.title
        
        wd.openWordDocument(get_title)
        
        #screenshot and document process
        take_screenshot(driver)
        document_process("Login Page")

        time.sleep(1)


        driver.find_element_by_id('login').click()

        driver.find_element_by_xpath('//input[@id="userName"]').send_keys('shreyas')
        driver.find_element_by_xpath('//input[@id="password"]').send_keys('Qwerty@123')

        driver.find_element_by_id('login').click()

        logged_username = driver.find_element_by_id('userName-value')
        if logged_username.text == 'shreyas':
            print("logged successfully")

            #searching the book
            search_the_book = True

        else:
            print("Error in logging - Inavlid Credentials")
            message = "Error in logging - Inavlid Credentials"
            driver.quit()
            status = "Not OK"
            time_end = time.perf_counter()
            validation_time = round(time_end - time_start)
            time_stamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            #now_string = now.strftime("%d/%m/%Y %H:%M:%S")
            final_result = {"Status" : status, "Comment" : message, "Validation_time" : validation_time, "Validated_at" : time_stamp, "Application_url" : application_url, "Validated_page" : get_title}
            
            
            filename = (f"report_{time_stamp}")
            create_excel_sheet(filename,final_result)
            return (final_result)
            
    except Exception as e:
        print(e)
        print("Error at Login")
        message = "Error in Logging - Please check credentials"
        driver.close()
    
    if search_the_book:
        
        take_screenshot(driver)
        document_process("Page After Login")

        main_stat,main_result = searchBook(driver)
        time_end = time.perf_counter()
        validation_time = round(time_end - time_start)
        time_stamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        filename = (f"report_{time_stamp}")
        wd.saveWordDocument(filename)    
        #now_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if main_stat:
            status = "OK"
            final_result={"Status" : status,"Comment" : "Working Fine", "Validation_time" : validation_time, "Validated_at" : time_stamp, "Application_url" : application_url, "Validated_page" : get_title}
            create_excel_sheet(filename,final_result)
            return(final_result)
        else:
            status = "Not OK"
            final_result={"Status" : status, "Comment" : main_result, "Validation_time" : validation_time, "Validated_at" : time_stamp, "Application_url" : application_url, "Validated_page" : get_title}
            create_excel_sheet(filename,final_result)
            return(final_result)
            

# print(perform_automation())
