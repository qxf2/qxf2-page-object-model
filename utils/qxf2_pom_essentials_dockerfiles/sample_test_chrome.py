from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox") # Often needed in Docker/headless environments
options.add_argument("--disable-dev-shm-usage")
#options.add_argument("--headless") # Don't set it if you want to see test running on VNC Viewer
driver = webdriver.Chrome(options=options)
driver.get("http://www.qxf2.com")
print(driver.title)
driver.quit()
