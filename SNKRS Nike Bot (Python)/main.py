from selenium import webdriver




driver = webdrive.Chrome()
driver = driver.get('https://www.nike.com/launch')
driver.maximize_window()   

try:
    login(driver=driver, username=username, password=password)
except TimeoutException:
    LOGGER.info("Failed to login due to timeout. Retrying...")
    skip_retry_login = False
except Exception as e:
    LOGGER.exception("Failed to login: " + str(e))
    six.reraise(Exception, e, sys.exc_info()[2])

login_or_signup_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/div/ul/li[1]/button')
