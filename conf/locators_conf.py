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

# Locators for search buses object
source = "xpath,//input[contains(@id,'txtSource')]"
destination = "xpath,//input[contains(@id,'txtDestination')]"
onward_date = "xpath,//input[contains(@id,'txtOnwardCalendar')]"
return_date = "xpath,//input[contains(@id,'txtReturnCalendar')]"
search_buses_button ="xpath,//button[contains(text(),'Search Buses')]"

#Locators for the redBus header object(redBus_header_object.py)
header_logo = "xpath,//a[contains(@class,'redbus-logo home-redirect')]"
#bus_tickets = "xpath,//a[contains(@class,'selectedBus site-links')]"
header_menu = "xpath,//nav[contains(@class,'product-nav fl')]/descendant::a[contains(text(),'%s')]"

#Locators for the redBus footer object(redBus_footer_object.py)
footer_menu_headings ="xpath,//h6[contains(text(),'%s')]"
foorter_logo = "xpath,//div[contains(@class,'logo')]"
footer_copyright_text = "xpath,//div[contains(@class,'copyright')]"

#Locators for redirect of redBus Main Page i.e view buses page 
#govt_buses_option = "xpath,//span[contains(text(),'Book your choice of bus on RTC')]"
source_location_in_view_buses_page = "xpath,//span[contains(@class,'src') and contains(@title,'%s')]"
destination_location_in_view_buses_page ="xpath,//span[contains(@class,'dst') and contains(@title,'%s')]"

