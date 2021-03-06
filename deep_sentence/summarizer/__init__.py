from __future__ import unicode_literals

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
# from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.utils import get_stop_words

from deep_sentence import settings
from deep_sentence.summarizer.models import abstractive as abstractive_summarizer
from deep_sentence.summarizer.utils.deduplicate_sentences import deduplicate_sentences

from . import text_extractor


try:
    unicode
except NameError:
    unicode = str

def summarize_text(text, sentences_count=3, language=settings.DEFAULT_LANGUAGE, as_list=False):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    sentences = [unicode(sentence) for sentence in summarizer(parser.document, sentences_count)]
    return sentences if as_list else '\n'.join(sentences)


def summarize_texts(texts, sentences_count=3, language=settings.DEFAULT_LANGUAGE, progress_callback=lambda _: None):
    options = {'sentences_count': sentences_count, 'language': language, 'as_list': True}
    documents = [summarize_text(text, **options) for text in texts]
    progress_callback(2)
    if documents and documents[0]:
        title = abstractive_summarizer.compute_title(documents[0][0])
        sentences = deduplicate_sentences(documents)
    else:
        title = 'no sentences could be extracted'
        sentences = []
    progress_callback(3)
    return (title, '\n'.join(sentences))


def summarize_url(url, sentences_count=3, language=settings.DEFAULT_LANGUAGE):
    [text] = text_extractor.extract_from_urls([url])
    return summarize_text(text, sentences_count=sentences_count, language=language)


def summarize_urls(urls, sentences_count=3, language=settings.DEFAULT_LANGUAGE, progress_callback=lambda _: None):
    texts = text_extractor.extract_from_urls(urls)
    progress_callback(1)
    return summarize_texts(texts, sentences_count=sentences_count, language=language, progress_callback=progress_callback)
