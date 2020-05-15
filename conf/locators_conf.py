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

#Locators for the footer object(footer_object.py)

footer_menu = "xpath,//ul[contains(@class,'nav-justified')]/descendant::a[text()='%s']"
copyright_text = "xpath,//p[contains(@class,'qxf2_copyright')]"
#----

#Locators for the form object(form_object.py)
name_field = "id,name"
email_field = "name,email"
phone_no_field = "css selector,#phone"
click_me_button = "xpath,//button[text()='Click me!']"
gender_dropdown = "xpath,//button[@data-toggle='dropdown']"
gender_option = "xpath,//a[text()='%s']"
tac_checkbox = "xpath,//input[@type='checkbox']"
#----

#Locators for hamburger menu object(hamburg_menu_object.py)
menu_icon = "xpath,//img[@alt='Menu']"
menu_link = "xpath,//ul[contains(@class,'dropdown-menu')]/descendant::a[text()='%s']"
menu_item = "xpath,//ul[contains(@class,'dropdown-menu')]/descendant::a[@data-toggle='dropdown' and text()='%s']"
#----

#Locators for header object(header_object.py)
qxf2_logo = "xpath,//img[contains(@src,'qxf2_logo.png')]"
qxf2_tagline_part1 = "xpath,//h1[contains(@class,'banner-brown') and text()='SOFTWARE TESTING SERVICES']"
qxf2_tagline_part2 = "xpath,//h1[contains(@class,'banner-grey') and text()='for startups']"
#----

#Locators for table object(table_object.py)
table_xpath = "xpath,//table[@name='Example Table']"
rows_xpath = "xpath,//table[@name='Example Table']//tbody/descendant::tr"
cols_xpath = "xpath,//table[@name='Example Table']//tbody/descendant::td"
cols_relative_xpath = "xpath,//table[@name='Example Table']//tbody/descendant::tr[%d]/descendant::td"
cols_header = "xpath,//table[@name='Example Table']//thead/descendant::th"
#----

#Locators for tutorial redirect page(tutorial_redirect_page.py)
heading = "xpath,//h2[contains(@class,'grey_text') and text()='Selenium for beginners: Practice page 2']"

#Locators for Contact Object(contact_object.py)
contact_name_field = "id,name"

#Locators for mobile application - Bitcoin Info(bitcoin_price_page.py)
bitcoin_real_time_price_button = "xpath,//android.widget.TextView[@resource-id='com.dudam.rohan.bitcoininfo:id/current_price']"
bitcoin_price_page_heading = "xpath,//android.widget.TextView[@text='Real Time Price of Bitcoin']"
bitcoin_price_in_usd = "xpath,//android.widget.TextView[@resource-id='com.dudam.rohan.bitcoininfo:id/doller_value']"
