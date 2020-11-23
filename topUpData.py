import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MB_MINIMUM = 200

browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
browser.get('https://www.t-mobile.nl/login')

try:
	browser.find_element_by_css_selector('label[for=Row1_Column1_Cell1_CookieSettings_SelectedCookieTypeAnalytics]').click()
except:
	print("Cookie notice button not found")

try:
	browser.find_element_by_id('Section1_Row2_Column1_Cell1_AutoLogin_AutoLoginButton').click()
except:
	print("Auto Login button not found")

try:
	bundleStatus = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.CLASS_NAME, 'bundle-status-unit-value'))
	)
except:
	print("Page not loading")
finally:
	bundleStatusHtml = browser.find_element_by_css_selector('.bundle-status-unit-value').get_attribute('innerHTML')
	bundleStatusValue = int(re.sub('[\D*]', '', bundleStatusHtml))

if bundleStatusValue < MB_MINIMUM:
	browser.get('https://www.t-mobile.nl/my/company/mbaanvullers')

	try:
		browser.find_element_by_id('Row1_Column1_Cell1_SubscriberCallStatusOverview_ChanageButton').click()
	except:
		print("Something went wrong opening the aanvuller page")

else:
	print("There is enough data...")
	browser.quit()

try:
	bundleTopUp = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.ID, 'ZoneBundleOverview6_details'))
	)
except:
	print("Page not loading")
finally:
	# browser.find_element_by_css_selector('#ZoneBundleOverview6_details input[value=Bevestigen]').click
	print('click #ZoneBundleOverview6_details input[value=Bevestigen]')
	browser.quit()