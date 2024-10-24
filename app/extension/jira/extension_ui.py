import random
import string

from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS

project_key = 'AASSS'
wait_timeout = 20
small_wait_timeout = 70
number_of_attempts = 10
env_url = 'https://www.google.com/'


def create_exploratory_test(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#tests")
    webdriver.refresh()

    test_title = "Test " + ''.join(random.choice(string.ascii_lowercase) for i in range(8))
    for k in range(number_of_attempts):
        try:
            webdriver.refresh()
            page.wait_until_visible((By.ID, "tio_menu-item_exploratory-tests"), wait_timeout).click()
            page.wait_until_visible((By.XPATH, "//div[contains(@class,'exploratoryTestsList')]"
                                               "//div[contains(@class,'test')]"), wait_timeout)
            page.wait_until_visible((By.XPATH, "//span[contains(@class,'createButton')]"), wait_timeout)
            break
        except TimeoutException:
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#tests")
            webdriver.refresh()
            print('TimeoutException handled')

    @print_timing("selenium_create_exploratory_test:start_creation")
    def measure():
        page.wait_until_visible((By.XPATH, "//span[contains(@class,'createButton')]"), wait_timeout).click()

    measure()

    @print_timing("selenium_create_exploratory_test:select_product")
    def measure():
        page.wait_until_visible((By.XPATH, "//label[text()='Product']/../div"), wait_timeout).click()
        page.action_chains() \
            .move_to_element(
            page.get_element((By.XPATH,
                              "//label[text()='Product']/..//div[contains(@class, 'item') and contains(text(),'Jira')]")
                             )).click(page.get_element((By.XPATH,
                                                        "//label[text()='Product']/..//div[contains(@class, 'item') and contains(text(),"
                                                        "'Jira')]"))).perform()

    measure()

    @print_timing("selenium_create_exploratory_test:select_section")
    def measure():
        page.wait_until_visible((By.XPATH, "//label[text()='Section']/../div"),
                                wait_timeout).click()
        page.wait_until_visible(
            (By.XPATH, "//label[text()='Section']/..//div[contains(@class, 'item')]"),
            wait_timeout)
        page.get_elements(
            (By.XPATH, "//label[text()='Section']/..//div[contains(@class, 'item')]"))[
            1].click()

    measure()

    @print_timing("selenium_create_exploratory_test:select_test_type")
    def measure():
        page.wait_until_invisible((By.XPATH, "//div[contains(@class, 'loader')]"), small_wait_timeout)
        page.wait_until_visible((By.XPATH, "//span[contains(@class, 'coverage')]/.."), wait_timeout).click()

    measure()

    @print_timing("selenium_create_exploratory_test:select_test_features")
    def measure():
        page.wait_until_invisible((By.XPATH, "//div[contains(@class, 'loader')]"), small_wait_timeout)
        page.wait_until_visible((By.XPATH, "//input[@name='test_title']"), wait_timeout).send_keys(
            test_title)
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'featureCheckbox')]"),
                                wait_timeout)
        page.get_elements((By.XPATH, "//div[contains(@class,'featureCheckbox')]"))[1].click()

    measure()

    @print_timing("selenium_create_exploratory_test:create_new_environment")
    def measure():
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'environmentField')]//span[@type='button']"),
                                wait_timeout).click()
        page.wait_until_visible((By.XPATH, "//input[@name='title']"), wait_timeout).send_keys(
            test_title)
        page.wait_until_visible((By.XPATH, "//input[@name='url']"), wait_timeout).send_keys(
            env_url)
        page.wait_until_clickable((By.XPATH, "//span[text()='Create']"), wait_timeout).click()
        page.wait_until_invisible((By.XPATH, "//div[text()='Create Test Environment']"
                                             "/following-sibling::div//span[text()='Cancel']"), wait_timeout)

    measure()

    @print_timing("selenium_create_exploratory_test:select_environment")
    def measure():
        page.wait_until_invisible((By.XPATH, "//div[contains(@class, 'loader')]"), small_wait_timeout)
        page.wait_until_visible((By.XPATH, "//label[text()='Environment']/../div"),
                                wait_timeout).click()
        page.wait_until_visible(
            (By.XPATH, "//label[text()='Environment']/..//div[contains(@class,'item')]"),
            wait_timeout)
        page.get_elements(
            (By.XPATH, "//label[text()='Environment']/..//div[contains(@class,'item')]"))[
            1].click()

    measure()

    @print_timing("selenium_create_exploratory_test:cancel_test_creation")
    def measure():
        page.wait_until_visible((By.XPATH, "//span[text()='Cancel']"), wait_timeout).click()
        page.wait_until_visible((By.XPATH, "//span[text()='Leave']"), wait_timeout).click()

    measure()

    @print_timing("selenium_create_exploratory_test:check_presence_start_creation")
    def measure():
        page.wait_until_visible((By.XPATH, "//span[contains(@class,'createButton')]"), wait_timeout)

    measure()


