import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy


def DeleteCompany(Article):
    '''
    :param Article(String): The article content
    :return Article(String): Content after being deleted company name
    '''
    # load spacy model
    nlp = spacy.load('en_core_web_sm')
    # load data
    doc = nlp(Article)
    # Get entities
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            Article = Article.replace(ent.text, '') # delete Organize
    return Article

def PreProcess(Article):
    '''
    :param Article(String): The article content
    :return: FilteredTokens
    '''
    # Regular Expression/Normalization
    # punc = string.punctuation
    # NormedArticle = re.sub(r"[,|.|?|%|“|/|:|$|']+", ' ', NormedArticle) # remove
    NormedArticle = re.sub(r'[^\w\s]+', ' ', Article)  # remove punctuation
    NormedArticle = re.sub(r'[\d+]+', ' ', NormedArticle)  # remove numbers, only save words
    NormedArticle = NormedArticle.lower()  # lowercase the words
    # Tokenize
    WordTokens = word_tokenize(NormedArticle)
    # Remove Stop words and Lemmatization
    ps = PorterStemmer()
    Stopwords = stopwords.words('english')  # get the stopwords list from nltk
    FilteredTokens = [ps.stem(w) for w in WordTokens if not w in Stopwords]
    return FilteredTokens

if __name__ == "__main__":
    # Get the article content
    news = 'amazon-announces-premiere-date-for-as-we-see-it'
    TxtFileName = 'News/' + news + '.txt'
    with open(TxtFileName, "r") as file:
        Article = file.read()
    #Delete article
    Article = DeleteCompany(Article)
    #Pre processing
    FilteredTokens =  PreProcess(Article)
