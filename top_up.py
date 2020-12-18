import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_PATH = "/home/kove/code/python/drivers/chromedriver"

LOGIN = "https://www.t-mobile.nl/login"
VERBRUIK = "https://www.t-mobile.nl/my/company/verbruik-en-kosten"
OVERVIEW = "https://www.t-mobile.nl/my/company/mbaanvullers"
AANVULLERS = "https://www.t-mobile.nl/my/company/mbaanvullertoevoegen"
MIFI = "http://mifi.local"

MB_MAX = 800  ## TODO Fine tune MB_MAX
REFRESHRATE = 10  ## TODO Increase refresh rate


## TODO Send desktop notifications when bot succeeds and when it fails
## TODO Fine tune all the try except blocks


def notFound(element):
    return element + " not found"


def loginTmobile():
    b2 = webdriver.Chrome(CHROME_PATH)
    b2.get(LOGIN)

    no_cookies = "label[for=Row1_Column1_Cell1_CookieSettings_SelectedCookieTypeAnalytics]"
    auto_login = "Section1_Row2_Column1_Cell1_AutoLogin_AutoLoginButton"

    try:
        b2.find_element_by_css_selector(no_cookies).click()
    except:
        print(notFound(no_cookies))

    try:
        b2.find_element_by_id().click()
        time.sleep(5)
    except:
        print(notFound(auto_login))
        b2.quit()

    return b2


def mbsAanvullen():
    b2 = loginTmobile()
    b2.get(OVERVIEW)

    mb_overview = "Section1_Row1_Column1_Cell1_SubscriberCallStatusOverview_ChanageButton"
    mb_remove_li = "jQuery('.list-group-inset[data-interaction-id=bundle_for_unlimited] li:not(:last-of-type)').remove()"

    try:
        b2.find_element_by_id(mb_overview).click()
    except:
        print(notFound(mb_overview))
        b2.quit()

    bundle_modal = "buyBundleModal_A0DAY02"
    select_bundle = bundle_modal + " .button-green.button-small.button-block"
    buy_bundle = select_bundle + ".mb-2.mb-tablet-0.order-tablet-last.buyBundleButton"

    try:
        WebDriverWait(b2, 30).until(EC.presence_of_element_located((By.ID, bundle_modal)))
    except:
        print(notFound(bundle_modal))
        b2.quit()

    for i in range(0, 10):
        try:
            b2.execute_script(mb_remove_li)
            b2.execute_script("jQuery('#" + bundle_modal + "').css('height', '0')")
            b2.find_element_by_css_selector(select_bundle).click()
            b2.execute_script("jQuery('#" + bundle_modal + "').css('height', 'auto')")
            time.sleep(3)
            # b2.find_element_by_css_selector(buy_bundle).click()
            print("Bevestigen geclicked")
            time.sleep(420)

            return True
        except:
            print("Something went wrong on the aanvullers page")
            time.sleep(5)
            b2.get(OVERVIEW)
            time.sleep(5)


def loginMifi(b1):
    b1.get(MIFI)
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
    b1.quit()


def init():
    b1 = webdriver.Chrome(CHROME_PATH)
    b1 = loginMifi(b1)
    clearHistory(b1)

    volume = readVolume(b1)
    while True:
        while volume <= MB_MAX:
            print("Current Volume: " + str(volume))
            time.sleep(REFRESHRATE)
            volume = readVolume(b1)

        # if mbsAanvullen():
        #     clearHistory(b1)


init()