def view_exploratory_test(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#tests")
    webdriver.refresh()

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.ID, "tio_menu-item_exploratory-tests"), wait_timeout).click()
            page.wait_until_visible(
                (By.XPATH, "//div[contains(@class,'title') and contains(text(),'Exploratory Tests')]"), wait_timeout)
            page.wait_until_visible((By.XPATH, "//div[contains(@class,'test')]//span[contains(@class,'title')]"),
                                    wait_timeout)
            break
        except TimeoutException:
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#tests")
            webdriver.refresh()
            print('TimeoutException handled')

    @print_timing("selenium_view_exploratory_test:open_test")
    def measure():
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'test')]//span[contains(@class,'title')]"),
                                wait_timeout)
        page.get_elements((By.XPATH, "//div[contains(@class,'test')]//span[contains(@class,'title')]"))[1].click()

    measure()

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.XPATH, "//div[text()='Test details']"), wait_timeout)
            break
        except TimeoutException:
            webdriver.refresh()
            page.wait_until_visible(
                (By.XPATH, "//div[contains(@class,'title') and contains(text(),'Exploratory Tests')]"), 10).click()
            page.wait_until_visible((By.XPATH, "//div[contains(@class,'test')]//span[contains(@class,'title')]"),
                                    wait_timeout)
            page.get_elements((By.XPATH, "///div[contains(@class,'test')]//span[contains(@class,'title')]"))[1].click()
            print('TimeoutException handled')

    @print_timing("selenium_view_exploratory_test:check_sections_present")
    def measure():
        for j in range(number_of_attempts):
            try:
                page.wait_until_visible((By.XPATH, "//div[text()='Test details']"), wait_timeout)
                page.wait_until_visible((By.XPATH, "//div[text()='Testers']"), wait_timeout)
                page.wait_until_visible((By.XPATH, "//div[text()='Where to test']"), wait_timeout)
                break
            except TimeoutException:
                print('TimeoutException handled')

    measure()


def view_user_stories(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#stories")
    webdriver.refresh()

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.ID, "tio_menu-item_user-stories"), wait_timeout).click()
            page.wait_until_visible(
                (By.XPATH, "//div[contains(@class,'grow') and contains(text(),'User Stories')]"),
                wait_timeout)
            break
        except TimeoutException:
            webdriver.refresh()
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#stories")
            print('TimeoutException handled')

    for k in range(number_of_attempts):
        try:
            page.wait_until_invisible((By.XPATH, "//div[contains(@class,'loader')]"), wait_timeout * 2)
            page.wait_until_visible((By.XPATH, "//div[contains(@class, 'story')]//div[contains(@class, 'grow')]"))
            break
        except TimeoutException:
            print('TimeoutException handled')

    @print_timing("selenium_view_user_stories:open_story_executions")
    def measure():
        for i in range(number_of_attempts):
            try:
                page.get_elements((By.XPATH, "//div[contains(@class, 'story')]//div[contains(@class, 'grow')]"))[
                    1].click()
                page.wait_until_visible(
                    (By.XPATH, "//div[contains(@class, 'executionsPanel')]//div[contains(@class, 'title')]"),
                    wait_timeout)
                break
            except TimeoutException:
                page.wait_until_invisible((By.XPATH, "//div[contains(@class,'loader')]"), wait_timeout * 2)
                page.wait_until_visible((By.XPATH, "//div[contains(@class, 'story')]//div[contains(@class, 'grow')]"))
                print('TimeoutException handled')

    measure()


