import time
import gc
import pickle
import pandas as pd
from selenium import webdriver

# Creation of a new instance of Google Chrome
# browser = webdriver.Chrome(ChromeDriverManager().install())
browser = webdriver.Chrome(r'D:/Projects/Drafts/chromedriver.exe')

url = 'https://www.linkedin.com/feed/hashtag/technology/'
tag = 'innovation'
hashtag = 'technology'

# Load the page on the browser
browser.get(url)

browser.execute_script(
    "(function(){try{for(i in document.getElementsByTagName('a')){let el = document.getElementsByTagName('a')[i]; "
    "if(el.innerHTML.includes('Sign in')){el.click();}}}catch(e){}})()")

time.sleep(2)

browser.execute_script(
    "document.querySelector('#username').value='alejandro.diazsantos.aws@gmail.com';"
    "document.querySelector('#password').value='77171618Valencia.';")

time.sleep(5)

print("Let's go\n")

SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

posts = []
# while True:
for _ in range(5000):

    main = browser.find_element_by_xpath("//div[@role = 'main']")
    elements = main.find_elements_by_xpath("//button[@class = 'feed-shared-inline-show-more-text__see-more-less-toggle see-more t-14 t-black--light t-normal hoverable-link-text']")
    # Click in all buttons
    for el in elements:
        # print("click button")
        browser.execute_script("arguments[0].click();", el)

    time.sleep(3)

    ember_view = main.find_elements_by_xpath("//div[@class = 'feed-shared-update-v2__description-wrapper ember-view']")

    res = []
    for rel in ember_view:
        res.append(rel.text)

    num_of_posts = len(res)
    posts.append(res)

    print(_)
    print("Number of posts", num_of_posts)
    print("Number total of posts", len([y for x in posts for y in x]))
    print("........................................................")

    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        posts_flatten = [y for x in posts for y in x if not '…see more' in y]
        posts_flatten_set = list(set(posts_flatten))
        df = pd.DataFrame(posts_flatten_set, columns=["posts"])
        df.to_csv('./scraping/'+tag+'/webscraping_'+hashtag+'_'+str(_)+'.csv', index=False, encoding='utf-8')

        with open('./scraping/'+tag+'/webscraping_'+hashtag+'_'+str(_)+'.txt', 'wb') as fp:
            pickle.dump(posts_flatten_set, fp)

        gc.collect()
        print(hashtag)
        print("list", len(posts_flatten))
        print("list set", len(posts_flatten_set))
        break

    last_height = new_height

    if _ % 20 == 0:
        posts_flatten = [y for x in posts for y in x if not '…see more' in y]
        posts_flatten_set = list(set(posts_flatten))
        df = pd.DataFrame(posts_flatten_set, columns=["posts"])
        df.to_csv('./scraping/'+tag+'/webscraping_'+hashtag+'_'+str(_)+'.csv', index=False, encoding='utf-8')

        with open('./scraping/'+tag+'/webscraping_'+hashtag+'_'+str(_)+'.txt', 'wb') as fp:
            pickle.dump(posts_flatten_set, fp)

        gc.collect()
        print(hashtag)
        print("list", len(posts_flatten))
        print("list set", len(posts_flatten_set))
