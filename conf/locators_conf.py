#Common locator file for all locators
#Locators are ordered alphabetically

############################################
#Selectors we can use
#ID
#NAME
#css selector
#CLASS_NAME
#LINK_TEXT
#PARTIAL_LINK_TEXT
#XPATH
###########################################

#Locators for weathershopper application - weather shopper main page(weather_shopper_main_page.py)

cart_button = "xpath,//button[@class='thin-text nav-link']"
information_icon = "xpath,//span[@class='octicon octicon-info']"
least_priced_product = "xpath,//p[contains(text(),'%s')]/following-sibling::button[@class='btn btn-primary']"
moisturizers_button = "xpath,//button[contains(text(),'Buy moisturizers')]"
payment_button = "xpath,//span[normalize-space()='Pay with Card']"
price_of_all = "xpath,//p[contains(text(),'Price')]"
qxf2_link = "xpath,//a[contains(text(),'Qxf2')]"
sunscreens_button = "xpath,//button[contains(text(),'Buy sunscreens')]"
temperature_text = "xpath,//span[@id='temperature']"
buy_button = "xpath,//button[contains(text(),'Buy %s')]"









