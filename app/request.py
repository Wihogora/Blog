import urllib.request,json
from .models import Quotes
def configure_request(app):
    global base_url
    base_url= app.config['QUOTES_URL']

def get_quotes():
    '''
    function that get the json response to our url request
    '''
    get_quote_url="http://quotes.stormconsultancy.co.uk/random.json"
    quotes_object = None
    with urllib.request.urlopen(get_quote_url)as url:
        get_data = url.read()
        get_response = json.loads(get_data)
        id = get_response.get('id')
        author = get_response.get('author')
        quote = get_response.get('quote')
       
        # category = news_item.get('category')
        # language = news_item.get('language')
        # country = news_item.get('country')
        quotes_object = Quotes(id,author,quote)

    return quotes_object