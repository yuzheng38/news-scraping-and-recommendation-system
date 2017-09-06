import cnn_news_scraper
import techcrunch_scraper

""" cnn news scraper test"""
NEWS_URL = 'http://edition.cnn.com/2017/01/17/us/fort-lauderdale-shooter-isis-claim/index.html'
EXPECTED_RESULT = "Ferlazzo, who conducted the interview in Miramar, said only that Santiago claimed to be fighting for ISIS and that he'd been in touch via jihadi chat rooms with like-minded people who were planning attacks as well. Santiago is charged with using and carrying a firearm during and in relation to a crime of violence; performing an act of violence against a person at an airport serving international civil aviation that caused serious bodily injury; and causing the death of a person through the use of a firearm."

def test_basic(url=NEWS_URL):
    news = cnn_news_scraper.extract_news(url)

    print news
    assert EXPECTED_RESULT in news
    print 'test_basic passed'

""" techcrunch scraper test """

if __name__ == '__main__':
    test_basic()