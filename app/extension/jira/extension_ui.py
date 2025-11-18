import random
import string

from selenium.common import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS
from selenium_ui.jira.pages.pages import Issue

project_key = 'AASSS'
wait_timeout = 20
small_wait_timeout = 70
number_of_attempts = 10
env_url = 'https://www.google.com/'

client = JiraRestClient(JIRA_SETTINGS.server_url, JIRA_SETTINGS.admin_login, JIRA_SETTINGS.admin_password)
rte_status = client.check_rte_status()
create_project_option_id = 'com.epam.ework.jira.ework-integration-qa:ework-project-button_create'
issue_without_ework_project_key = 'AANES-504'
issue_with_ework_project_key = 'AANES-503'
ework_project_with_task = 'AUTO_STREAM'
wait_timeout = 5
small_wait_timeout = 50
number_of_attempts = 10

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
                              "//label[text()='Product']/..//div[contains(@class, 'item') and contains(text(),'Product')]")
                             )).click(page.get_element((By.XPATH,
                                                        "//label[text()='Product']/..//div[contains(@class, 'item') and contains(text(),"
                                                        "'Product')]"))).perform()

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
            0].click()

    measure()

    page.wait_until_invisible((By.XPATH, "//div[contains(@class, 'loader')]"), small_wait_timeout)

    @print_timing("selenium_create_exploratory_test:select_test_type")
    def measure():
        page.wait_until_visible((By.XPATH, "//span[contains(@class, 'coverage')]/.."), wait_timeout).click()

    measure()

    page.wait_until_invisible((By.XPATH, "//div[contains(@class, 'loader')]"), small_wait_timeout)

    @print_timing("selenium_create_exploratory_test:select_test_features")
    def measure():
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

    measure()

    for m in range(number_of_attempts):
        try:
            page.wait_until_clickable((By.XPATH, "//div[text()='Create Test Environment']"
                                                 "/following-sibling::div//span[text()='Cancel']"),
                                      wait_timeout).click()
            break
        except ElementClickInterceptedException:
            page.wait_until_invisible((By.XPATH, "//div[contains(@class, 'loader')]"), small_wait_timeout)
            print('ElementClickInterceptedException handled')

    page.wait_until_invisible((By.XPATH, "//div[contains(@class, 'loader')]"), small_wait_timeout)
    page.wait_until_visible((By.XPATH, "//label[text()='Environment']/../div"), wait_timeout)

    @print_timing("selenium_create_exploratory_test:select_environment")
    def measure():
        page.wait_until_visible((By.XPATH, "//label[text()='Environment']/../div"),
                                wait_timeout).click()
        page.wait_until_visible((By.XPATH, "//label[text()='Environment']/..//div[contains(@class,'item')]"),
                                wait_timeout)
        page.get_elements((By.XPATH, "//label[text()='Environment']/..//div[contains(@class,'item')]"))[
            0].click()

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
            page.get_elements((By.XPATH, "//div[contains(@class,'test')]//span[contains(@class,'title')]"))[0].click()
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
            page.wait_until_clickable(
                (By.XPATH,  "//div[contains(@class,'issueDetails')]//span[contains(@class, 'accept')]"),
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


# def app_change_severity_testio_bug(webdriver):
#     page = BasePage(webdriver)
#     page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
#     page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
#
#     for k in range(number_of_attempts):
#         try:
#             page.wait_until_visible((By.XPATH, "//div[contains(@class, 'scrollableContent')]//h1"),
#                                     wait_timeout)
#             page.wait_until_visible(
#                 (By.XPATH, "//span[contains(@class, 'secondary') and text()='More']"),
#                 number_of_attempts)
#             break
#         except TimeoutException:
#             webdriver.refresh()
#             print('TimeoutException handled')
#
#     @print_timing("selenium_app_change_severity_testio_bug")
#     def measure():
#         for j in range(number_of_attempts):
#             try:
#                 number_of_issues = len(page.get_elements(
#                     (By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]")))
#                 for i in range(2, number_of_issues):
#                     try:
#                         page.wait_until_visible(
#                             (By.XPATH, "//span[contains(@class, 'secondary') and text()='More']"),
#                             number_of_attempts).click()
#                         page.wait_until_visible(
#                             (By.XPATH, "//span[contains(@class, 'secondary') and text()='Change Severity']"),
#                             number_of_attempts).click()
#                         page.wait_until_visible((By.XPATH, "//input[@name='new_severity']/.."), wait_timeout).click()
#                         page.wait_until_visible(
#                             (By.XPATH, "//input[@name='new_severity']/..//div[contains(@class,'item')]"),
#                             wait_timeout)
#                         page.get_elements((By.XPATH, "//input[@name='new_severity']/..//div[contains(@class,'item')]"))[
#                             0].click()
#
#                         page.wait_until_visible((By.XPATH, "//textarea[@name='comment']"), wait_timeout).send_keys(
#                             "New severity")
#                         page.wait_until_visible((By.XPATH, "//span[@type='button' and text()='Change']"),
#                                                 wait_timeout).click()
#                         break
#                     except TimeoutException:
#                         page.get_elements((By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]"))[
#                             i].click()
#                         print('TimeoutException handled')
#                 break
#             except TimeoutException:
#                 webdriver.refresh()
#                 page.wait_until_visible((By.XPATH, "//div[contains(@class, 'scrollableContent')]//h1"),
#                                         wait_timeout)
#                 page.wait_until_visible(
#                     (By.XPATH, "//span[contains(@class, 'secondary') and text()='More']"),
#                     number_of_attempts).click()
#                 print('TimeoutException handled')
#
#     measure()


# def app_send_request_testio_bug(webdriver):
#     page = BasePage(webdriver)
#     page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
#     page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues")
#     for k in range(number_of_attempts):
#         try:
#             page.wait_until_visible((By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
#                                     wait_timeout)
#             break
#         except TimeoutException:
#             webdriver.refresh()
#             print('TimeoutException handled')
#         except ElementClickInterceptedException:
#             webdriver.refresh()
#             print('ElementClickInterceptedException handled')
#
#     for j in range(number_of_attempts):
#         try:
#             number_of_issues = len(page.get_elements(
#                 (By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]")))
#             for i in range(2, number_of_issues):
#                 page.wait_until_visible(
#                     (By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
#                     wait_timeout)
#                 if "disabled" in page.get_element(
#                         (By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']")) \
#                         .get_attribute('class'):
#                     page.get_elements((By.XPATH, "//div[contains(@class,'issue') and contains(@class,'false')]"))[
#                         i].click()
#
#                 else:
#                     break
#         except TimeoutException:
#             webdriver.refresh()
#             page.wait_until_visible((By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
#                                     wait_timeout)
#             print('TimeoutException handled')
#         except ElementClickInterceptedException:
#             webdriver.refresh()
#             page.wait_until_visible((By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
#                                     wait_timeout)
#             print('ElementClickInterceptedException handled')
#
#     @print_timing("selenium_app_send_request_testio_bug")
#     def measure():
#         page.wait_until_visible(
#             (By.XPATH, "//span[contains(@class, 'secondary') and text()='Send Request']"),
#             wait_timeout).click()
#         page.wait_until_visible((By.XPATH, "//textarea[@name='comment']"), wait_timeout) \
#             .send_keys("User request")
#         page.wait_until_visible((By.XPATH, "//span[@type='button' and text()='Send']"),
#                                 wait_timeout).click()
#
#     measure()


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

    @print_timing("selenium_view_testio_specific_bug")
    def measure():
        try:
            page.wait_until_visible(
                (By.XPATH, "//div[contains(@class,'issuesList')]//div[contains(@class,'issue')]"),
                wait_timeout)
        except TimeoutException:
            webdriver.refresh()
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/issues")
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/{project_key}/test-io-issues#bugs")
            print('TimeoutException handled')

    measure()

def check_edit_project(webdriver):
    page = BasePage(webdriver)

    @print_timing("selenium_edit_project:view_open_project_option")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_with_ework_project_key}")
        page.wait_until_visible((By.ID, "summary-val"))
        page.wait_until_visible((By.ID, "opsbar-operations_more")).click()
        page.wait_until_present(
            (By.ID, "com.epam.ework.jira.ework-integration-qa:ework-project-button_preview")).click()

    measure()

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.XPATH, "//span[text()='Edit project']")).click()
            page.wait_until_visible((By.XPATH, "//input[@name='name']"))
            break
        except (TimeoutException, StaleElementReferenceException):
            webdriver.refresh()
            print('TimeoutException handled')

    @print_timing("selenium_edit_project:open_edit_requirements_tab")
    def measure():
        page.wait_until_visible((By.XPATH, "//div[text()='Instructions']")).click()

    measure()

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.XPATH, "//trix-editor[@input='react_trix-editor_requirements']"))
            break
        except TimeoutException:
            page.wait_until_visible((By.XPATH, "//div[text()='Instructions']")).click()
            print('TimeoutException handled')

    @print_timing("selenium_edit_project:save_changed_requirements_tab")
    def measure():
        page.wait_until_visible((By.XPATH, "//trix-editor[@input='react_trix-editor_requirements']")).send_keys(
            "update")
        page.wait_until_visible((By.XPATH, "//span[text()='Save changes']")).click()
        page.wait_until_visible((By.XPATH, "//span[text()='Close Page']"))

    measure()


