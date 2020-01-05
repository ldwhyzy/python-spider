'''
说说碰到的问题吧，找电影封面的时候有的封面就是找不到,以为是没加载出来，
使用WebDriverWait，还是找不到，看了出错信息发现有的img是显示的data-src这个属性，
不是src属性，src属性没有的错误提示刚好在一堆log里，没看到。。。。
只能说第一绝对要找出错信息。
把使用WebDriverWait注释掉，取data-src也可以了。
然后，你这img标签，有的显示src属性的图片，有的显示data-src属性是要闹哪样。
改完后，还有一个图片没取到，没去分析，把WebDriverWait又用回来，完全没问题了。
没有再去验证那个图片没取到是不是没加载出来。
'''
#import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver.implicitly_wait(20)
wait = WebDriverWait(driver, 10)

def get_one_page(url):
    try:
        driver.get(url)
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'board-img')))
        #time.sleep(30)
        #print(driver.page_source)
        #with open('test.html', 'w+', encoding='utf-8') as f:
        #    f.write(driver.page_source)
    except Exception as e:
        print(e)
        return
    return driver.page_source
    
def parse_page(page):
    if not page:
        return
    movie_info_list = []
    try:
        dds = driver.find_elements_by_css_selector('.board-wrapper>dd')
        for dd in dds:
            movie_info = {}
            src = dd.find_element_by_css_selector('img.board-img').get_attribute('src')
            if not src:
                src = dd.find_element_by_css_selector('.board-img').get_attribute('data-src')
            movie_info['img'] = src
            movie_info['name'] = dd.find_element_by_css_selector('.name').text
            movie_info['star'] = dd.find_element_by_css_selector('.star').text
            movie_info['releasetime'] = dd.find_element_by_css_selector('.releasetime').text
            movie_info['score'] = dd.find_element_by_css_selector('.score').text
            #print(movie_info)
            movie_info_list.append(movie_info)
        url = driver.find_element_by_css_selector('.list-pager>li:last-child a').get_attribute('href')
        if 'http' not in url:
            #url = None
            driver.close()
            return movie_info_list
        page = get_one_page(url)
        movie_info_one = parse_page(page)
        if movie_info_one:
            movie_info_list.extend(movie_info_one)        
    except Exception as e:
        print(e)
        return        
    return movie_info_list

def main():
    url = 'https://maoyan.com/board/4'
    #url = 'http://127.0.0.1:3000'
    #url = 'https://www.baidu.com'
    page = get_one_page(url)
    info = parse_page(page)
    with open('猫眼TOP100榜.txt', 'w+', encoding='utf-8') as f:
        f.write('\n'.join([str(x) for x in info]))
    
if __name__ == '__main__':
    main()   