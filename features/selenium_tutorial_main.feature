@bdd
Feature: Test Selenium Tutorial Page

	Scenario: Validate Form
		Given I setup the test object
		And I open url /selenium-tutorial-main
		When I set text: Qxf2 in element with id: name
		And I set text: test@qxf2.com in element with name: email
		And I set text: 0000000000 in element with id: phone
		And I click the element with type: button
		And I click the element with text: Male
		And I click the element with type: submit