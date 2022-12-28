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

# In[2]:


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

# In[3]:


# Read CSV file

bw = pd.read_csv('201902-fordgobike-tripdata.csv')


# In[4]:


# high-level overview of data shape and composition
print(bw.shape)
print(bw.dtypes)
print(bw.head(10))


# In[5]:


bw.describe()


# In[6]:


# how many trips have a minimum duration ( 1 minute and 1 second )

bw[(bw['duration_sec']== 61)].shape[0]


# In[7]:


# how many trips have a minimum duration of the average trip ( 12 minute )
bw[(bw['duration_sec']== 726)].shape[0]


# In[8]:


bw[(bw['duration_sec']>= 80000)].shape[0]


# In[9]:


bw.nlargest(10, ['duration_sec'])


# In[10]:


bw.isna().sum()


# In[11]:


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

# In[12]:


bw.insert(1, 'duration_minutes', bw.duration_sec/60)
bw.insert(1, 'duration_hours', bw.duration_sec/3600)
bw.insert(1, 'duration_days', bw.duration_hours/24)


# In[13]:


# Average Duration 
bw.describe()


# Adding day names

# In[14]:


#changing data type to datetime
bw[['start_time', 'end_time']] = bw[['start_time', 'end_time']].apply(pd.to_datetime)


# In[15]:


# Day name column
bw.insert(4, 'start_day', bw['start_time'].dt.day_name())
bw.insert(6, 'end_day', bw['end_time'].dt.day_name())


# Extract other relevent date information from datetime variable

# In[16]:


bw['start_date_dt']=pd.to_datetime(bw['start_time'])

bw['date'] = bw['start_date_dt'].dt.date
bw['year'] = bw['start_date_dt'].dt.year
bw['day']=bw['start_date_dt'].dt.day
bw['month'] = bw['start_date_dt'].dt.month
bw['dayname']=bw['start_date_dt'].dt.strftime("%A")
bw['monthname'] = bw['start_date_dt'].dt.strftime("%B")
bw['time'] = bw['start_date_dt'].dt.time


# In[ ]:





# In[17]:


bw.info()


# In[18]:


bw.describe


# In[19]:


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

# In[37]:


plt.figure(figsize=[14.70, 8.27])
log_binsize = 0.025
bin_edges = 10 ** np.arange(2.0, np.log10(bw['duration_minutes'].max())+log_binsize, log_binsize)
ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
labels = ['{}'.format(val) for val in ticks]

plt.hist(data = bw, x = 'duration_minutes', bins = bin_edges, rwidth = 0.8);
plt.title('Trip Duration in minutes', y=1.05, fontsize=14, fontweight='bold')
plt.xticks([0, 1e3, 2e3, 5e3, 1e4, 2e4], [0, '5', '10', '15', '20k', '25k'])
plt.xlabel('Duration in minutes', fontweight='bold')
plt.xticks(ticks, labels)
plt.ylabel('Number of Bike Trips', fontweight='bold')


# 
# 
# >**Rubric Tip**: Visualizations should depict the data appropriately so that the plots are easily interpretable. You should choose an appropriate plot type, data encodings, and formatting as needed. The formatting may include setting/adding the title, labels, legend, and comments. Also, do not overplot or incorrectly plot ordinal data.

# What days have the most trips 

# In[21]:


bw.dayname.value_counts()


# What dates have the most trips 

# In[22]:


bw.day.value_counts()


# In[24]:


