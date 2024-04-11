from glob import glob
import pickle
#import spacy
import pandas as pd
import sys
import json

# Load the spaCy language model
# nlp = spacy.load("en_core_web_lg")  # or "en_core_web_lg" for higher accuracy

def preprocess_text(text):
    """Tokenize and normalize the text."""
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if not token.is_punct]
    return tokens


def highlight_semantically_similar_words(paragraph, phrases, similarity_threshold=0.7):
    """Highlight words in the paragraph that are semantically similar to the given phrase."""
    processed_paragraph = preprocess_text(paragraph)
    processed_phrases = [nlp(phrase.lower()) for phrase in phrases]
    sims = 0

    highlighted_paragraph = []
    for word in processed_paragraph:
        processed_word = nlp(word)
        similarities = [processed_phrase.similarity(processed_word) for processed_phrase in processed_phrases]
        if any([(similarity >= similarity_threshold) for similarity in similarities]):
            sims += 1
            highlighted_word = f">>>    {word}    <<<"
        else:
            highlighted_word = word
        highlighted_paragraph.append(highlighted_word)

    # Reconstruct the paragraph with highlighted words
    if sims > 0:
        return ' '.join(highlighted_paragraph)
    else:
        return None


def highlight_similar_sentences(paragraph, phrase, similarity_threshold=0.7):
    """Highlight sentences in the paragraph that are semantically similar to the given phrase."""
    doc = nlp(paragraph)
    processed_phrase = nlp(phrase)
    highlighted_paragraph = []
    sims = 0

    for sent in doc.sents:
        sentence_similarity = processed_phrase.similarity(sent)
        if sentence_similarity >= similarity_threshold:
            # Sentence is similar; highlight it
            sims += 1
            highlighted_paragraph.append(f">>>                {sent.text}                <<<")
        else:
            highlighted_paragraph.append(sent.text)

    # Reconstruct the paragraph with highlighted sentences
    if sims > 0:
        return " ".join(highlighted_paragraph)
    else:
        return None



def is_relevant(title_abstract):
    return ('expert' in title_abstract.lower()) and \
       ('search' in title_abstract.lower()) and \
       ('recommendation system' not in title_abstract.lower())

def filter_papers(input_files):
    for fn in input_files:
        with open(fn, 'r') as f:
            papers = json.load(f)
            for paper in papers:
                abstract = paper.get('abstract') or ''
                title = paper.get('title') or ''
                relevance = is_relevant(title + abstract)
                if relevance:
                    print(title)
                    print(abstract)
                    print("\n")
                    print("-"*40)

if __name__ == '__main__':
    input_files = sys.argv[1:]
    print('Filtering:')
    for fn in input_files:
        print(f'\t{fn}')
    print('=' * 40)
    filter_papers(input_files)
