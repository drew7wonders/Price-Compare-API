from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Update to allow all origins in development

def scrape_snapdeal(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            product_name = soup.find('h1', class_='pdp-e-i-head')
            price_element = soup.find('span', class_='payBlkBig')

            if price_element:
                price = price_element.get_text(strip=True)
                return {"product_name": product_name.text.strip(), "product_price": price}

        return {"error": "Product is currently unavailable. Please try again later.", "price": response.status_code}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}

def scrape_flipkart(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html'
        }
        ch = 100
        response = requests.get(url, headers=headers)

        if response.status_code == 500:
            soup = BeautifulSoup(response.content, 'html.parser')
            ch = 101
            product_name = soup.find('span', class_='B_NuCI')
            price_element = soup.find('div', class_='_30jeq3 _16Jk6d')

            if product_name:
                product_name_text = product_name.get_text(strip=True)

                if price_element:
                    price = price_element.get_text(strip=True)
                    return {"product_name": product_name_text, "product_price": price}
                else:
                    return {"error": "Product price not found on the page.", "url": url}

        return {"error": "Product is currently unavailable. Please try again later.", "name": response.status_code, "ch": ch}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}

        
def scrape_amazon(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            product_name = soup.find('span', class_='a-size-large product-title-word-break')
            price_element = soup.find('span', class_='a-price-whole')

            if price_element:
                price = price_element.get_text(strip=True)
                return {"product_name": product_name.text.strip(), "product_price": pricel}  # Typo: should be "price"

        return {"error": "Product is currently unavailable. Please try again later.", "price": response.status_code}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
        
@app.route('/api/scrape', methods=['POST'])
def handle_scraping():
    data = request.get_json()

    url_amaz = data.get('amazon_url', '')
    result_amaz = scrape_amazon(url_amaz)
    
    url_snap = data.get('snapdeal_url', '')
    result_snap = scrape_snapdeal(url_snap)

    url_flip = data.get('flipkart_url', '')
    result_flip = scrape_flipkart(url_flip)


    ret = {"snap": result_snap, "flip": result_flip, "amaz": result_amaz}
    return jsonify(ret)

if __name__ == "__main__":
    # # Use Gunicorn as the production server
    # bind_address = os.getenv('BIND', '0.0.0.0')
    # bind_port = int(os.getenv('PORT', 5000))

    # print(f"Starting server on {bind_address}:{bind_port}")
    app.run()
