"""
Qxf2 Services: Utility script to generate XPaths for the given URL
* Take the input URL from the user
* Parse the HTML content using beautifilsoup
* Find all Input and Button tags
* Guess the XPaths
"""

from selenium import webdriver
from bs4 import BeautifulSoup

class Xpath_Util:
    "Class to generate the xpaths"  
    def guess_xpath(self,tag,attr,element):
        "Guess the xpath based on the tag,attr,element[attr]"
        #Class attribute returned as a unicodeded list, so removing 'u from the list and joining back
        if type(element[attr]) is list:
            element[attr] = [i.encode('utf-8') for i in element[attr]]
            element[attr] = ' '.join(element[attr])
        self.xpath = "//%s[@%s='%s']"%(tag,attr,element[attr])
                
        return  self.xpath

    def guess_xpath_button(self,tag,attr,element):
        "Guess the xpath for button tag"
        self.button_xpath = "//%s[%s='%s']"%(tag,attr,element)
       
        return  self.button_xpath

    def guess_xpath_using_contains(self,tag,attr,element):
        "Guess the xpath using contains function"
        self.button_contains_xpath = "//%s[contains(%s,'%s')]"%(tag,attr,element)
        
        return self.button_contains_xpath
    
    def get_elements_list(self,locator):
        "Get all the elements for the given xpath"
        self.ifunique = False
        if len(driver.find_elements_by_xpath(locator))==1:
            self.ifunique = True
            
        return self.ifunique

    
#-------START OF SCRIPT--------
if __name__ == "__main__":
    print "Start of %s"%__file__

    #Initialize the xpath object
    xpath_obj = Xpath_Util()

    #Get the URL and parse
    url = input("Enter URL: ")
    
    #Create a chrome session
    driver = webdriver.Chrome()
    driver.get(url)
    
    #Parsing the HTML page with BeautifulSoup
    page = driver.execute_script("return document.body.innerHTML").encode('utf-8') #returns the inner HTML as a string
    soup = BeautifulSoup(page, 'html.parser')
 
    #Finding all input tags 
    inputs =  soup.find_all('input')
    
    #Finding all button tags
    buttons = soup.find_all('button')
    
    if inputs == [] and buttons == []:
        print "No input or button tags available to generate the XPath"
    
    for input in inputs:        
        try:
            if input.has_attr('type'):
                if input['type'] == "hidden":
                    continue                
            if input.has_attr("id"):               
                locator = xpath_obj.guess_xpath("input","id",input)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue                                          
            if input.has_attr("name"):               
                locator = xpath_obj.guess_xpath("input","name",input)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue
            if input.has_attr("placeholder"):                
                locator = xpath_obj.guess_xpath("input","placeholder",input)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue          
            if input.has_attr("value"):                
                locator = xpath_obj.guess_xpath("input","value",input)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue 
            if input.has_attr("type"):                
                locator = xpath_obj.guess_xpath("input","type",input)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue                                    
            if input.has_attr("class"):                
                locator = xpath_obj.guess_xpath("input","class",input)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue
        except Exception,e:
            print "Exception when generating XPath for input tags:%s"%__file__
            print "Python says:%s"%str(e)
            
    for button in buttons:
        try:
            if button.has_attr("id"):
                locator = xpath_obj.guess_xpath("button","id",button)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue           
            if button.getText():
                button_text = button.getText()
                if button.getText() == button_text.strip():
                    locator = xpath_obj.guess_xpath_button("button","text()",button.getText())
                else:
                    locator = xpath_obj.guess_xpath_using_contains("button","text()",button_text.strip())

                if xpath_obj.get_elements_list(locator):   
                    #To fix UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 20: ordinal not in range            
                    print locator.encode('utf-8')
                    continue
            if button.has_attr("name"):            
                locator = xpath_obj.guess_xpath("button","name",button)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue 
            if button.has_attr("type"):           
                locator = xpath_obj.guess_xpath("button","type",button)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue 
            if button.has_attr("title"):                
                locator = xpath_obj.guess_xpath("button","title",button)
                if xpath_obj.get_elements_list(locator):
                    print locator
                    continue 
        except Exception,e:
            print "Exception when generating XPath for button tags:%s"%__file__
            print "Python says:%s"%str(e)
     
    driver.quit() 