def check_create_project_option(webdriver):
    page = BasePage(webdriver)

    @print_timing("selenium_create_project:check_availability_project_creation")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_without_ework_project_key}")
        page.wait_until_visible((By.ID, "summary-val"))
        page.wait_until_visible((By.ID, "opsbar-operations_more")).click()
        page.wait_until_present((By.ID, create_project_option_id))

    measure()


def check_project_creation(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_without_ework_project_key}")

    issue_modal = Issue(webdriver)
    issue_modal.open_create_issue_modal()
    issue_modal.fill_summary_create()
    issue_modal.fill_description_create(rte_status)
    issue_modal.set_resolution()  # Set resolution if there is such field
    issue_modal.assign_to_me()
    issue_modal.submit_issue()

    page = BasePage(webdriver)

    @print_timing("selenium_create_project:select_project_creation_option")
    def measure():
        page.wait_until_present((By.XPATH, "//a[@class='issue-created-key issue-link']")).click()
        page.wait_until_present((By.ID, "opsbar-operations_more")).click()
        page.wait_until_visible((By.ID, create_project_option_id)).click()

    measure()

    next_step = "//span[text()='Continue']"

    @print_timing("selenium_create_project:select_create_ework_project")
    def measure():
        page.wait_until_visible((By.XPATH, "//div[text()='Create a Single Task']/../..")).click()
        page.wait_until_visible((By.XPATH, next_step)).click()

    measure()

    ework_project_name = "EWork test" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    page.wait_until_present((By.XPATH, "//input[@name='name']"))

    @print_timing("selenium_create_project:fill_project_name")
    def measure():
        page.wait_until_present((By.XPATH, "//input[@name='name']")).send_keys(ework_project_name)
        page.wait_until_visible((By.XPATH, "//span[text()='Confirm and Continue']")).click()

    measure()

    page.wait_until_present((By.XPATH, "//trix-editor[@input='react_trix-editor_requirements']"))

    @print_timing("selenium_create_project:fill_project_instructions")
    def measure():
        page.wait_until_present((By.XPATH, "//trix-editor[@input='react_trix-editor_requirements']")).send_keys(
            "Test description")
        page.wait_until_visible((By.XPATH, "//input[@placeholder='Select Date']")).click()
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'calendar')]"))
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'sameDay')]")).click()
        page.wait_until_visible((By.XPATH, next_step)).click()

    measure()

    page.wait_until_visible((By.XPATH, "//input[@name='access_url']"))

    @print_timing("selenium_create_project:grant_access")
    def measure():
        page.wait_until_visible((By.XPATH, "//input[@name='access_url']")).send_keys("https://www.google.com/")
        page.wait_until_visible((By.XPATH, next_step)).click()

    measure()

    page.wait_until_visible((By.XPATH, "//input[@name='use_freelancers']"))

    @print_timing("selenium_create_project:configure_team")
    def measure():
        page.wait_until_visible((By.XPATH, "//input[@name='use_freelancers']")).click()
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'multiSelect')]")).click()
        page.wait_until_visible((By.XPATH, "//input[@name='skill_ids']/following-sibling::div/input")).send_keys(
            "AWK")
        page.wait_until_visible((By.XPATH, "//div[@title='AWK']")).click()
        page.wait_until_visible((By.XPATH, next_step)).click()

    measure()

    page.wait_until_visible((By.XPATH, "//div[@type='redactor']/input"))

    @print_timing("selenium_create_project:payment")
    def measure():
        page.wait_until_visible((By.XPATH, "//div[@type='redactor']/input")).send_keys("40")
        page.wait_until_visible((By.XPATH, next_step)).click()

    measure()

    page.wait_until_visible((By.XPATH, "//span[text()='Publish Project']"))

    @print_timing("selenium_create_project:publish_project")
    def measure():
        page.wait_until_visible((By.XPATH, "//span[text()='Publish Project']")).click()

    measure()

    @print_timing("selenium_create_project:check_auto_comment")
    def measure():
        actual_text = page.wait_until_visible((By.XPATH, "//div[contains(@class, 'singleTaskPreview')]/p")).text
        expected_text = "We are already looking for engineers matching your requirements. You can check the project directly in EWORK."
        assert actual_text == expected_text, f"Error: Expected '{expected_text}', but got '{actual_text}'"

    measure()


