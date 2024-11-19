from bs4 import BeautifulSoup

class HTMLParser:
    def parse(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        components = {
            "tags": [tag.name for tag in soup.find_all()]
        }
        return components
