"""
This is a Selenium test in Python3 to test a wiki page.

Prerequisites:
1. Download and place the chromedriver binary version matching your browser version under /opt/WebDriver/bin/
2. Install the required Python modules
"""

import pdb
from urllib import request, error

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

test_url = "https://en.wikipedia.org/wiki/Metis_(mythology)"


# helper method to validate if a given URL is valid or not
def validate_url(url):
    try:
        request.urlopen(url)
        print(url+" is a valid URL")
    except error.URLError as url_error:
        pdb.set_trace()
        print(url_error.reason)


# create a Selenium Webdriver for Chrome
driver = webdriver.Chrome()
driver.get(test_url)
# get the table of contents(toc) element
toc = driver.find_element_by_xpath('//*[@id="toc"]')
# capture the items in toc object into a list
contents_list = toc.find_elements_by_tag_name("li")

# iterate the list, for each item:
# 1. assert the href link is functional
# 2. assert the content name is displayed as heading on the page
for content in contents_list:
    href_label = content.text
    content_label = content.find_element_by_class_name("toctext").text
    # validate that hyperlink is functional
    try:
        driver.find_element_by_xpath("//span[text()='"+content_label+"']")
        content.find_element_by_link_text(href_label).click()
        print("URL is functional for: " + href_label)
    except NoSuchElementException as e:
        print("ERROR: URL is not functional for: " + href_label)

    # validate that content name is displayed as heading
    try:
        content.find_element_by_xpath("//span[text()='"+content_label+"']")
        print("Heading name displayed on page for: " + content_label)
    except NoSuchElementException as e:
        print("ERROR: Heading name not found for: " + content_label)

# verify popup displays expected text
name_to_hover_over = "Nike"
hover_class_name = "mwe-popups-extract"
v_text = "In ancient Greek civilization, Nike was a goddess who personified victory. Her Roman equivalent was Victoria."
personified_concepts_element = driver.find_elements_by_class_name("sidebar-content")[2]
try:
    element_to_hover_over = personified_concepts_element.find_element_by_link_text(name_to_hover_over)
    print("Found element: " + name_to_hover_over)
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mwe-popups-extract")))
    print("Displayed popup text: " + popup.text)
    if popup.text != v_text:
        print("ERROR: Displayed popup text does not match expected")
    # navigate to new page
    element_to_hover_over.click()
    # traverse to "Family tree" section
    driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[5]/div[1]/div[2]/ul/li[7]/a/span[2]").click()
    # verify "Family tree" is displayed
    driver.find_element_by_class_name("toccolours")
    print("Family tree displayed on page")
except NoSuchElementException as e:
    print("ERROR: " + e.msg)


driver.close()