plt.figure(figsize=[14, 6])
Month = ['February']
sb.countplot(data=bw, x = 'duration_minutes', order=Month, color='steelblue')
plt.title('Trips by Month', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Month', fontweight='bold')
plt.ylabel('Number of Bike Trips', fontweight='bold');


# In[25]:


plt.figure(figsize=[14, 6])
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sb.countplot(data=bw, x='dayname', order=day_order, color='steelblue')
plt.title('Trips by days', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Days of the week', fontweight='bold')
plt.ylabel('Number of Bike Trips', fontweight='bold');


# Looking at this visualization we can see that Thursday has the highest number of trips followed by Tuesday and Wednesday. Now lets drill down on the data and visualize what days had the most bike trips started and what days had the most bike trips ended.

# In[26]:


#  What day are the most bike trips started

bw.start_day.value_counts()


# In[27]:


plt.figure(figsize=[14, 6])
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
bw['start_day'].value_counts(ascending=True).index
sb.countplot(data=bw, y='start_day', order=day_order, color='steelblue')
plt.title('Days With The Most Trips Started', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Days of the week', fontweight='bold')
plt.ylabel('Number of Trips Started', fontweight='bold')
plt.xticks(rotation = 45);


# In[28]:


plt.figure(figsize=[14, 6])
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sb.countplot(data=bw, y='end_day', order=day_order, color='steelblue')
plt.title('Days With The Most Trips Ended', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Days of the week', fontweight='bold')
plt.ylabel('Number of Trips Ended', fontweight='bold');


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

# In[29]:


# Does trip duration change with user type?

plt.figure(figsize=[14.70, 8.27])
sb.violinplot(data = bw.query('duration_minutes <=60'),x= 'user_type',y='duration_minutes',color = sb.color_palette()[0])
plt.title('Duration of Bike Trips by User Type')
plt.xlabel('User Type', fontweight='bold')
plt.ylabel('Duration of Bike Trips', fontweight='bold')


# In[30]:


# Minimum duration per date

plt.figure(figsize=[14.70, 8.27])
base_color = sb.color_palette()[0]
sb.pointplot(data = bw, x = 'day', y = 'duration_minutes', color = base_color)
plt.title('Average Duration of Bike Trips Per Date', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Date', fontweight='bold')
plt.ylabel('Average Duration of Bike Trips in Minutes', fontweight='bold');


# In[31]:


# Minimum duration per date

plt.figure(figsize=[14.70, 8.27])
base_color = sb.color_palette()[0]
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sb.pointplot(data = bw, x = 'dayname', y = 'duration_minutes', order = day_order, color = base_color)
plt.title('Average Duration of Bike Trips Per Day', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Day', fontweight='bold')
plt.ylabel('Average Duration of Bike Trips in Minutes', fontweight='bold');


# In[ ]:




### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?

> Your answer here!

### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?

> Your answer here!
# ## Multivariate Exploration
# 
# > Create plots of three or more variables to investigate your data even
# further. Make sure that your investigations are justified, and follow from
# your work in the previous sections.

# In[32]:


#scatterplot - duration and date

plt.figure(figsize=[14.70, 8.27])
sb.violinplot(data = bw.query('duration_minutes <=60'), x='month', y = 'duration_minutes', hue = 'user_type')
plt.legend(loc= 'center left', bbox_to_anchor = (1, 0.5), title = 'User Type')
plt.title('Trip Duration by Month according to User Type', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Month', fontweight='bold')


# In[33]:


#scatterplot - duration and date

plt.figure(figsize=[14.70, 8.27])
sb.stripplot(data = bw, x='month', y = 'duration_minutes', hue = 'user_type', jitter = 0.35, dodge = True)
plt.legend(loc= 'center left', bbox_to_anchor = (1, 0.5), title = 'User Type')
plt.title('Trip Duration per Month according to User Type', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Month', fontweight='bold')


# In[34]:


#scatterplot - duration and date

plt.figure(figsize=[14.70, 8.27])
sb.pointplot(data = bw, x='day', y = 'duration_minutes', hue = 'user_type', jitter = 0.35, dodge = True)
plt.legend(loc= 'center left', bbox_to_anchor = (1, 0.5), title = 'User Type')
plt.title('Trip Duration on each Date according to User Type', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Date', fontweight='bold')


# In[35]:


#scatterplot - duration and date

plt.figure(figsize=[14.70, 8.27])
sb.stripplot(data = bw, x='dayname', y = 'duration_minutes', hue = 'user_type', jitter = 0.35, dodge = True)
plt.legend(loc= 'center left', bbox_to_anchor = (1, 0.5), title = 'User Type')
plt.title('Trip Duration on each Day according to User Type', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Day', fontweight='bold')


# In[36]:


#scatterplot - duration and date

plt.figure(figsize=[14.70, 8.27])
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sb.pointplot(data = bw.query('duration_minutes <=60'), x='dayname', y = 'duration_minutes', 
order = day_order, hue = 'user_type')
plt.legend(loc= 'center left', bbox_to_anchor = (1, 0.5), title = 'User Type')
plt.title('Trip Duration by Day according to User Type', y=1.05, fontsize=14, fontweight='bold')
plt.xlabel('Day', fontweight='bold')


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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