def app_accept_testio_bug(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#bugs")

    for k in range(number_of_attempts):
        try:
            page.wait_until_invisible((By.XPATH, "//*[text()='No bugs found']"), wait_timeout)
            page.wait_until_visible((By.ID, "tio_menu-item_received-bugs"), wait_timeout).click()
            page.wait_until_visible(
                (By.XPATH, "//div[contains(@class,'title') and contains(text(),'Received Bugs')]"),
                wait_timeout)
            break
        except TimeoutException:
            webdriver.refresh()
            print('TimeoutException handled')

    @print_timing("selenium_app_accept_testio_bug")
    def measure():
        for i in range(number_of_attempts):
            try:
                page.wait_until_visible(
                    (By.XPATH, "//div[contains(@class,'issueDetails')]//span[contains(@class, 'accept')]"),
                    wait_timeout).click()
                break
            except TimeoutException:
                webdriver.refresh()
                print('TimeoutException handled')

    measure()


def app_change_severity_testio_bug(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.XPATH, "//div[contains(@class, 'scrollableContent')]//h1"),
                                    wait_timeout)
            page.wait_until_visible(
                (By.XPATH, "//span[contains(@class, 'secondary') and text()='More']"),
                number_of_attempts)
            break
        except TimeoutException:
            webdriver.refresh()
            print('TimeoutException handled')

    @print_timing("selenium_app_change_severity_testio_bug")
    def measure():
        for j in range(number_of_attempts):
            try:
                number_of_issues = len(page.get_elements(
                    (By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]")))
                for i in range(2, number_of_issues):
                    try:
                        page.wait_until_visible(
                            (By.XPATH, "//span[contains(@class, 'secondary') and text()='More']"),
                            number_of_attempts).click()
                        page.wait_until_visible(
                            (By.XPATH, "//span[contains(@class, 'secondary') and text()='Change Severity']"),
                            number_of_attempts).click()
                        page.wait_until_visible((By.XPATH, "//input[@name='new_severity']/.."), wait_timeout).click()
                        page.wait_until_visible(
                            (By.XPATH, "//input[@name='new_severity']/..//div[contains(@class,'item')]"),
                            wait_timeout)
                        page.get_elements((By.XPATH, "//input[@name='new_severity']/..//div[contains(@class,'item')]"))[
                            1].click()

                        page.wait_until_visible((By.XPATH, "//textarea[@name='comment']"), wait_timeout).send_keys(
                            "New severity")
                        page.wait_until_visible((By.XPATH, "//span[@type='button' and text()='Change']"),
                                                wait_timeout).click()
                        break
                    except TimeoutException:
                        page.get_elements((By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]"))[
                            i].click()
                        print('TimeoutException handled')
                break
            except TimeoutException:
                webdriver.refresh()
                page.wait_until_visible((By.XPATH, "//div[contains(@class, 'scrollableContent')]//h1"),
                                        wait_timeout)
                page.wait_until_visible(
                    (By.XPATH, "//span[contains(@class, 'secondary') and text()='More']"),
                    number_of_attempts).click()
                print('TimeoutException handled')

    measure()


def app_send_request_testio_bug(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
                                    wait_timeout)
            break
        except TimeoutException:
            webdriver.refresh()
            print('TimeoutException handled')
        except ElementClickInterceptedException:
            webdriver.refresh()
            print('ElementClickInterceptedException handled')

    for j in range(number_of_attempts):
        try:
            number_of_issues = len(page.get_elements(
                (By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]")))
            for i in range(2, number_of_issues):
                page.wait_until_visible(
                    (By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
                    wait_timeout)
                if "disabled" in page.get_element(
                        (By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']")) \
                        .get_attribute('class'):
                    page.get_elements((By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]"))[
                        i].click()

                else:
                    break
        except TimeoutException:
            webdriver.refresh()
            page.wait_until_visible((By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
                                    wait_timeout)
            print('TimeoutException handled')
        except ElementClickInterceptedException:
            webdriver.refresh()
            page.wait_until_visible((By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
                                    wait_timeout)
            print('ElementClickInterceptedException handled')

    @print_timing("selenium_app_send_request_testio_bug")
    def measure():
        page.wait_until_visible(
            (By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
            wait_timeout).click()
        page.wait_until_visible((By.XPATH, "//textarea[@name='comment']"), wait_timeout) \
            .send_keys("User request")
        page.wait_until_visible((By.XPATH, "//span[@type='button' and text()='Send']"),
                                wait_timeout).click()

    measure()


def view_testio_specific_bug(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#bugs")

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.ID, "tio_menu-item_received-bugs"), wait_timeout).click()
            page.wait_until_visible((By.XPATH, "//div[text()='Received Bugs']"), wait_timeout)
            break
        except TimeoutException:
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#bugs")
            webdriver.refresh()
            print('TimeoutException handled')

    try:
        page.wait_until_visible(
            (By.XPATH, "//div[contains(@class,'issuesList')]//div[contains(@class,'issue')]"),
            wait_timeout)
    except TimeoutException:
        webdriver.refresh()
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#bugs")
        print('TimeoutException handled')

    @print_timing("selenium_view_testio_specific_bug")
    def measure():
        page.wait_until_visible(
            (By.XPATH, "//div[contains(@class,'issuesList')]//div[contains(@class,'issue')]"),
            wait_timeout)

    measure()
