import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MB_MINIMUM = 200

browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
browser.get('https://www.t-mobile.nl/login')
browser.maximize_window()

try:
	browser.find_element_by_css_selector('label[for=Row1_Column1_Cell1_CookieSettings_SelectedCookieTypeAnalytics]').click()
except:
	print("Cookie notice button not found")
	browser.quit()

try:
	browser.find_element_by_id('Section1_Row2_Column1_Cell1_AutoLogin_AutoLoginButton').click()
except:
	print("Auto Login button not found")
	browser.quit()

browser.get('https://www.t-mobile.nl/my/company/verbruik-en-kosten')

try:
	browser.find_element_by_id('Row1_Column1_Cell1_SubscriberCallStatusOverview_ChanageButton').click()
except:
	print("Bekijk verbruik button not found")
	browser.quit()

try:
	el = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.ID, 'bundle-status-identifier'))
	)
except:
	print("Bundle Status page not loading")
	browser.quit()

bundleStatusHtml = browser.find_element_by_css_selector('.bundle-status-unit-value').get_attribute('innerHTML')
bundleStatusValue = int(re.sub('[\D*]', '', bundleStatusHtml))

while bundleStatusValue >= 200:
	browser.find_element_by_id('RefreshUsageButton').click()
	browser.implicitly_wait(15)

browser.get('https://www.t-mobile.nl/my/company/mbaanvullertoevoegen')

try:
	bundleTopUp = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.ID, 'ZoneBundleOverview6_details'))
	)
except:
	print("MB Aanvuller page not loading")

try:
	# browser.find_element_by_css_selector('#ZoneBundleOverview6_details input[value=Bevestigen]').click
	print('Click Bevestigen')
	browser.implicitly_wait(5)
	browser.get('https://www.t-mobile.nl/my/company/verbruik-en-kosten')
except:
	print("Auto Login button not found")