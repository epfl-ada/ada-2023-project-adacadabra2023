## ABSTRACT:

Move beyond the ordinary tourist experience and immerse yourself in the world of beer exploration when travelling. Our concept serves as a guiding light for those adventurous souls who crave more from their beer-related travels. Whether you are a novice or expert beer enthusiasts __Be(er)AGuide__ will lead you to explore unique facets of beer culture around the world. In our blog, we characterize several countries by exploring the amount of local and industrial breweries they have and the most preferred beer styles by trimester of the year. In addition, we further investigate how the users describe the different beer styles by doing text analysis. Join us as we transform typical beer tourism into a shared adventure, discovering the heart of each destination through its unique brews. You now have the opportunity to Be(er)AGuide!

Find our data story here: https://adacadabra2023gigi.streamlit.app/

## Research questions:
Exploring the impact of culture on an individual's personality is a common research question in sociology. Some authors such as Baharuddin (2014) and Wright (2001) have reflected how this aspect can even be extended to something as personal as our taste in food. They have revealed that exposure and experiences with various flavors significantly shape an individual's culinary preferences, highlighting the intricate connection between culture, personality, and our palate. In our case, we wanted to use the provided beer dataset to determine whether a similar influence could be observed in the beer preferences. In other words, we tried to assess if distinct stylistic preferences in beer could be used to predict a person's country of origin, training, in this way, our classifier. 

## METHODS:

### Herding Effect in Beer Ratings:
The article by G. Lederrey and R. West (https://doi.org/10.1145/3178876.3186160) on the provided beer dataset reveals a strong influence of preceding ratings on subsequent rating evaluations. This phenomenon, known as the "herding effect," is manifested across both rating platforms and it emerges due to the behavioral tendency among survey participants to align their opinions with previous users. This compromises the overall reliability of the data, especially to analyze trends that require the use of the scores from both data sources.

For example, analyzing the merged results by year and performing an average for the same beer or the style, would highly be influenced by the herding effect. One could consider that this effect would be mitigated by doing a macro-average but, if for a certain year, there are only beers coming from the same source, the herding effect would still be present.

To counteract this trend, we introduced a detrending function. The rating score from each of the reviews was normalized to its z-score following the pipeline described in the paper to reduce any influence of the year. Then, the ratings were ordered according to the time they were posted and an expanding average was calculated. The latter was done to obtain each time the average of the previous scores, which is what was shown to the user. A linear regression model was used to predict the difference between the ith z-score and the expanding average at that point. The predicted difference from the model was added (the model predicted a negative value if the z-score was higher than the expanding average at that point) to the actual z-score, thus detrending the herding effect.

### Dataframes merging
For the merging of both datasets, we randomly chose to keep the IDs from RateBeer, used the matched datasets to map the IDs for data coming from BeerAdvocate and, lastly, for the unmatched data in BeerAdvocate, random IDs were assigned, excluding the numbers that had already been used by RateBeer to avoid erroneous matchings. This also allowed to track back where the data was coming from.

### Macro-beer styles
To improve the interpretability of the beer styles, given their high number (180), we opted to reduce dimensionality by categorizing them into 20 classes named macro_styles. These classes were defined based on shared properties among the beers. Initially, ChatGPT was employed to extract the general structure, but it proved incomplete results. Subsequently, Craft Beer's comprehensive database, grouping styles by production procedure, color, bitterness, and alcohol level, was utilized for a more accurate classification.

### Main pre-processing:
We created an auxiliary python (main_preprocessing.py) script which can be run from the terminal and provide the users with the compressed and transformed data for the analysis. In particular it provides the above-mentioned analysis and standard pre-processing (filtering and unification of countries) explained in the notebook and webpage. 

### Text analysis:
Starting from the detrend dataset, we cleaned the reviews by eliminating stopwords, emoticons, emoji, URL, email addresses and numbers. The text was then normalized through lemmatization to reduce words to their canonical form (lemma) and tokenized to see the different words of the reviews. The length of each review was then computed by counting the tokens. 

The TF-IDF is a method that tries to identify the most distinctively frequent or significant words in a document. It computes the multiplication of the Term Frequency (TF) and the Inverse Document Frequency (IDF). The TF captures the frequency of the word within each document while the IDF captures in how many documents each word appears. We computed the TF-IDF with scikit-learn library which prevents zero divisions in the IDF and computes the two terms as described in the notebook.

The function of the TF-IDF score is to allow to extract the top 3 most representative words for each review so to group them by the beer macro_style. By exploiting WordCloud representation we are then able to represent the most representative words used by the users to describe the beer_styles.

### Country recommender
Choosing a holiday destination is not easy and everyone does it based on their own criteria. For those who like to decide based on where they can find their favourite beers, we have developed a tool that recommends a country to visit based on your taste (and when you would like to do the trip).

To build it, we have analyzed which are the three most popular beers styles for each country for each season. As proxy for popularity, we have used the weighted average rating of each beer style produced in that country. The weighting has been done based on the score of the beer style and on the 'expertise' of the user voting, which is dependent on the number of ratings.

The recommender system is based on a Decision Tree constructed from this data: for each season, we have trained a decision tree to predict the country based on the 3 most popular beer styles as categorial variables. Since we only have one entry in our training datasets per each country, this is a trivial task in terms of machine learning and we obtain accuracies of around 85%. Misclassifications only happening when 2 or more countries happen to have the same 3 'top beers'.

Finally, to give a suggestion to the user we ask for their 3 favorite beer styles and when they want to travel and we input that to the corresponding decision tree.
![Country recommender site](src/country_recommender.png)

## Proposed deadlines:
 
03.11.23 – Analysis and understanding of data
 
06.11.23 – Preprocessing of text files to tsv format
 
09.11.23 – Detranding of herding effect to merge scores
 
17.11.23 – Pause project work
 
01.12.23 – Homework 2 deadline
  
03.12.23 – Seasonal, text analysis and breweries data extraction
 
08.12.23 – Building the predictor for countries

15.12.23 – Finalizing analysis to compute plots
 
18.12.23 – Provide data story and finalize webpage
 
22.12.23 - Milestone 3 deadline
 
## Organization of the team in terms of responsibility
 
Andrea: herding effect detrending, unification of databases and trimester analysis

Sebas: trimester analysis, macro-beer styles selection and pyplots expert

Cristina: text analysis, breweries analysis and webpage implementation

Sandra: data preprocessing, trimester analysis and predictor analysis (interactive plot)

Antonello: text analysis and breweries analysis and webpage implementation
 
We equally contribute to data story creation and initial preprocessing of the data. 