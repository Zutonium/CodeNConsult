import http.server
import socketserver
import json
import os
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

PORT = 8080
DATA_FILE = os.path.join(os.path.dirname(__file__), 'grind_and_crumb_data', 'full_dashboard_data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

from test_ceo import get_ceo_response

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/data':
            data = load_data()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif parsed.path == '/' or parsed.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length)

        if parsed.path == '/api/chat':
            try:
                body = json.loads(post_body.decode('utf-8'))
                prompt = body.get('prompt', '')
                api_key = body.get('apiKey', '').strip()
                full_data = load_data()

                # If Gemini API key provided, try calling Google Gemini API
                if api_key:
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                        system_prompt = f"""You are the Executive AI Advisor for Anna Whitfield, CEO of Grind & Crumb, a 12-store specialty café chain.
Company Data: Total Sales £{full_data['chain']['total_revenue']:,.0f}, Profit £{full_data['chain']['total_profit']:,.0f} (Margin: {full_data['chain']['overall_margin']}%).
Key issues: Manchester Piccadilly (S07) loses -£49.7k due to £366k rent and lunch delivery bottlenecks; Leeds Trinity (S12) cannibalizes Leeds Briggate (S03) which wastes £16.6k food; 29% of delivery orders are under £8 losing money; Dashly increased commission to 33%; £1.5M budget should be deployed into CS3 Manchester Oxford Rd, CS4 York Station Kiosk, CS1 Headingley, and York refit, while avoiding CS7 Wellington Place (cannibalization trap) and CS2 Kelham Island.
Answer executive questions with concise, numbers-grounded, strategic advice."""

                        req_payload = {
                            "contents": [
                                {
                                    "role": "user",
                                    "parts": [{"text": f"{system_prompt}\n\nCEO Question: {prompt}"}]
                                }
                            ]
                        }
                        req = urllib.request.Request(
                            url,
                            data=json.dumps(req_payload).encode('utf-8'),
                            headers={'Content-Type': 'application/json'}
                        )
                        with urllib.request.urlopen(req, timeout=12) as response:
                            res_json = json.loads(response.read().decode('utf-8'))
                            answer = res_json['candidates'][0]['content']['parts'][0]['text']
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json; charset=utf-8')
                            self.end_headers()
                            self.wfile.write(json.dumps({'response': answer, 'source': 'gemini-api'}).encode('utf-8'))
                            return
                    except Exception as e:
                        # Fallback to local response engine if api call fails
                        pass

                # Fallback to local deep knowledge engine
                answer = get_ceo_response(prompt, full_data)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'response': answer, 'source': 'local-engine'}).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

        elif parsed.path == '/api/upload':
            try:
                body = json.loads(post_body.decode('utf-8'))
                file_name = body.get('fileName', 'uploaded.csv')
                csv_content = body.get('content', '')
                
                upload_dir = os.path.join(os.path.dirname(__file__), 'grind_and_crumb_data', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, file_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(csv_content)

                # Rebuild dataset
                import build_full_dataset
                build_full_dataset.build_full_dataset()
                updated_data = load_data()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': f'Uploaded and reprocessed {file_name}', 'data': updated_data}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = PORT
    for p in range(PORT, PORT + 10):
        try:
            with socketserver.TCPServer(("", p), DashboardHandler) as httpd:
                print(f"Grind & Crumb Executive Server running at http://localhost:{p}")
                httpd.serve_forever()
        except OSError:
            print(f"Port {p} occupied, trying next port...")
            continue

if __name__ == '__main__':
    run_server()
