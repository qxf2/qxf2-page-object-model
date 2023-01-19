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

#Locators for Main Page

PAGE_TITLE = "xpath,//h1[contains(text(),'Qxf2 Newsletter Generator')]"
HAMBURGER = "xpath,//*[local-name()='svg' and @data-icon='bars']/*[local-name()='path']"
ADD_ARTICLE = "xpath,//div[@class='dropdown-content']/descendant::a[text()='%s']"

#locators for Add Article Page

URL = "xpath,//input[@id='url']"
TITLE = "xpath,//input[@id='title']"
DESCRIPTION = "xpath,//textarea[@id='description']"
TIME = "xpath,//input[@id='time']"
SELECT_CATEGORY = "xpath,//*[@id='category_id']/descendant::option[text()='%s']"
ADD_ARTICLE_BUTTON = "xpath,//input[@id='submit']"
ADDED_RECORD = "xpath,//span[contains(text(),'Record added successfully')]"

#locators for Create Newsletter Page

CATEGORY_URL = "xpath,//span[@role='combobox']"
ADD_MORE_ARTICLE = "xpath,//input[@id='add_more']"
CLEAR_FIELDS = "xpath,//input[@id='cancel']"
ADDED_ARTICLE = "xpath,//td[normalize-space()='%s']"
SELECT_URL = "xpath,//li[contains(text(),'%s')]"
SUBJECT = "xpath,//input[@id='subject']"
OPENER = "xpath,//textarea[@id='opener']"
PREVIEW_TEXT = "xpath,//textarea[@id='preview_text']"
PREVIEW_NEWSLETTER = "xpath,//input[@id='preview_newsletter']"
PREVIEW_CONTENT = "xpath,//div//td[contains(text(),'%s')]"
CREATE_CAMPAIGN = "xpath,//button[@id='campaign']"