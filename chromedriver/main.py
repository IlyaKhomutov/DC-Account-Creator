import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


username = str(input("Text your username: "))
email = str(input("Text your email: "))
password = (''.join(random.choice(string.ascii_letters) for i in range(15)))
birthday_day = str(random.randint(1, 12))
birthday_month = str(random.randint(1, 12))
birthday_year = str(random.randint(1990, 2001))
url = "https://discord.com/register"
options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
actions = ActionChains(driver)


def solvehaptcha():
    api_key = os.getenv('APIKEY_2CAPTCHA', '6d2047f498b2f9d6dd6d823a876411dd')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.hcaptcha(
            sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
            url='https://discord.com/register',
        )

    except Exception as e:
        print(e)
        return False

    else:
        return result


try:
    driver.get(url=url)
    email_input = driver.find_element(By.ID, "uid_5")
    email_input.send_keys(email)
    username_input = driver.find_element(By.ID, "uid_7")
    username_input.send_keys(username)
    password_input = driver.find_element(By.ID, "uid_9")
    password_input.send_keys(password)
    actions.send_keys(Keys.TAB)
    actions.send_keys(birthday_day)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(birthday_month)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(birthday_year)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    res = driver.find_element(By.CLASS_NAME, "contents-3ca1mk")
    time.sleep(2)
    res.click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR,
         '#app-mount > div.appDevToolsWrapper-1QxdQf > div > div.app-3xd6d0 > div > div > div > section > div > div.flexCenter-1Mwsxg.flex-3BkGQD.justifyCenter-rrurWZ.alignCenter-14kD11 > div > iframe'
         )))

    result_response = solvehaptcha()

    if result_response:
        captcha_code = result_response['code']
        print(f"YOUR CAPTCHA CODE:", captcha_code)
        driver.execute_script(
            "document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + captcha_code + "'")
        time.sleep(50)
        # iframe = driver.find_element(By.XPATH,
        #                             '//*[@id="app-mount"]/div[2]/div/div[1]/div/div/div/section/div/div[2]/div/iframe')
        # driver.switch_to.frame(iframe)
        # driver.find_element(By.XPATH, '//*[@id="checkbox"]').click()
        # WebDriverWait(driver, 150).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[8]"))).click()
        # driver.find_element(By.XPATH, "/html/body/div[2]/div[8]").click()


    # IT RETURNS TOKEN IF CAPTCHA PASSED
    # input('Press ENTER to get 0Auth token:')
    # token = driver.execute_script(
    #     'location.reload();var i=document.createElement("iframe");document.body.appendChild(i);return i.contentWindow.localStorage.token').strip(
    #     '"')  # Get the token
    # print(f'{token}')

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
