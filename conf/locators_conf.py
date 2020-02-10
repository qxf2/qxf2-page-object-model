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
search_buses_button ="xpath,//button[contains(@class,'D120_search_btn searchBuses')]"

#Locators for the redBus header object(redBus_header_object.py)
header_logo = "xpath,//a[contains(@class,'redbus-logo home-redirect')]"
header_menu = "xpath,//nav[contains(@class,'product-nav fl')]/descendant::a[contains(text(),'%s')]"

#Locators for the redBus footer object(redBus_footer_object.py)
footer_menu_headings ="xpath,//h6[contains(text(),'%s')]"
foorter_logo = "xpath,//div[contains(@class,'logo')]"
footer_copyright_text = "xpath,//div[contains(@class,'copyright')]"

#Locators for redirect of redBus Main Page i.e search results page 
source_location_in_search_results_page = "xpath,//span[contains(@class,'src')]"
destination_location_in_search_results_page ="xpath,//span[contains(@class,'dst')]"
view_seats_button = "xpath,(//div[contains(@class,'button view-seats')])[1]"
seat_selection_message="xpath,//span[contains(@class,'seatSelMsg') or contains(text(),'Click on an Available seat to proceed with your transaction.')]"

