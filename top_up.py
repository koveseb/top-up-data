import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_PATH = "/home/kove/code/python/drivers/chromedriver"

TMO_LOGIN = "https://www.t-mobile.nl/login"
MB_AANVULLERS = "https://www.t-mobile.nl/my/company/mbaanvullers"
MB_AANVULLERS_TOEVOEGEN = "https://www.t-mobile.nl/my/company/mbaanvullertoevoegen"
MIFI_LOGIN = "http://mifi.local"

MB_MIN = 200
REFRESH_RATE = 10


## TODO Send desktop notifications when bot succeeds and when it fails
## TODO Fine tune all the try except blocks


def notFound(element):
    return element + " not found"


def loginTmobile():
    b2 = webdriver.Chrome(CHROME_PATH)
    b2.get(TMO_LOGIN)
    b2.maximize_window()

    no_cookies = "label[for=Row1_Column1_Cell1_CookieSettings_SelectedCookieTypeAnalytics]"
    auto_login = "Section1_Row2_Column1_Cell1_AutoLogin_AutoLoginButton"

    try:
        b2.find_element_by_css_selector(no_cookies).click()
    except:
        print(notFound(no_cookies))

    try:
        b2.find_element_by_id(auto_login).click()
        time.sleep(5)
    except:
        print(notFound(auto_login))
        b2.quit()

    return b2


def bekijkVerbruik():
    b2 = loginTmobile()

    bundle_status = ".bundle-status-unit-value"
    u = "[\D+]"

    try:
        bundle_value = b2.find_element_by_css_selector(bundle_status).get_attribute("innerHTML")
    except:
        print(notFound(bundle_status))
        b2.quit()
    else:
        verbruik = int(float(re.sub(u, "", bundle_value)))
        print("T-Mobile dashboard verbruik: " + str(verbruik))
        return verbruik, b2


def mbsAanvullen(b2):
    b2.get(MB_AANVULLERS)
    time.sleep(5)

    try:
        b2.execute_script("goToManage('+3197023474585','')")
        time.sleep(5)
    except:
        print(notFound("goToManage"))
        b2.quit()

    bundle_modal = "buyBundleModal_A0DAY02"
    mb_remove_li = "jQuery('.list-group-inset[data-interaction-id=bundle_for_unlimited] li:not(:last-of-type)').remove()"
    select_bundle = 'button[data-modal-toggle="#' + bundle_modal + '"]'
    buy_bundle = 'button[data-interaction-id="aanvullers__1 GB-aanvuller NL (zone NL)"]'

    for i in range(0, 10):
        try:
            WebDriverWait(b2, 30).until(EC.presence_of_element_located((By.ID, bundle_modal)))
        except:
            print(notFound(bundle_modal))
            b2.quit()
            time.sleep(5)
            b2.get(MB_AANVULLERS_TOEVOEGEN)
            time.sleep(5)

        try:
            b2.execute_script(mb_remove_li)
            b2.execute_script("jQuery('#" + bundle_modal + "').css('height', '0')")
            b2.find_element_by_css_selector(select_bundle).click()
            b2.execute_script("jQuery('#" + bundle_modal + "').css('height', 'auto')")
            time.sleep(3)
            b2.find_element_by_css_selector(buy_bundle).click()
            print("Bevestigen succeeded")
            b2.quit()
            return True
        except:
            print("Something went wrong on the aanvullers page")
            time.sleep(5)
            b2.refresh()
            time.sleep(5)

    print("Refreshing browser page did not work")
    b2.quit()


def loginMifi(b1):
    b1.get(MIFI_LOGIN)
    login = "logout_span"
    username_field = "username"
    password_field = "password"
    confirm = "pop_login"
    username = "admin"
    password = "9z$Y1kLL6E8k"
    statistic = "statistic"

    try:
        b1.find_element_by_id(login).click()
    except:
        print(notFound(login))
        b1.quit()

    try:
        b1.find_element_by_id(username_field).send_keys(username)
    except:
        print(notFound(username_field))
        b1.quit()

    try:
        b1.find_element_by_id(password_field).send_keys(password)
    except:
        print(notFound(password_field))
        b1.quit()

    try:
        b1.find_element_by_id(confirm).click()
        time.sleep(3)
    except:
        print(notFound(confirm))
        b1.quit()

    try:
        b1.find_element_by_id(statistic).click()
        time.sleep(3)
    except:
        print(notFound(statistic))
        b1.quit()

    return b1


def clearHistory(b1):
    clear_history = "button_clear_history"
    confirm = "pop_confirm"

    try:
        b1.find_element_by_id(clear_history).click()
    except:
        print(notFound(clear_history))
        b1.quit()

    try:
        b1.find_element_by_id(confirm).click()
    except:
        print(notFound(confirm))
        b1.quit()


def readVolume(b1):
    current_volume = "mobile_current_volume"
    u = "\s\D+"

    for i in range(0, 10):
        try:
            volume = b1.find_element_by_id(current_volume).get_attribute("innerHTML")
            unit = re.sub("\s", "", re.findall(u, volume)[0])

            if unit == "KB" or unit == "B":
                time.sleep(60)

            return int(float(re.sub(u, "", volume)))
        except:
            print(notFound(current_volume))
            loginMifi(b1)
            time.sleep(3)
        else:
            break


def init():
    b1 = webdriver.Chrome(CHROME_PATH)
    b1 = loginMifi(b1)
    clearHistory(b1)

    while True:
        verbruik, b2 = bekijkVerbruik()
        mb_max = verbruik - MB_MIN
        print("MB max = " + str(mb_max))

        volume = readVolume(b1)
        while volume <= mb_max:
            print("Current Volume: " + str(volume))
            time.sleep(REFRESH_RATE)
            volume = readVolume(b1)
        else:
            if mbsAanvullen(b2):
                clearHistory(b1)
                print("mbsAanvullen complete")


init()
