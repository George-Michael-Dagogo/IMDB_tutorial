# %%
#the time span of the comments
#word count/ frequncy
#number of words in each comment after stopwords have beenremoved
#length of reviews
#display of language
#dropping none english reviews
#word cloud
#top keywords

#! pip install spacy spacy-langdetect
#! python -m spacy download en_core_web_sm

# %% [markdown]
# ## Merging all csv files 

# %%
import os
import pandas as pd

# Set the paths to the folders
folder_paths = ["/workspace/IMDB_tutorial/Tari_csv/Attractions", "/workspace/IMDB_tutorial/Tari_csv/Hotels", "/workspace/IMDB_tutorial/Tari_csv/Restaurants"]

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Loop through each folder
for folder_path in folder_paths:
    # Get the list of CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    print('1')
    
    # Loop through each CSV file in the folder
    for csv_file in csv_files:
        # Construct the full path to the CSV file
        file_path = os.path.join(folder_path, csv_file)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path,lineterminator='\n')
        
        print('2')
        # Concatenate the DataFrame to the merged_data
        merged_data = pd.concat([merged_data, df], ignore_index=True)

# Write the merged data to a new CSV file
merged_data = merged_data.drop('title', axis=1)
reddit_data = pd.read_csv('/workspace/IMDB_tutorial/Tari_csv/london_reddit_merged_data.csv')
merged_full_data = pd.concat([merged_data, reddit_data], ignore_index=True)
merged_full_data.to_csv("/workspace/IMDB_tutorial/Tari_csv/merged_full_data.csv", index=False)


# %%
import pandas as pd
ed = pd.read_csv("/workspace/IMDB_tutorial/Tari_csv/merged_full_data.csv",lineterminator='\n')
ed

# %% [markdown]
# ## Word count without stopwords

# %%
import pandas as pd
import nltk
from nltk.corpus import stopwords

# Download the stopwords dataset
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
# Function to count words without stopwords
def count_words_without_stopwords(text):
    # Check if the value is a string or bytes-like object
    if isinstance(text, (str, bytes)):
        # Tokenize the text
        words = nltk.word_tokenize(str(text))
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]
        
        # Return the count of non-stopwords
        return len(filtered_words)
    else:
        # If the value is not a string or bytes-like, return 0
        return 0
# Apply the function to the 'Text' column and create a new column 'WordCount'
ed['WordCount'] = ed['content'].apply(count_words_without_stopwords)

# Display the DataFrame with word counts
ed




# %% [markdown]
# ## Detecting language

# %%
import pandas as pd
import langid
from iso639 import languages

# Function to detect language using langid
def detect_language(text):
    # Convert NaN to an empty string
    text = str(text) if pd.notna(text) else ''
    
    # Use langid to detect the language
    lang, confidence = langid.classify(text)
    return lang
# Apply the function to the 'Text' column and create a new column 'Language'
ed['Language'] = ed['content'].apply(detect_language)

ed['Language'] = ed['Language'].apply(lambda x: languages.get(alpha2=x).name)
ed


# %% [markdown]
# ## Language distribution with en

# %%
import matplotlib.pyplot as plt
ed['Language'].value_counts().plot(kind='bar', color='skyblue', figsize=(10, 6))

plt.title('Language Distribution')
plt.xlabel('Language')
plt.ylabel('Count')
plt.show()

# %% [markdown]
# ## Language distribution without en

# %%
filtered_data = ed[ed['Language'] != 'en']

# Plot the counts after excluding 'en'
filtered_data['Language'].value_counts().plot(kind='bar', color='skyblue', figsize=(10, 6))

plt.title('Language Distribution (excluding "en")')
plt.xlabel('Language')
plt.ylabel('Count')
plt.show()


# %% [markdown]
# ## Top Keywords

# %%
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import string

nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Convert to lowercase
    tokens = [word.lower() for word in tokens]
    
    # Remove punctuation
    tokens = [word for word in tokens if word.isalnum()]
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return tokens

def get_top_keywords(tokens, top_n=40):
    # Calculate word frequencies
    freq_dist = FreqDist(tokens)
    
    # Get the top N keywords
    top_keywords = freq_dist.most_common(top_n)
    
    return top_keywords

text_data_column = ed['content']

# Convert the column values to a single text variable
text_data = ' '.join(text_data_column.astype(str).tolist())

# Preprocess the text
preprocessed_tokens = preprocess_text(text_data)

# Get the top keywords
top_keywords = get_top_keywords(preprocessed_tokens)

# Print or use the top keywords
print(top_keywords)


# %% [markdown]
# ## Word Cloud

# %%
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Convert the list of tuples to a dictionary for WordCloud input
wordcloud_dict = dict(top_keywords)

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_dict)

# Display the WordCloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Turn off the axis labels
plt.show()




