# ABSTRACT: Based on the beer taste we can infer if people are going to be compatible or matching as friends/partner. The user can approach the website and put some features inside and he will be shown a list of users he will be compatible with. This will be done with clustering based on data from BA and RB. (NEEDS TO BECOME CATCHY BY REPHRASING) we want to pull the beer community together or if you’re visiting a country you can find the perfect guide to go for a beer
 
 
# QUESTION:
1.     Can we cluster users based on geographical data (easy to see on the dataset), commercial/local beers (based on brewery distribution and number of beers they produce  check that there’s matching so that nations we do the search have unique breweries) and the style of beer you would like to try
Based on the cluster we can match the best as possible 
a.     Based on the reviews we can infer the uniqness of a brewery
b.     Based on # of beers it produces we can infer the uniqness of brewery
c.     Do users from same or near location are similar in beer styles preferences? Look at similarities matrix of sebas
2.     Fun facts:
a.     Do you know that people tend to write more (length of description) to describe beers with low scoring?
b.     Do you know that people tend to use weird words (low TFIF) to describe beers with more alcholic content?
c.     Do you know what would be the best year for you to live in?
d.     Do you know what country as your same preferences?
 
# METHODS:

### Temporal Analysis and Herding Effect in Beer Ratings:
In order to analyze the popularity of a certain beer and o
The article by G. Lederrey and R. West (https://doi.org/10.1145/3178876.3186160) on the provided beer dataset reveals a strong influence of preceding ratings on subsequent rating evaluations. This phenomenon, known as the "herding effect," is manifested across both rating platforms, BeerAdvocate and RateBeer. Even when the same beer received similar user counts for ratings, the overall grade assigned to the beer exhibited significant variance between the webs. This discrepancy could be attributed to the initial review presented on the respective website.
The herding effect, as observed in this context, denotes a behavioral tendency among survey participants to align their opinions with those expressed by others. This conformity among users affects the analysis and reliability of the data. This collective conformity among users introduces a significant impact on the analysis and compromises the overall reliability of the data. In response to this challenge, our objective was to counteract this trend by introducing a detrending function.
Firstly, normalizing the reviews so that the average between each pair of previous ratings was compared to the ith rating. In this way we were able to find the offset that this beer was initially encountering by this first rating and by calculating the ratio in which it was affecting the rest of the ratings we could proceed with the weighted aggregation mechanism to balance the overall evaluation and account for this herding effect.
EXTEND A BIT AND REPHRASE(SOBRETODO ESTA ULTIMA PARTE CREO, explain z-score might be important)

### Geographical analysis:
As we wanted to come up with fun facts and relations between nationalities and beer priorites, we merged the data of the users with the beers and brewery information. 

This data shows a huge number of breweries, users and beers from the US.

 
Proposed deadlines:
 
03.11.23 – Analysis and understanding of data
 
06.11.23 – Preprocessing of text files to tsv format
 
09.11.23 – Detranding of herding effect to merge scores
 
17.11.23 - Pause project work
 
01.12.23 - Homework 2 deadline
  
03.12.23 – Fun facts analysis
 
08.12.23 – Extract features for clustering
 
15.12.23 – Clustering algorithm implementation, draft of data story and of webpage 
 
18.12.23 - Provide data story and finalize webpage
 
22.12.23 - Milestone 3 deadline
 
 
Organization of the team in terms of responsibility
 
Andrea: general pipeline, herding effect detrending, time and geographical analysis
Sebas:
Cristina:
Sandra: general pipeline, herding effect detrending, time and geographical analysis
Antonello: Text analysis
 
We equally contribute to data story creation, webpage implementation, clustering and initial preprocessing of the data. 