def check_task_creation(webdriver):
    page = BasePage(webdriver)
    page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_without_ework_project_key}")

    issue_modal = Issue(webdriver)
    issue_modal.open_create_issue_modal()
    issue_modal.fill_summary_create()
    issue_modal.fill_description_create(rte_status)
    issue_modal.set_resolution()  # Set resolution if there is such field
    issue_modal.assign_to_me()
    issue_modal.submit_issue()

    page = BasePage(webdriver)

    @print_timing("selenium_create_task:select_project_creation_option")
    def measure():
        page.wait_until_present((By.XPATH, "//a[@class='issue-created-key issue-link']")).click()
        page.wait_until_present((By.ID, "opsbar-operations_more")).click()
        page.wait_until_visible((By.ID, create_project_option_id)).click()

    measure()

    next_step = "//span[text()='Continue']"

    @print_timing("selenium_create_task:select_create_ework_task")
    def measure():
        page.wait_until_visible(
            (By.XPATH, "//div[text()='Create a Task for an existing Stream Project']/../..")).click()
        page.wait_until_visible((By.XPATH, next_step)).click()

    measure()

    ework_task_name = "EWork task" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.XPATH, "//div[contains(@type,'redactor')]"))
            break
        except TimeoutException:
            print('TimeoutException handled')

    @print_timing("selenium_create_task:select_ework_stream_project")
    def measure():
        page.wait_until_visible((By.XPATH, "//div[contains(@type,'redactor')]")).click()
        for n in range(number_of_attempts):
            try:
                page.wait_until_visible((By.XPATH, "//div[@type='dropdown']/div")).click()
                break
            except StaleElementReferenceException:
                print('StaleElementReferenceException handled')

    measure()

    for k in range(number_of_attempts):
        try:
            page.wait_until_visible((By.XPATH, "//input[@name='title']"), small_wait_timeout)
            break
        except TimeoutException:
            page.wait_until_visible((By.XPATH, "//div[contains(@type,'redactor')]")).click()
            page.wait_until_visible((By.XPATH, "//div[@type='dropdown']/div")).click()
            print('TimeoutException handled')

    @print_timing("selenium_create_task:fill_task_data")
    def measure():
        page.wait_until_present((By.XPATH, "//input[@name='title']")).send_keys(ework_task_name)
        page.wait_until_present((By.XPATH, "//trix-editor[@input='react_trix-editor_requirements']")).send_keys(
            "Test description")
        page.wait_until_visible((By.XPATH, "//input[@placeholder='Select Date']")).click()
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'calendar')]"))
        page.wait_until_visible((By.XPATH, "//div[contains(@class,'sameDay')]")).click()
        page.wait_until_visible((By.XPATH, "//span[text()='Create Task']")).click()
        page.wait_until_visible((By.XPATH, "//h2[text()='Stream Task was published successfully']"))

    measure()
