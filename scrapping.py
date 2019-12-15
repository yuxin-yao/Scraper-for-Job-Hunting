# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 17:31:22 2019

@author: genev
"""

'''
Function: getting information from glassdoor
Input: the number of pages scraped; the searching job title
Output: a dataframe with all the data type; the number of jobs in this search
'''
def find_info(page, jobName):
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import time
    from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    url = ("https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=%s&sc.keyword=%s&locT=&locId=&jobType=" % (jobName, jobName))
    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.

    driver = webdriver.Chrome(
        executable_path="C:\\Users\\genev\\chromedriver.exe",
        options=options)
    driver.set_window_size(1120, 1000)
    driver.get(url)

    position = []
    company = []
    location = []
    salary = []
    rating = []
    for i in range(page):
        try:
            driver.find_element_by_class_name("selected").click()  # catch the pop-up windows
        except ElementClickInterceptedException:
            pass
        try:
            driver.find_element_by_xpath("//*[@id=\"JAModal\"]/div/div[2]/span").click()  # clicking to the X.
        except NoSuchElementException:
            pass

        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Using find function to get the static information in each job record
        for div in soup.find(name="ul", class_="jlGrid hover").children:
            try:
                current_position = div.find_all(class_="jobLink jobInfoItem jobTitle")[1].get_text()
                position.append(current_position)
            except:
                position.append("None")
            try:
                current_company = div.find(class_="jobInfoItem jobEmpolyerName").get_text()
                company.append(current_company)
            except:
                company.append("None")
            try:
                current_location = div.find(class_="subtle loc").get_text()
                location.append(current_location)
            except:
                location.append("None")
            try:
                current_salary = div.find(class_="salaryText").get_text()
                salary.append(current_salary)
            except:
                salary.append("None")
            try:
                current_rating = div.find(class_="compactStars").get_text()
                rating.append(current_rating)
            except:
                rating.append("None")

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Page %d is failed" % i)
        time.sleep(1)
    result = pd.DataFrame({'jobTitle': position,
                           'companyName': company,
                           'location': location,
                           'salary': salary,
                           'companyRating': rating})
    jobsCount = soup.find(class_="jobsCount")
    print("The number of related job posted: %s" % jobsCount.get_text())
    return result, jobsCount.get_text()


'''
Function: Format the user input, regulate the pages searched and calculate the executing time
Input: the searching job title
Output: a dataframe with all the data type; the number of jobs in this search
'''
def glassdoorscraper(search_job):
    import time
    # hdr = {'User-Agent': 'Mozilla/5.0'}
    jobName = search_job.replace(' ', '+')  # change the searching keyword to the format of glassdoor's url
    page = 30
    start = time.time()
    result_glassdoor, jobsCount = find_info(page, jobName)
    end = time.time()
    print("Executing time: %d" % (end-start))
    return result_glassdoor, jobsCount


'''
Function: getting information from indeed
Input: the searching job title
Output: a dataframe with all the data type
'''
def indeedscraper(search_job):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    jobname_url_1 = '+'.join(search_job.split(' '))

    result = pd.DataFrame()
    for p in range(1,101):  # last page we can scrape is 100
        p = (p-1) * 10  
        url = ('https://www.indeed.com/jobs?q='+jobname_url_1+'&start=%d' % (p) )  # get full url 
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Using find_all function to return a list of all the job record in this page
        detail = soup.find_all('div', attrs={'class': 'row'})
        for d in detail:
            try:
                position = d.find(name='a', attrs={'data-tn-element':'jobTitle'}).attrs['title']
            except:
                position = 'None'
            try:
                company = d.find(name="span", class_="company").get_text().strip()
            except:
                company = 'none'
            try:
                summary = d.find(name="li").get_text()
            except:
                summary = 'None'
            result = result.append({'job title': position, 'company name': company,
                                'job summary': summary}, ignore_index=True)
    return result
