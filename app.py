from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

# Your OkeyMeta authentication token
USER_AUTH_TOKEN = "okeyai_dde13dfd7746406fef0da923c704f14a946100d74053d2d3dc620690d1c084e0"
BASE_URL = "https://api.okeymeta.com.ng/api/ssailm/model/okeyai3.0-vanguard/okeyai"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user message from request
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Encode the message for URL
        encoded_message = urllib.parse.quote(user_message)
        full_url = f"{BASE_URL}?input={encoded_message}"
        
        # Set up headers
        headers = {
            "Authorization": f"Bearer {USER_AUTH_TOKEN}"
        }
        
        # Make request to OkeyMeta API
        response = requests.get(full_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Extract the bot's reply (adjust based on actual API response structure)
        bot_reply = data.get('response', data.get('output', str(data)))
        
        return jsonify({
            'success': True,
            'reply': bot_reply
        })
        
    except requests.exceptions.RequestException as e:
        error_message = f"API Error: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_message = e.response.json().get('error', error_message)
            except:
                error_message = e.response.text
        
        return jsonify({
            'success': False,
            'error': error_message
        }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)