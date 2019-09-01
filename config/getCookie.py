import time
import TickerConfig


def getDrvicesID(session):
    """
    :return:
    """
    print("cookie获取中")
    from selenium import webdriver
    cookies = []
    driver = webdriver.Chrome(TickerConfig.CHROME_PATH)
    driver.get("https://www.12306.cn/index/index.html")
    time.sleep(10)
    for c in driver.get_cookies():
        cookie = dict()
        if c.get("name") == "RAIL_DEVICEID" or c.get("name") == "RAIL_EXPIRATION":
            cookie[c.get("name")] = c.get("value")
            cookies.append(cookie)
    if cookies:
        session.httpClint.set_cookies(cookies)
    print("cookie获取完成")
