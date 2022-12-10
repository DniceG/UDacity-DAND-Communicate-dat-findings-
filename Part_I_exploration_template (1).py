#!/usr/bin/env python
# coding: utf-8

# # Part I - (Dataset Exploration Title)
# ## by (your name here)
# 
# ## Introduction
# > Introduce the dataset
# 
# >**Rubric Tip**: Your code should not generate any errors, and should use functions, loops where possible to reduce repetitive code. Prefer to use functions to reuse code statements.
# 
# > **Rubric Tip**: Document your approach and findings in markdown cells. Use comments and docstrings in code cells to document the code functionality.
# 
# >**Rubric Tip**: Markup cells should have headers and text that organize your thoughts, findings, and what you plan on investigating next.  
# 
# 
# 
# ## Preliminary Wrangling
# 

# In[4]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import zipfile
import requests
import io


get_ipython().run_line_magic('matplotlib', 'inline')


# > Load in your dataset and describe its properties through the questions below. Try and motivate your exploration goals through this section.
# 

# # 2. Gathering Data

# Gobike bike-sharing

# # A. Getting Jan 2020 Baywheels-Data zip file

# In[6]:


# Read CSV file

bw = pd.read_csv('201902-fordgobike-tripdata.csv')


# In[7]:


# high-level overview of data shape and composition
print(bw.shape)
print(bw.dtypes)
print(bw.head(10))


# In[8]:


bw.describe()


# In[9]:


# how many trips have a minimum duration ( 1 minute and 1 second )

bw[(bw['duration_sec']== 61)].shape[0]


# In[10]:


# how many trips have a minimum duration of the average trip ( 12 minute )
bw[(bw['duration_sec']== 726)].shape[0]


# In[11]:


bw[(bw['duration_sec']>= 80000)].shape[0]


# In[12]:


bw.nlargest(10, ['duration_sec'])


# In[13]:


bw.isna().sum()


# In[14]:


bw.user_type.value_counts()


# # Data Analysis

# ### What is the structure of your dataset?
# 
# > Your answer here!
# 
# ### What is/are the main feature(s) of interest in your dataset?
# 
# > Your answer here!
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# 
# > Your answer here!

# ## Univariate Exploration
# 
# > In this section, investigate distributions of individual variables. If
# you see unusual points or outliers, take a deeper look to clean things up
# and prepare yourself to look at relationships between variables.
# 
# 
# > **Rubric Tip**: The project (Parts I alone) should have at least 15 visualizations distributed over univariate, bivariate, and multivariate plots to explore many relationships in the data set.  Use reasoning to justify the flow of the exploration.
# 
# 
# 
# >**Rubric Tip**: Use the "Question-Visualization-Observations" framework  throughout the exploration. This framework involves **asking a question from the data, creating a visualization to find answers, and then recording observations after each visualisation.** 
# 

# Adding new duration segments to anayze the data easier 

# In[15]:


bw.insert(1, 'duration_minutes', bw.duration_sec/60)
bw.insert(1, 'duration_hours', bw.duration_sec/3600)
bw.insert(1, 'duration_days', bw.duration_hours/24)


# In[16]:


# Average Duration 
bw.describe()


# Adding day names

# In[17]:


#changing data type to datetime
bw[['start_time', 'end_time']] = bw[['start_time', 'end_time']].apply(pd.to_datetime)


# In[18]:


# Day name column
bw.insert(4, 'start_day', bw['start_time'].dt.day_name())
bw.insert(6, 'end_day', bw['end_time'].dt.day_name())


# Extract other relevent date information from datetime variable

# In[19]:


bw['start_date_dt']=pd.to_datetime(bw['start_time'])

bw['date'] = bw['start_date_dt'].dt.date
bw['year'] = bw['start_date_dt'].dt.year
bw['day']=bw['start_date_dt'].dt.day
bw['month'] = bw['start_date_dt'].dt.month
bw['dayname']=bw['start_date_dt'].dt.strftime("%A")
bw['monthname'] = bw['start_date_dt'].dt.strftime("%B")
bw['time'] = bw['start_date_dt'].dt.time


# In[ ]:





# In[20]:


bw.info()


# In[21]:


bw.describe


# In[22]:


# Duration of bike rides in minutess 
plt.figure(figsize=[14.70, 8.27])
bin_edges = np.arange(0, 45, 1)
ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
labels = ['{}'.format(val) for val in ticks]

plt.hist(data = bw, x = 'duration_minutes', bins = bin_edges, rwidth = 0.8);
plt.title('Trip Duration in minutes', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Duration in minutes', fontweight='bold')
plt.xticks(ticks, labels)
plt.ylabel('Number of Bike Trips', fontweight='bold')


# Looking at the graph it apears that most of the rides tend to be concentrated between 3-15 minutes

# 
# 
# >**Rubric Tip**: Visualizations should depict the data appropriately so that the plots are easily interpretable. You should choose an appropriate plot type, data encodings, and formatting as needed. The formatting may include setting/adding the title, labels, legend, and comments. Also, do not overplot or incorrectly plot ordinal data.

# What days have the most trips 

# In[23]:


bw.dayname.value_counts()


# What dates have the most trips 

# In[24]:


bw.day.value_counts()


# In[26]:


plt.figure(figsize=[14, 6])

sb.countplot(data=bw, x='dayname', order=labels, color='steelblue')
plt.title('Trips by days', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Days of the week', fontweight='bold')
plt.ylabel('Number of Bike Trips', fontweight='bold');


# ### Discuss the distribution(s) of your variable(s) of interest. Were there any unusual points? Did you need to perform any transformations?
# 
# > Your answer here!
# 
# ### Of the features you investigated, were there any unusual distributions? Did you perform any operations on the data to tidy, adjust, or change the form of the data? If so, why did you do this?
# 
# > Your answer here!

# ## Bivariate Exploration
# 
# > In this section, investigate relationships between pairs of variables in your
# data. Make sure the variables that you cover here have been introduced in some
# fashion in the previous section (univariate exploration).

# In[ ]:





# ### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?
# 
# > Your answer here!
# 
# ### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?
# 
# > Your answer here!

# ## Multivariate Exploration
# 
# > Create plots of three or more variables to investigate your data even
# further. Make sure that your investigations are justified, and follow from
# your work in the previous sections.

# In[ ]:





# ### Talk about some of the relationships you observed in this part of the investigation. Were there features that strengthened each other in terms of looking at your feature(s) of interest?
# 
# > Your answer here!
# 
# ### Were there any interesting or surprising interactions between features?
# 
# > Your answer here!

# ## Conclusions
# >You can write a summary of the main findings and reflect on the steps taken during the data exploration.
# 

# 
# > Remove all Tips mentioned above, before you convert this notebook to PDF/HTML
# 
# 
# > At the end of your report, make sure that you export the notebook as an
# html file from the `File > Download as... > HTML or PDF` menu. Make sure you keep
# track of where the exported file goes, so you can put it in the same folder
# as this notebook for project submission. Also, make sure you remove all of
# the quote-formatted guide notes like this one before you finish your report!
# 
# 

# In[ ]:





# In[ ]:




