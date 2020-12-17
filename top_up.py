import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN = "https://www.t-mobile.nl/login"
VERBRUIK = "https://www.t-mobile.nl/my/company/verbruik-en-kosten"
AANVULLERS = "https://www.t-mobile.nl/my/company/mbaanvullertoevoegen"

MB_MINIMUM = 215
REFRESHRATE = 120

def reset():
    i = 0

    browser.quit()

    browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
    browser.get(LOGIN)
    browser.maximize_window()

    try:
        browser.find_element_by_css_selector(
            "label[for=Row1_Column1_Cell1_CookieSettings_SelectedCookieTypeAnalytics]"
        ).click()
    except:
        print("Cookie notice button not found")
        browser.quit()

    try:
        browser.find_element_by_id("Section1_Row2_Column1_Cell1_AutoLogin_AutoLoginButton").click()
    except:
        print("Auto Login button not found")
        browser.quit()
    else:
        bekijkVerbruik()


def mbsAanvullen():
    browser.get(AANVULLERS)

    try:
        bundleTopUp = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, "buyBundleModal_A0DAY02"))
        )
    except:
        print("MB Aanvuller page not loading")

    try:
        browser.execute_script("jQuery('.list-group-inset[data-interaction-id=bundle_for_unlimited] li:not(:last-of-type)').remove()")
        browser.execute_script("jQuery('#buyBundleModal_A0DAY02').css('height', '0')")
        browser.find_element_by_css_selector('#buyBundleModal_A0DAY02 .button-green.button-small.button-block').click()
        browser.execute_script("jQuery('#buyBundleModal_A0DAY02').css('height', 'auto')")
        time.sleep(3)
        browser.find_element_by_css_selector('#buyBundleModal_A0DAY02 .button-green.button-block.mb-2.mb-tablet-0.order-tablet-last.buyBundleButton').click()
        print("Bevestigen geclicked")
        time.sleep(420)

        bekijkVerbruik()
    except:
        mbsAanvullen()

def bekijkVerbruik():
    browser.get(VERBRUIK)

    try:
        browser.find_element_by_id(
            "Row1_Column1_Cell1_SubscriberCallStatusOverview_ChanageButton"
        ).click()
    except:
        print("Bekijk verbruik button not found")
        browser.quit()

    try:
        el = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#ro1co1ce1 .cell .bundle-usage-table tr:first-of-type td:nth-last-of-type(2)",
                )
            )
        )
    except:
        print("Bundle Status page not loading")
        browser.quit()

    bundleStatusElement = browser.find_element_by_css_selector(
            "#ro1co1ce1 .cell .bundle-usage-table tr:first-of-type td:nth-last-of-type(2)"
    ).get_attribute("innerHTML")
    bundleStatusValue = int(re.sub("[\D*]", "", bundleStatusElement))

    while bundleStatusValue >= MB_MINIMUM:
        print(bundleStatusValue)
        browser.find_element_by_id("RefreshUsageButton").click()
        time.sleep(REFRESHRATE)
        bundleStatusElement = browser.find_element_by_css_selector("#ro1co1ce1 .cell .bundle-usage-table tr:first-of-type td:nth-last-of-type(2)").get_attribute("innerHTML")
        bundleStatusValue = int(re.sub("[\D*]", "", bundleStatusElement))
        time.sleep(5)
        # i+=1 

        # if i > 5:
            # reset()

        
    mbsAanvullen()

i = 0
browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
browser.get(LOGIN)
browser.maximize_window()

try:
    browser.find_element_by_css_selector(
        "label[for=Row1_Column1_Cell1_CookieSettings_SelectedCookieTypeAnalytics]"
    ).click()
except:
    print("Cookie notice button not found")
    browser.quit()

try:
    browser.find_element_by_id("Section1_Row2_Column1_Cell1_AutoLogin_AutoLoginButton").click()
except:
    print("Auto Login button not found")
    browser.quit()
else:
    bekijkVerbruik()
