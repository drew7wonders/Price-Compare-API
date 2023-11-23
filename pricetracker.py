from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html'
        }

    def scrape_snapdeal(self):
        try:
            response = requests.get(self.url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_name = soup.find('h1', class_='pdp-e-i-head')
                price_element = soup.find('span', class_='payBlkBig')

                if price_element:
                    price = price_element.get_text(strip=True)
                    return {"product_name": product_name.text.strip(), "product_price": price}

            return {"error": "Product is currently unavailable. Please try again later.", "url":self.url}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request Error: {str(e)}"}

        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    def scrape_flipkart(self):
        try:
            response = requests.get(self.url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_name = soup.find('span', class_='B_NuCI')
                price_element = soup.find('div', class_='_30jeq3 _16Jk6d')

                if price_element:
                    price = price_element.get_text(strip=True)
                    return {"product_name": product_name.text.strip(), "product_price": price}

            return {"error": "Product is currently unavailable. Please try again later.", "url":self.url}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request Error: {str(e)}"}

        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    def scrape_amazon(self):
        try:
            response = requests.get(self.url, headers=self.headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_name = soup.find('span', class_='a-size-large product-title-word-break')
                price_element = soup.find('span', class_='a-price-whole')

                if price_element:
                    price = price_element.get_text(strip=True)
                    return {"product_name": product_name.text.strip(), "product_price": price}

            return {"error": "Product is currently unavailable. Please try again later.", "url":self.url}

        except requests.exceptions.RequestException as e:
            return {"error": f"Request Error: {str(e)}"}

        except Exception as e:
            return {"error": f"Error: {str(e)}"}

@app.route('/scrape', methods=['POST'])
def handle_scraping():
    data = request.get_json()

    url_snap = data.get('snapdeal_url', '')
    url_flip = data.get('flipkart_url', '')
    url_amaz = data.get('amazon_url', '')

    scraper_snapdeal = Scraper(url_snap)
    result_snap = scraper_snapdeal.scrape_snapdeal()

    scraper_flipkart = Scraper(url_flip)
    result_flip = scraper_flipkart.scrape_flipkart()

    scraper_amazon = Scraper(url_amaz)
    result_amaz = scraper_amazon.scrape_amazon()

    ret = {"snap": result_snap, "flip": result_flip, "amaz": result_amaz}
    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True, port=5003, threaded=True)
