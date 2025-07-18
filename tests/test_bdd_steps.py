from pytest_bdd import parsers,scenario, given, when, then

@scenario("selenium_tutorial_main.feature", "Validate Form")
def test_form(test_obj):
	"""Sample BDD test scenario."""
	pass

@given(parsers.cfparse("I open url {url:String}", extra_types={"String": str}))
def open_url(test_obj, url):
	"""
	Given step to open a URL in the browser.
	This step is used to navigate to a specific URL before running tests.
	"""
	print(f"Opening URL: {test_obj.base_url + url}")
	test_obj.open(url)

@when(parsers.cfparse("I set text: {text:String} in element with id: {id:String}", extra_types={"String": str}))
def set_text_id(test_obj, text, id):
	"""
	When step to set text in an element with a specific locator.
	This step is used to interact with elements on the page.
	"""
	locator = f"css selector,#{id}"
	print(f"Setting text '{text}' in element with locator '{locator}'")
	test_obj.set_text(locator, text)

@when(parsers.cfparse("I set text: {text:String} in element with name: {name:String}", extra_types={"String": str}))
def set_text_name(test_obj, text, name):
	"""
	When step to set text in an element with a specific locator.
	This step is used to interact with elements on the page.
	"""
	locator = f"css selector,[name={name}]"
	print(f"Setting text '{text}' in element with locator '{locator}'")
	test_obj.set_text(locator, text)


@when(parsers.cfparse("I click the element with type: {type:String}", extra_types={"String": str}))
def click_element(test_obj, type):
	"""
	When step to click an element with a specific type.
	This step is used to interact with elements on the page.
	"""
	locator = f"css selector,[type={type}]"
	print(f"Clicking element with locator '{locator}'")
	test_obj.click_element(locator)

@when(parsers.cfparse("I click the element with text: {text:String}", extra_types={"String": str}))
def click_element_with_text(test_obj, text):
	"""
	When step to click an element with specific text.
	This step is used to interact with elements on the page.
	"""
	locator = f"xpath,//*[text()='{text}']"
	print(f"Clicking element with locator '{locator}'")
	test_obj.click_element(locator)