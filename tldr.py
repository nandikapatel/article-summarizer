#importing libraries
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request  
import nltk

# getting the page from the URL
# replace this place-filler URL with any URL of your choice!
web_page = urllib.request.urlopen('https://en.wikipedia.org/wiki/Vincent_van_Gogh')

# extracting the article from the page
article = BeautifulSoup.BeautifulSoup(web_page.read(),'html.parser')

# getting all the <p> tags in the article
paragraphs = article.find_all('p')

article_content = ''

# add the contents of each paragraph to the article_content string
for p in paragraphs:  
    article_content += p.text


def _create_dictionary_table(text) -> dict:
   
    # eleminate all stop words
    stop_words = set(stopwords.words("english"))
    
    words = word_tokenize(text)
    
    # reduce words to their root form
    root = PorterStemmer()
    
    # make a dictionary for the word frequency table
    freq = dict()
    for word in words:
        word = root.stem(word)
        if word in stop_words:
            continue
        if word in freq:
            freq [word] += 1
        else:
            freq [word] = 1

    return freq


def _calculate_sentence_scores(sentences, freq) -> dict:   

    # sort sentences by their words and the wieght of the frequency of the words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in freq:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight [sentence[:7]] += freq [word_weight]
                else:
                    sentence_weight [sentence[:7]] = freq [word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

       

    return sentence_weight

def _calculate_average_score(sentence_weight) -> int:
   
    # calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score

def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary

def _run_article_summary(article):
    
    # creating a dictionary for the word frequency table
    freq = _create_dictionary_table(article)

    # tokenizing the sentences
    sentences = sent_tokenize(article)

    # algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, freq)

    #getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    # producing the summary
    article_summary = _get_article_summary(sentences, sentence_scores, 1.5 * threshold)

    return article_summary

if __name__ == '__main__':
    summary_results = _run_article_summary(article_content)
    print(summary_results)
