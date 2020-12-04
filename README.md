<<<<<<< HEAD


![Colorado Participated  in a U.S. General Election in 1876](https://commons.wikimedia.org/wiki/File:ElectoralCollege1876.svg)

<a href="https://commons.wikimedia.org/wiki/File:ElectoralCollege1876.svg">AndyHogan14</a>, Public domain, via Wikimedia Commons


# MSDS69 Practicum 2, Fall of 2020
### James D. Reed (jreed011@regis.edu)
#### December 9, 2020

=======
# MSDS696 Practicum 2, Fall of 2020
>>>>>>> ba6ae081bc9e2ec6fb19c97b37222e0cf14f17c2

## Project Summary

The project consisted of data collection from several sources and dealing with APIs and a third-party application (TABULA).  I was able to produce tables and visual artifacts using blended data sets.  For example, I merged geographic data (FIPS codes of locations and associated shape files)



## Problem Definition
I will use publicly available data from the Colorado state government and the US Census Bureau to characterize Colorado counties' demographic makeup and voting behavior.  The period covered will nominally be from 2010 to 2020, including the pending general election to be held on November 3, 2020.  The 2020 election data depends, of course, on the availability of election data after the election and before the date this project is due.   

Colorado has sixty-four counties, most of which lean conservative (at least in the recent past), as evidenced by past elections.  This is not unlike rural areas in most states.  I will investigate demographic data from the US Census to understand the basis for this behavior.  

##  Questions Addressed

I have learned  enough in my research to address the following questions:

 1)	How do rural counties affect the outcome of national elections?
 2)	Have voting patterns changed over the past ten years?
 3)	What is the demographic makeup of the active voting population?
 4)	Do economic shifts affect the way people vote?

 Comments on these topics will be presented in the summary section of this report.


## Data Inventory

I have successfully collected the following datasets:.

### Colorado Voter Registration

1.	Colorado Voter Registration for the years 2009 to 2020.  Eachyears data consists of twelve (one for each month).  There are multiple tabs in each workbook breaking the data out by gender, party and status (active or non-active).  I have created several Pandas Data Frames:  
 a. Co-party
 b.	Co-registered-voters-by-gender  
 c.	Co-registered-voters-by-party 
 d.	Co-status  

 ### U.S. Census 2010 Decennial and American Community Surveys

 2) 	US Census (Census.gov).  Generally, I have focused on two sources here:  American Community Survey for 2019 (ACS19) and the decennial census for 2010 (Census2010).  This is a summary of the Data Frames I have created so far:  
 a.	acs19-inc_df – Income distribution by county.
 b.	acs19-mar_df – marital status by county.  
 c.	acs19-pop_df – population distribution by county.  
 d.	acs19-pov_df – poverty by county.  

### Colorado Election Abstracts and Voter Registration

3.	 Colorado Voter Abstracts These are datasets used to summarize the results of an election.  I have transferred the Presidential results from the Abstracts for these general election years:  
 a.	1952  
 b.	1956    
 c.	1960  
 d.	1964  
 e.	1968  
 f.	1972  
 g.	1976  
 h.	1980

### Electoral Map Images and Geographic Shape Files

 4. Images and geographic data required to generate images.
  a. Shape files for the boudaries of Colorado state and its counties.
  b. To illustrate the history of U.S.  election results, including Colorado, I have collected national red/blue  maps from Wikipedia  

[2020 General Election Electoral College Results ](https://commons.wikimedia.org/wiki/File:ElectoralCollege2020_with_results.svg)

<a title="Kingofthedead, Public domain, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:ElectoralCollege2020_with_results.svg"><img width="512" alt="ElectoralCollege2020 with results" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/ElectoralCollege2020_with_results.svg/512px-ElectoralCollege2020_with_results.svg.png"></a>
---
### Tools

1. Anaconda Python 3.7 Jupyter Lab from Anaconda.  I actually relied on two installations installations.  One on my laptop (hadley), of course and the other on a workstation (woolsey) running CentOS 7 located in my basement.  It was convenient to keep most of my work on the basement workstation (woolsey).

2. [Census.gov]( https://www.census.gov/data/developers.html)  This site provided instructions on how to use the API.  Once one know the structure of a request, its pretty straightforword to compose and download the desired data.  See module _censusFunctions.py_ in the notebooks directory here.  The messy part of retrieving so  much data is that the variables are "coded" and on direct inspections hard to decipher.  In most cases I translated each of these coded variable names  into something more easily recognizable.  For example Census.gov variable **P001001** became  **total_population**.  This is a labor-intensive task and  I think the better way to handle these is to use the Census.gov assigned variable names and build a data dictionary so you can just _look-up_ the purpose of a variable.

Following is a small excerpt of a data dictionary I made using a bit of RE and Python:


|  Variable              |  Description                                           
| ------------------ | --------------------------------------------------------------|
|  DP02_0001E   	|   Estimate_HOUSEHOLDS BY TYPE_Total households       |
|  DP02_0001PE     |  Percent Estimate_HOUSEHOLDS BY TYPE_Total hous...   |
|  DP02_0002E	    |  Estimate_HOUSEHOLDS BY TYPE_Total households_F...  |
| DP02_0002PE	   |  Percent Estimate_HOUSEHOLDS BY TYPE_Total hous...   |
| DP02_0003E  	    |  Estimate_HOUSEHOLDS BY TYPE_Total households_F...  |
| DP02_0003PE	   |  Percent Estimate_HOUSEHOLDS BY TYPE_Total hous...   |
| DP02_0004E	    |  Estimate_HOUSEHOLDS BY TYPE_Total households_F...  |
| DP02_0004PE      | Percent Estimate_HOUSEHOLDS BY TYPE_Total hous...    |
| DP02_0005E        |  	Estimate_HOUSEHOLDS BY TYPE_Total households_F... |

3. The Colorado Secretary of State (currently Jena Griswold) [website]( https://www.sos.state.co.us/pubs/elections/main.html) has digital resources valuable in researching this topic.  Specifically, I have taken advantage of:    
  a. 2020 General Election Results, both graphical and tabular by county.  
  b. Since 1902, Colorado has published  Abstracts of Election Results  and in more recent years this has included the votes cast for each candidate summarized by county.  
  c.  Voter Registration Statistics.  These are published on a monthly basis, again, by county and include active and non-active party registrants.  Additionally, these data are summarized by gender and age.  Registration data is broken down by congressional districts as well as counties.

  4. I must acknowledge the skills I achieved usiing courses from both DataCamp and  Udemy.   I picked up  a clearer understanding of Pandas and Regular Expressioons (Udemy) and Seaborn graphics (DataCamp).



---

## Project Objective

The purpose of this project is to explore the voting behavior of Colorado counties in U.S.  General Elections .  Specifically, I will be using results of the Presidential election results.  One of the observations often cited is that rural counties tend to be conservative.  We have all seen the "red/blue" maps that show that most of the Democrat votes come from Northeastern Cities and the West and Northwest of the Continental Forty-Eight.  One of my goals is to determine if this is a phenomenon that is true through the ages.  If so, what influences this tendency.  Is it the demographic characteristics of rural life:  wealth, education, housing?  

Using the data artifacts I list above and Machine Learning, I hope to uncover the reasons for Colorado's voting history and current behavior at the county level.

## Summary of Analysis

High level description of steps performed for the analysis:


### Methods


#### Utilities and Techniques


#### Models


### Results

### Lessons Learned

### Next Steps

### Data and Project Summary


```{python}
val =  function(data) 
for j in range(len(foo)):
    ret = j**2



```
