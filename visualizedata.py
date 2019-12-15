# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 17:33:35 2019

@author: genev
"""

def heatmapdraw(jobs, search_job):
    '''
   This function is used to visualize the data of salary and job location in format of choropleth map
    Input arguments: cleaned data of job information collected from Glassdoor.
    This fuction plots 2 Heat Maps. 
    THe first one is a heatmap for job number distribution. 
    The second one is a heatmap for average salary distribution. 

    Parameters
    ----------
    jobs : TYPE
        DESCRIPTION.
    search_job : TYPE
        DESCRIPTION.

    Returns
    -------
    list
        DESCRIPTION.

    '''
    import pandas as pd
    from collections import Counter
    z = jobs['State']
    a = Counter(z)
    df = pd.DataFrame.from_dict(a, orient='index').reset_index()
    df = df[df['index'].str.len() <= 2]
    import plotly.graph_objects as go

    # Load data frame and tidy it.

    
    
    figstate = go.Figure(data=go.Choropleth(
        locations=df['index'], # Spatial coordinates
        z = df[0].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Blues',
        colorbar_title = "# of jobs",
    ))
    
    figstate.update_layout(
        title_text = '# of '+search_job+' jobs in USA by State',
        geo_scope='usa', # limite map scope to USA
    )
    
    figstate.show()
    
    salstate = jobs[['Average Sal','State']]

    sumavesal = pd.DataFrame()
    sumavesal['Sum'] = salstate.groupby(['State']).sum()['Average Sal']
    sumavesal['Count'] = salstate.groupby(['State']).count()['Average Sal']
    sumavesal['Result'] = sumavesal['Sum']/sumavesal['Count']

    figsal = go.Figure(data=go.Choropleth(
        locations=sumavesal.index, # Spatial coordinates
        z = sumavesal['Result'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Blues',
        colorbar_title = "K dollars",
    ))
    
    figsal.update_layout(
        title_text = 'Average salaries of '+search_job+' jobs in USA by State',
        geo_scope='usa', # limite map scope to USA
    )
    
    figsal.show()
    return [figstate, figsal]

'''
Function:This funtion generates 3 plots. 
The first is a histogram of salary distribution in the nationwide.
The second is a barchart showing the top 5 job positions salary distribution
The third is a horizonal barchart presenting top 10 job
Input: cleaned job data from Glassdoor in pandas dataframe
Output: One histrogram and two bar charts
'''
def barchartdata(jobs):
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    from io import BytesIO
    import base64	
    import numpy as np

    salDf = jobs
    df = salDf[pd.notnull(salDf['Average Sal'])]   # remove NaN
    
    
    # histogram salary distribution
    
    # summarize mean,median, 75% and 25% quantiles
    m = df['Average Sal'].mean()   # mean salary for all positions
    me = df['Average Sal'].median()
    q1 = df['Average Sal'].quantile(0.25)
    q2 = df['Average Sal'].quantile(0.75)
    sns.set_style("dark")
    salDist = sns.distplot(df['Average Sal'])
    salDist.axvline(me, lw=1.5, ls='dashed', color='black')
    salDist.axvline(m, lw=1.5, ls='dashed', color='red')
    salDist.axvline(q1, lw=1.5, ls='dashed', color='green')
    salDist.axvline(q2, lw=1.5, ls='dashed', color='green')
    plt.xlabel('Average Salary')
    plt.title('Salary($k) Distribution with Median (black), Mean (red) and Quantiles (green)')
    
    # save the plot
    buffer = BytesIO()
    plt.savefig(buffer)  
    plot_data = buffer.getvalue()
    
    imb = base64.b64encode(plot_data)  
    ims = imb.decode()
    imd = "data:image/png;base64,"+ims
    salbar_im = """<img src="%s", width = 1000>""" % imd 
   
        
    # plot the average salary for top 5 positions
    df['jobTitle'] = df['jobTitle'].str.replace('Sr.','Senior')
    df['jobTitle'] = df['jobTitle'].str.replace('Sr','Senior')
    jobCnt = df['jobTitle'].value_counts()
    top5Cnt = jobCnt[0:5].to_dict()
    
    # average the salaries by job title
    top5Sal = {}
    for job in list(top5Cnt.keys()):
        row = df[df['jobTitle'].str.match(job)]
        top5Sal[job] = row['Average Sal'].mean()
    
    job = list(top5Sal.keys())
    sal = list(top5Sal.values())
    
    
    plt.figure(figsize=(10, 6))
    plt.bar(job, sal)
    plt.xlabel('Job Title')
    plt.ylabel('Average Salary ($k)')
    plt.axhline(y = me, ls='dashed', color="black")
    plt.axhline(y = m, ls='dashed', color="red")
    
    plt.title('Average Salary for Top 5 Job Positions with Median (black) and Mean (red)')  
    plt.tight_layout()  # show conplete labels in the saved image
    buffer = BytesIO()
    plt.savefig(buffer)  
    plot_data = buffer.getvalue()
    
    # save the plot 
    imb = base64.b64encode(plot_data)  
    ims = imb.decode()
    imd = "data:image/png;base64,"+ims
    salpobar_im = """<img src="%s", width = 1000>""" % imd 
    
    
    # plot the counts of top 10 job titles
        
    data = jobs    
    title_count=data['jobTitle'].value_counts()
    
    top=10
    title_count1=title_count[:top]  
    titles=list(title_count1.index)
    counts=list(title_count1.values)

    fig1, ax1 = plt.subplots(dpi = 1200)
    y_pos = np.arange(len(titles))
        
    ax1.barh(y_pos,counts)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(titles)
    ax1.invert_yaxis()  # labels read top-to-bottom
    title_String='Number ('+str(len(data['jobTitle']))+' Job Posts in Total)'
    ax1.set_xlabel(title_String)
    for i, v in enumerate(counts):
        ax1.text(v, i, str(v),fontsize=9)
    ax1.set_title('Top 10 Job Titles',fontsize=18)

    # save the plot 
    buffer = BytesIO()
    plt.savefig(buffer)  
    plot_data = buffer.getvalue()
    
    imb = base64.b64encode(plot_data)  
    ims = imb.decode()
    imd = "data:image/png;base64,"+ims
    pobar_im = """<img src="%s", width = 1000>""" % imd 
    fig1.savefig('pobar_im.png', bbox_inches="tight")

    

    return [salbar_im,salpobar_im,pobar_im]

'''
Function: calculate the words frequency in job description and generate a wordCloud
Input: a list of job description
Output: the visualization of wordCloud
'''
def wordclouddata(indeed_jobs):
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    from wordcloud import WordCloud
    import nltk
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import TfidfVectorizer
    plt.clf()
    data = indeed_jobs.drop_duplicates().reset_index(drop=True)

    # Change the dataframe to a string list
    jobDescription = []
    for i in range(len(data)):
        jobDescription.append(data['job summary'][i])

    # Use nltk to get the english stop words and add some new words to it
    nltk.download('stopwords')
    stop_words = stopwords.words('english')
    extra_stop_words = ["experience", "position", "work", "please", "click", "must", "may", "required", "preferred",
                        "type", "including", "strong", "ability", "needs", "apply", "skills", "requirements", "company",
                        "knowledge", "job", "responsibilities", "develop", "solution", "support", "build", "new",
                        "development", "years", "solutions", "etc", "using", "management", "environment", "time",
                        "related", "help", "working", "analysis", "tools", "technologies", "design", "scientist",
                        "research", "information", "techniques", "degree", "models", "status", "us", "people",
                        "opportunity", "role", "understanding", "advanced", "use", "well", "insights", "provide",
                        "products", "complex", "based", "across", "plus", "problems", "teams", "employees",
                        "employers", "one", "employer", "employee", "within", "improve", "industry", "reporting",
                        "field", "excellent", "best", "quality", "e", "impact", "g", "key", "building", "methods",
                        "looking", "deep", "developing", "create", "high", "multiple", "make", "benefits", "care",
                        'statistical', 'deliver', 'non', 'focus', 'maintenance', 'sets', 'manage', 'various']
    stop_words += extra_stop_words
    print("Generating Word Cloud...")

    # Build the parameter for calculating word frequency
    tfidf_para = {
        "stop_words": stop_words,
        "analyzer": 'word',   #analyzer in 'word' or 'character'
        "token_pattern": r'\w{1,}',    #match any word with 1 and unlimited length
        "sublinear_tf": False,  #False for smaller data size  #Apply sublinear tf scaling, to reduce the range of tf with 1 + log(tf)
        "dtype": int,   #return data type
        "norm": 'l2',     #apply l2 normalization
        "smooth_idf":False,   #no need to one to document frequencies to avoid zero divisions
        "ngram_range" : (1, 2),   #the min and max size of tokenized terms
        "max_features": 60    #the top 60 weighted features
    }
    tfidf_vect = TfidfVectorizer(**tfidf_para)
    transformed_job_desc = tfidf_vect.fit_transform(jobDescription)
    freqs_dict = dict([(word, transformed_job_desc.getcol(idx).sum()) for word, idx in tfidf_vect.vocabulary_.items()])

    # Use the word frequency to generate a wordCloud object with top 60 words
    wordcloud = WordCloud(
        background_color='white',
        width=1500,
        height=960,
        margin=10,
        mode='RGBA',
        max_words=60).fit_words(freqs_dict)

    # Use matplotlib to show and save the image
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file('my_test1.png')

    buffer = BytesIO()
    plt.savefig(buffer)  
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  
    ims = imb.decode()
    imd = "data:image/png;base64,"+ims
    text_im = """<img src="%s", width = 1000>""" % imd
    return text_im
