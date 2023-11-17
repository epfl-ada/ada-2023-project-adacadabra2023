## TITLE:
Be(er)AGuide

## ABSTRACT:
Move beyond the ordinary tourist experience and immerse yourself in the world of beer exploration when travelling. Our concept serves as a guiding light for those adventurous souls who crave more from their beer-related travels. We are building a community where beer enthusiasts unite to uncover the true essence of each locale's brews. "Be(er)AGuide" is more than a guide; it is an invitation to be part of a community, connecting with individuals who share your passion, discovering unique beers and learning interesting curiosities of our community and beyond. Join us as we transform typical beer tourism into a shared adventure, discovering the heart of each destination through its unique brews. You now have the opportunity to Be(er)AGuide!
 
## Research questions:
In our traveling guide we aim to address the following questions where the three main categories are:
1. Information on local breweries and unique beers for your travel:
    - What are the top-rated beers and breweries among the local ones in each country? Does it change over time?
    - Within a preferred beer style, which is the top-rated in each country?
2. Connecting with people when you travel:
    - Can we cluster users based on beer styles using the mean ratings of a set of beers and could these people be in contact when traveling? 
    - After doing clustering, are there any features in common within a cluster? In particular, we will investigate if users belonging to the same cluster share location, similar alcohol content, or use similar wording.
    - If you are a new user and not part of the community, can we put you in contact with a beer expert user?
3. Fun facts about the community:
    - Does the length of the reviews change over the years?
    - Can we provide information on which beer had the highest rating each year? 
    - Can we extract what are the most out-of-context words that reviewers used when commenting on a beer?

 
## METHODS:

### Herding Effect in Beer Ratings:
The article by G. Lederrey and R. West (https://doi.org/10.1145/3178876.3186160) on the provided beer dataset reveals a strong influence of preceding ratings on subsequent rating evaluations. This phenomenon, known as the "herding effect," is manifested across both rating platforms and it emerges due to the behavioral tendency among survey participants to align their opinions with previous users. This compromises the overall reliability of the data, especially to analyze trends that require the use of the scores from both data sources.  

For example, analyzing the merged results by year and performing an average for the same beer or the style, would highly be influenced by the herding effect. One could consider that this effect would be mitigated by doing a macro-average but, if for a certain year, there are only beers coming from the same source, the herding effect would still be present.

To counteract this trend we introduced a detrending function. The rating score from each of the reviews was normalized to its z-score following the pipeline described in the paper to reduce any influence of the year. Then, the ratings were ordered according to the time they were posted and an expanding average was calculated. The latter was done to obtain each time the average of the previous scores, which is what was shown to the user. A linear regression model was used to predict the difference between the ith z-score and the expanding average at that point. The predicted difference from the model was added (the model predicted a negative value if the z-score was higher than the expanding average at that point) to the actual z-score, thus detrending the herding effect.	

### Time and geographical analysis:
For the time analysis distribution of preferred styles or beer over the years, a macro-average was performed with the ratings from both websites. In the geographical analysis, a distribution of the users per country was analyzed and we concluded the use of the subdivision by state for the USA would yield more balanced sets of data.

### Matching users by styles ratings:
After analysing the ratings of the users, we could compare the preferences of each user review for a subsequent match. The preferences are considered from the mean score of the detrended value that one user gives to a set of beers from the same beer style. Having this information, we could apply a similarity analysis treating each user as a vector where the components are the ratings of the styles. Therefore, as we focus on those users with similar ratings on common styles, the cosine method suits due to the score decrease when one component is zero, indicating if those vectors point to the same direction. However, the Pearsons’ correlation uses a similar principle but centering the data at the mean value of the dataset and performing the linear correlations from this new coordinate axis. Finally, having these similarities between users, we could create a network and form clusters.

### Text analysis:
Starting from the detrend dataset we cleaned the reviews by eliminating stopwords, emoticons, emoji, URL, email addresses and numbers. The text was then normalized through lemmatization to reduce words to their canonical form (lemma) and tokenized to see the different words of the reviews. The length of each review was then computed by counting the tokens. 

The TF-IDF is a method that tries to identify the most distinctively frequent or significant words in a document. It computes the multiplication of the Term Frequency (TF) and the Inverse Document Frequency (IDF). The TF captures the frequency of the word within each document while the IDF captures in how many documents each word appears. We computed the TF-IDF with scikit-learn library which prevents zero divisions in the IDF and computes the two terms as described in the notebook.

The use of the TF-IDF will be as following:
    - Clustering task, TF-IDF used to extrapolate words that best define each reviewers
    - Fun facts section, TF-IDF used to identify unusual words. The analysis will be followed by SVD to reduce dimensionality of the reviews and represent them into vectorial space. By color coding each review by corresponding ABV content we can see if there's any relation between the ABV and the unusual words used by reviewers


## Proposed deadlines:
 
03.11.23 – Analysis and understanding of data
 
06.11.23 – Preprocessing of text files to tsv format
 
09.11.23 – Detranding of herding effect to merge scores
 
17.11.23 – Pause project work
 
01.12.23 – Homework 2 deadline
  
03.12.23 – Fun facts analysis
 
08.12.23 – Text analysis and breweries data extraction

15.12.23 – Clustering algorithm implementation, draft of data story and webpage 
 
18.12.23 – Provide data story and finalize webpage
 
22.12.23 - Milestone 3 deadline
 
## Organization of the team in terms of responsibility
 
Andrea: herding effect detrending, time and geographical analysis

Sebas: users clustering

Cristina: text analysis and breweries analysis 

Sandra: herding effect detrending, time and geographical analysis

Antonello: text analysis and breweries analysis
 
We equally contribute to data story creation, webpage implementation and initial preprocessing of the data. 
