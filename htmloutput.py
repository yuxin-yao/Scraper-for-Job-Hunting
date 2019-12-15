# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 17:54:51 2019

@author: genev
"""

def htmlOutPut(search_job,jobsCount,figstate,figsal,salbar_im,salpobar_im,pobar_im,text_im,outdir):
    '''
    This function is used to generating a HTML report for users. 

    Parameters
    ----------
    search_job : TYPE
        DESCRIPTION.
    jobsCount : TYPE
        DESCRIPTION.
    figstate : TYPE
        DESCRIPTION.
    figsal : TYPE
        DESCRIPTION.
    salbar_im : TYPE
        DESCRIPTION.
    salpobar_im : TYPE
        DESCRIPTION.
    pobar_im : TYPE
        DESCRIPTION.
    text_im : TYPE
        DESCRIPTION.
    outdir : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    import chart_studio
    import chart_studio.plotly as py
    chart_studio.tools.set_credentials_file(username='YuxinYao', api_key='tEFRY8O2Q7hwAKdUGy01')
    
    plotstate_url = py.plot(figstate, filename='plotstate_url') 
    plotsal_url = py.plot(figsal, filename='plotsal_url') 
    html_string = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head>
        <body>
            <h1>'''+search_job+''' search report</h1>
            <h2>There are total '''+jobsCount+''' of '''+search_job+''' in USA</h2>
            <!-- *** Section 1 Choropleth Maps  *** --->
            <h2>Section 1: Choropleth Map for job number distribution in USA</h2>
            <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
    src="''' + plotstate_url + '''.embed?width=800&height=550"></iframe>
            <p>From Glassdoor.</p>
            
            <h2>Section 2: Choropleth Map for job salary distribution in USA</h2>
            <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
    src="''' + plotsal_url + '''.embed?width=800&height=550"></iframe>
            <p>From glassdoor.</p>
            <!-- *** Section 2 Bar Chart*** --->
            <h2>Section 3: Histogram for job salary distribution in USA</h2>
            '''+salbar_im+'''
            <p>From glassdoor.</p>
            <h2>Section 4: Bar chart for Top 5 Positions Salary Distribution in USA</h2>
            '''+salpobar_im+'''
            <p>From glassdoor.</p>
            <h2>Section 5: Bar chart for job title in USA</h2>
            <img src="pobar_im.png", width = 1000>
            <p>From glassdoor.</p>
            <!-- *** Section 3 Word Cloud*** --->
            <h2>Section 6: Word Cloud for job description in USA</h2>
            <img src="my_test1.png", width = 1000>
            <p>From Indeed.</p>
           
        </body>
    </html>'''
    
    f = open(outdir+'/'+search_job+'_report.html','w')
    f.write(html_string)
    f.close()
