# Scraper-for-Job-Hunting

## Abstract
This application is a web scraper to collect job information and deliver a nationwide insight html report for the kind of job input to the application. The application is user-friendly, after users enter a job type, they’ll be presented with a detailed csv file documenting related information (job position, company, salary, job summary, etc.) acquired from Glassdoor and Indeed. More importantly, an html report will also be presented, containing figures (choropleth maps, histograms, bar charts, word cloud) that are generated based on the advanced analysis of scrapped data, which provides more insights for users. To realize the application, the team first utilized xpath and the libraries Beautiful Soup, Selenium, Time, and Pandas to scrape and process data. After using Pandas and Numpy to clean the data, various visualizations are created with the libraries Matplotlib, Seaborn, Wordcloud, and Plotly, and the final html report is automatically generated with chart_studio. In using those libraries, the team successfully achieves various features and presents productive information. 

## Documentation: 
 
### projectall (main)
This module is used as a main method to call all the other modules. First, it would promopt the user to enter a job title. Then, it would call scrapping's methods to scrape the data from glassdoor and indeed. Next, it would use the dataclean.cleanjobs method to do the data cleaning. After that, it would call all the methods in visualizedata to visualize and analyze the data. Finally, it would use the htmloutput.htmlOutPut to generate a html report.


### scrapping
This module consists of three functions that receives the searching key word and scrapes the raw data from glassdoor and indeed:

glassdoorscraper(search_job):
	Description: This function is used to format the user input of job title and call the find_info function. Also, it will count the executing time and control the number of pages to scrape. 
	Input: the job title string from user input
	Output: The first one is a dataframe contains all the data scraped from Glassdoor, including job title, company name, salary, etc. The second one is an integer: the total number of jobs in this search. 

find_info(page, jobName):
	Description: This function utilizes Beautiful Soup and Selenium to scrape the data from Glassdoor. Firstly, it catches the possible pop-up windows on each page and closes them. Secondly, it uses find function to get the static information on the current page. Thirdly, it uses click function in Selenium to enter the next page. At last, it structures the data into a data frame and returns the value. 
	Input: number of pages as interger; the job title string from user input
	Output: The first one is a dataframe that contains all the data scraped from Glassdoor, including job title, company name, salary, etc. The second one is an integer: the total number of jobs in this search. 

indeedscraper(search_job):
	Description: This function is defined to scrape and process data from the website Indeed, using Beautiful Soup and Pandas. The first step is to scrape required data from the website specified by users' input after inspecting. Using a loop allows us to scrape at most 100 pages from the website and get nearly 2000 records.  
	Input: the job title string from user input
	Output: a Pandas DataFrame. In the output, there are 3 columns in the dataframe, specifying job position, company, and job summary of each job. 

### dataclean
This module contains a function for cleaning the data scraped from glassdoor:

cleanjobs(jobs):
	Description: Cleans the raw data from glassdoor. It mostly focus on two columns: location and salary. For location, it extracts state name and delete state name with more than two letters. For salary, it extracts min salary and max salary without format and calculate average salary. It also replaces None with np.nan in salary and state. And finally, it deletes rows with None jobTitle in the data frame.
	Input: raw data of job information collected from Glassdoor.
	Output: data frame after cleaning. 

### visualizedata
This module contains three functions for to generate the visualizations for the job data:
heatmapdraw(jobs, search_job):
	Description: This function is used to visualize the data of salary and job location in the format of a choropleth map which is a heatmap using geographical boundaries to represent spatial variations of a quantity. First uses Counter from collection package to aggregate data then utilizes ploty API to visualize those results.
	Input: cleaned data of job information collected from Glassdoor.
	This fuction plots 2 Heat Maps. The first one is a heatmap for job number distribution. We aggregate data by state, count the job number within each state, and then plot the heatmap. The second one is a heatmap for average salary distribution. We aggregate data by state, get the average salary within each state and then plot the heatmap.

barchartdata(jobs):
	Description: This function is used to visualize the data of salary and job positions in format of histogram and barchart. First uses Pandas and Numpy to perform analytics, then utilizes Seaborn and Matplotlib to visualize those results.
	Input: cleaned job data from Glassdoor in Pandas dataframe
	Output: three plots generated. The first is a histogram of salary distribution nationwide mean, median as well as quartile values are marked for comparation. The second is a barchart showing the top 5 job positions salary distribution, with mean and median salary of all job positions for reference. The third is a horizontal barchart presenting top 10 job positions along with the number of job posts for each one.


wordclouddata(indeed_jobs):
	Description: This function is used to receive the job description from this search and return a word cloud. Firstly, it downloads the english stop words from nltk and adds some new words to it. Secondly, it uses sklearn to generate the word frequency list. Finally, the wordCloud object is generated by wordcloud library and shows the image by Matplotlib.
	Input: a list of job description
	Output: a wordcloud object shows the top 60 words


### htmloutput
This module contains a fuction to generate a HTML that contains all the data visualzations:
htmloutput:
	Description: This function is used to generate an HTML report for users. First uses chart_studio; chart_studio.plotly to get the url for figures in plotly and use BytesIO to save images in matplotlib as binary file and use base64 to get the images’ html form. And then inserts the images’ url and text descriptions into the html report.
	Input: search_job, jobsCount, image urls, outdir for output location
	Output: An HTML report in the output location which contians all the analytical graphs.


## Instructions

1. This application uses ChromeDriver. Download ChromeDriver from this link:
https://chromedriver.chromium.org/ 
Unzip the ChromeDriver executable and move it to the desired folder location.
*  If there is a space in the directory path, python may have an issue accessing it.
2. Set ChromeDriver Directory: Open the “scrapping” script and locate the “find_info” function. Find the following script and change the path below to the folder directory of ChromeDriver.exe.
driver = webdriver.Chrome(
        executable_path="C:\\Users\\genev\\chromedriver.exe",
        options=options)
3. Set output Directory: Open the “projectall” script. Find the following script and change the path to the folder directory of the location where the user want to get the output report.
outdir = 'C:\\Users\\genev\\OneDrive\\Desktop\\Python\\Project'
4. Check if these libraries are installed in your Python: request, bs4, plotly, wordcloud. If not, install them.
5. Create a ploty account and change the username and api_key in your Python: Open the "htmloutput" script and change the username and api_key as your own.
6. Start the Program and input a job name: Run the “projectall” script and type in a desired job name.
7. A Chrome window will open. Don’t close it or do anything to it.	             
8. Output: Wait around 5 minutes until the program is finished running and an HTML report is generated.

The “data scientist_report” in HTML contains all the graphs.
The “jobs.csv” displays stores all the scraped data.
