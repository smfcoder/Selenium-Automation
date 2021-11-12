
def take_screenshot(driver):
    s = driver.get_window_size()
    #obtain browser height and width
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    #set to new window size
    driver.set_window_size(w, h)
    #obtain screenshot of page within body tag
    driver.find_element_by_tag_name('body').screenshot("ss1.png")
    driver.set_window_size(s['width'], s['height'])