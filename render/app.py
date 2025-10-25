from flask import Flask, request, jsonify, render_template_string
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf.json_format import MessageToJson
import binascii
import aiohttp
import requests
import json
import like_pb2
import like_count_pb2
import uid_generator_pb2
import os

app = Flask(__name__)

def load_tokens(server_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if server_name == "IND":
        with open(os.path.join(base_dir, "token_ind.json"), "r") as f:
            return json.load(f)
    elif server_name in {"BR", "US", "SAC", "NA"}:
        with open(os.path.join(base_dir, "token_br.json"), "r") as f:
            return json.load(f)
    else:
        with open(os.path.join(base_dir, "token_bd.json"), "r") as f:
            return json.load(f)

def encrypt_message(plaintext):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return binascii.hexlify(encrypted_message).decode('utf-8')

def create_protobuf_message(user_id, region):
    message = like_pb2.like()
    message.uid = int(user_id)
    message.region = region
    return message.SerializeToString()

async def send_request(encrypted_uid, token, url):
    edata = bytes.fromhex(encrypted_uid)
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB50"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=edata, headers=headers) as response:
                return response.status
    except Exception as e:
        print(f"Request failed: {e}")
        return 500

async def send_multiple_requests(uid, server_name, url, num_requests):
    region = server_name
    protobuf_message = create_protobuf_message(uid, region)
    encrypted_uid = encrypt_message(protobuf_message)
    tasks = []
    tokens = load_tokens(server_name)
    
    for i in range(num_requests):
        token = tokens[i % len(tokens)]["token"]
        tasks.append(send_request(encrypted_uid, token, url))
    
    results = await asyncio.gather(*tasks)
    return results

def create_protobuf(uid):
    message = uid_generator_pb2.uid_generator()
    message.krishna_ = int(uid)
    message.teamXdarks = 1
    return message.SerializeToString()

def enc(uid):
    protobuf_data = create_protobuf(uid)
    encrypted_uid = encrypt_message(protobuf_data)
    return encrypted_uid

def make_request(encrypt, server_name, token):
    if server_name == "IND":
        url = "https://client.ind.freefiremobile.com/GetPlayerPersonalShow"
    elif server_name in {"BR", "US", "SAC", "NA"}:
        url = "https://client.us.freefiremobile.com/GetPlayerPersonalShow"
    else:
        url = "https://clientbp.ggblueshark.com/GetPlayerPersonalShow"

    edata = bytes.fromhex(encrypt)
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB50"
    }

    response = requests.post(url, data=edata, headers=headers)
    hex_data = response.content.hex()
    binary = bytes.fromhex(hex_data)
    return decode_protobuf(binary)

def decode_protobuf(binary):
    try:
        items = like_count_pb2.Info()
        items.ParseFromString(binary)
        return items
    except Exception as e:
        print(f"Error decoding Protobuf data: {e}")
        return None

INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Fire Like Increaser</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            padding: 20px; 
        }
        .container { 
            background: rgba(255, 255, 255, 0.95); 
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); 
            max-width: 500px; 
            width: 100%; 
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { 
            color: #667eea; 
            font-size: 2em; 
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .neon-text {
            color: #00ff88;
            text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88, 0 0 30px #00ff88;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .developer-btn {
            display: inline-block;
            background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
            color: #000;
            padding: 10px 25px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            margin: 10px 0;
            transition: transform 0.3s;
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4);
        }
        .developer-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 255, 136, 0.6);
        }
        .join-channel {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.9em;
            margin: 10px 0;
            transition: all 0.3s;
        }
        .join-channel:hover {
            background: #764ba2;
            transform: translateY(-2px);
        }
        .server-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 1.2em;
            margin: 20px 0;
            display: inline-block;
        }
        .form-group { margin-bottom: 20px; }
        .form-group label { 
            display: block; 
            margin-bottom: 8px; 
            color: #333; 
            font-weight: 600; 
            font-size: 0.95em; 
        }
        .form-group input { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e0e0e0; 
            border-radius: 10px; 
            font-size: 1.1em; 
            transition: all 0.3s; 
        }
        .form-group input:focus { 
            outline: none; 
            border-color: #667eea; 
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); 
        }
        .btn { 
            width: 100%; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 18px; 
            border: none; 
            border-radius: 10px; 
            font-size: 1.2em; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.3s; 
        }
        .btn:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4); 
        }
        .btn:active { transform: translateY(-1px); }
        .btn:disabled { 
            opacity: 0.6; 
            cursor: not-allowed; 
            transform: none; 
        }
        .result { 
            margin-top: 20px; 
            padding: 20px; 
            border-radius: 10px; 
            display: none; 
        }
        .result.show { display: block; }
        .result.success { 
            background: #e8f5e9; 
            border-left: 4px solid #4caf50; 
            color: #2e7d32; 
        }
        .result.error { 
            background: #ffebee; 
            border-left: 4px solid #f44336; 
            color: #c62828; 
        }
        .result h4 { margin-bottom: 10px; font-size: 1.1em; }
        .result p { margin: 5px 0; }
        .loading { display: none; text-align: center; padding: 20px; }
        .loading.show { display: block; }
        .spinner { 
            border: 4px solid #f3f3f3; 
            border-top: 4px solid #667eea; 
            border-radius: 50%; 
            width: 50px; 
            height: 50px; 
            animation: spin 1s linear infinite; 
            margin: 0 auto 15px; 
        }
        @keyframes spin { 
            0% { transform: rotate(0deg); } 
            100% { transform: rotate(360deg); } 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Free Fire Like Increaser</h1>
            <p style="margin: 10px 0; color: #666;">In neon developer:</p>
            <a href="https://t.me/thethestar" target="_blank" class="developer-btn">Piyush XD</a>
            <br>
            <a href="https://t.me/neopie/projects" target="_blank" class="join-channel">Join Channel</a>
            <br>
            <div class="server-badge">🇮🇳 IND SERVER (ULTRA NEON)</div>
        </div>
        <form id="likeForm">
            <div class="form-group">
                <label for="uid">Enter User ID (UID)</label>
                <input type="text" id="uid" placeholder="e.g., 123456789" required>
            </div>
            <button type="submit" class="btn" id="sendBtn">🚀 Send Likes</button>
        </form>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="color: #667eea; font-weight: 600;">Sending likes...</p>
        </div>
        <div class="result" id="result">
            <h4 id="resultTitle">Result</h4>
            <p id="resultMessage"></p>
        </div>
    </div>
    <script>
        const API_URL = window.location.origin;
        const API_KEY = 'gst';
        const SERVER = 'IND';
        
        document.getElementById('likeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const uid = document.getElementById('uid').value.trim();
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const sendBtn = document.getElementById('sendBtn');
            
            if (!uid) { alert('Please enter a valid UID'); return; }
            
            loading.classList.add('show');
            result.classList.remove('show', 'success', 'error');
            sendBtn.disabled = true;
            
            try {
                const response = await fetch(`${API_URL}/like?uid=${uid}&server_name=${SERVER}&key=${API_KEY}`);
                const data = await response.json();
                
                loading.classList.remove('show');
                result.classList.add('show');
                
                if (data.status === 1 && data.LikesGivenByAPI > 0) {
                    result.classList.add('success');
                    document.getElementById('resultTitle').textContent = '✅ Success!';
                    document.getElementById('resultMessage').innerHTML = `
                        <p><strong>Player:</strong> ${data.PlayerNickname} (${data.UID})</p>
                        <p><strong>Likes Sent:</strong> ${data.LikesGivenByAPI}</p>
                        <p><strong>Before:</strong> ${data.LikesBeforeCommand} → <strong>After:</strong> ${data.LikesAfterCommand}</p>
                        <p><strong>Success Rate:</strong> ${data.SuccessRate}</p>
                    `;
                } else if (data.error) {
                    result.classList.add('error');
                    document.getElementById('resultTitle').textContent = '❌ Error';
                    document.getElementById('resultMessage').textContent = data.error;
                } else {
                    result.classList.add('error');
                    document.getElementById('resultTitle').textContent = '⚠️ Warning';
                    document.getElementById('resultMessage').textContent = 'No likes were sent. Please try again.';
                }
            } catch (error) {
                loading.classList.remove('show');
                result.classList.add('show', 'error');
                document.getElementById('resultTitle').textContent = '❌ Error';
                document.getElementById('resultMessage').textContent = 'Failed to connect to server. Please try again.';
            } finally {
                sendBtn.disabled = false;
            }
        });
    </script>
</body>
</html>'''

ADMIN_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MaxLikes API - Admin Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: rgba(255, 255, 255, 0.95); padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2); margin-bottom: 30px; text-align: center; }
        .header h1 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
        .header p { color: #666; font-size: 1.1em; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); text-align: center; transition: transform 0.3s; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card h3 { color: #667eea; font-size: 1.1em; margin-bottom: 15px; }
        .stat-card .value { font-size: 2.5em; font-weight: bold; color: #333; margin-bottom: 5px; }
        .stat-card .label { color: #999; font-size: 0.9em; }
        .panel { background: rgba(255, 255, 255, 0.95); padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2); margin-bottom: 30px; }
        .panel h2 { color: #667eea; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #f0f0f0; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #333; font-weight: 500; }
        .form-group input, .form-group select { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1em; transition: border-color 0.3s; }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #667eea; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; transition: transform 0.2s; font-weight: 600; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .btn:active { transform: translateY(0); }
        .result { margin-top: 20px; padding: 20px; border-radius: 8px; background: #f8f9fa; border-left: 4px solid #667eea; display: none; }
        .result.show { display: block; }
        .result pre { background: #fff; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 0.9em; margin-top: 10px; }
        .server-status { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 20px; }
        .server-badge { padding: 15px; border-radius: 8px; text-align: center; font-weight: 600; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .api-info { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 15px; }
        .api-info code { background: #fff; padding: 2px 6px; border-radius: 4px; color: #667eea; font-weight: 600; }
        .loading { display: none; text-align: center; padding: 20px; }
        .loading.show { display: block; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .error { background: #fee; border-left-color: #f44336; color: #c00; }
        .success { background: #efe; border-left-color: #4caf50; color: #060; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 MaxLikes API Admin Panel</h1>
            <p>Monitor, Test & Manage Your Game Like API</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><h3>API Status</h3><div class="value" id="apiStatus">🟢</div><div class="label">Online</div></div>
            <div class="stat-card"><h3>Total Servers</h3><div class="value">6</div><div class="label">IND, BR, US, SAC, NA, BD</div></div>
            <div class="stat-card"><h3>Requests Today</h3><div class="value" id="requestCount">-</div><div class="label">Live Counter</div></div>
            <div class="stat-card"><h3>API Key</h3><div class="value" style="font-size: 1.5em;">gst</div><div class="label">Authentication</div></div>
        </div>
        <div class="panel">
            <h2>🧪 Test API Endpoint</h2>
            <form id="testForm">
                <div class="form-group"><label for="uid">User ID (UID)</label><input type="text" id="uid" name="uid" placeholder="Enter User ID (e.g., 123456789)" required></div>
                <div class="form-group"><label for="server">Server Region</label><select id="server" name="server" required><option value="IND">IND - India</option><option value="BR">BR - Brazil</option><option value="US">US - United States</option><option value="SAC">SAC - South America</option><option value="NA">NA - North America</option><option value="BD">BD - Bangladesh</option></select></div>
                <div class="form-group"><label for="likes">Number of Tokens to Use (Optional)</label><input type="text" id="likes" name="likes" placeholder="Leave empty to use ALL tokens, or enter number/max"></div>
                <button type="submit" class="btn">🚀 Send Request</button>
            </form>
            <div class="loading" id="loading"><div class="spinner"></div><p style="margin-top: 15px; color: #667eea; font-weight: 600;">Processing request...</p></div>
            <div class="result" id="result"><h3 style="margin-bottom: 10px; color: #667eea;">Response:</h3><pre id="resultContent"></pre></div>
        </div>
        <div class="panel">
            <h2>📡 Server Status</h2>
            <div class="server-status">
                <div class="server-badge">IND</div><div class="server-badge">BR</div><div class="server-badge">US</div><div class="server-badge">SAC</div><div class="server-badge">NA</div><div class="server-badge">BD</div>
            </div>
            <div class="api-info"><p><strong>API Endpoint:</strong> <code>/like</code></p><p><strong>Method:</strong> GET</p><p><strong>Authentication:</strong> API Key (gst)</p></div>
        </div>
        <div class="panel">
            <h2>📖 API Documentation</h2>
            <div class="api-info">
                <h3 style="margin-bottom: 10px;">Endpoint Structure:</h3>
                <code>GET /like?uid={USER_ID}&server_name={SERVER}&key=gst&like={OPTIONAL}</code>
                <h3 style="margin-top: 20px; margin-bottom: 10px;">Parameters:</h3>
                <ul style="margin-left: 20px; line-height: 1.8;">
                    <li><strong>uid</strong> (required) - User ID to send likes to</li>
                    <li><strong>server_name</strong> (required) - Server region (IND, BR, US, SAC, NA, BD)</li>
                    <li><strong>key</strong> (required) - API authentication key (currently: "gst")</li>
                    <li><strong>like</strong> (optional) - Number of tokens to use (omit for ALL tokens)</li>
                </ul>
                <h3 style="margin-top: 20px; margin-bottom: 10px;">Example URLs:</h3>
                <p style="margin: 10px 0;"><code>/like?uid=123456789&server_name=IND&key=gst</code> - Use ALL tokens</p>
                <p style="margin: 10px 0;"><code>/like?uid=123456789&server_name=IND&key=gst&like=500</code> - Use 500 tokens</p>
                <p style="margin: 10px 0;"><code>/like?uid=123456789&server_name=IND&key=gst&like=max</code> - Use max tokens</p>
            </div>
        </div>
    </div>
    <script>
        let requestCounter = 0;
        function updateRequestCount() { document.getElementById('requestCount').textContent = requestCounter; }
        document.getElementById('testForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const uid = document.getElementById('uid').value;
            const server = document.getElementById('server').value;
            const likes = document.getElementById('likes').value;
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const resultContent = document.getElementById('resultContent');
            loading.classList.add('show');
            result.classList.remove('show', 'error', 'success');
            let url = `/like?uid=${uid}&server_name=${server}&key=gst`;
            if (likes) { url += `&like=${likes}`; }
            try {
                const response = await fetch(url);
                const data = await response.json();
                loading.classList.remove('show');
                result.classList.add('show');
                if (data.status === 1) { result.classList.add('success'); } else if (data.error) { result.classList.add('error'); }
                resultContent.textContent = JSON.stringify(data, null, 2);
                requestCounter++;
                updateRequestCount();
            } catch (error) {
                loading.classList.remove('show');
                result.classList.add('show', 'error');
                resultContent.textContent = 'Error: ' + error.message;
            }
        });
        updateRequestCount();
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/ok.html')
def admin_panel():
    return render_template_string(ADMIN_HTML)

@app.route('/like', methods=['GET'])
def handle_requests():
    uid = request.args.get("uid")
    server_name = request.args.get("server_name", "").upper()
    key = request.args.get("key")
    like_param = request.args.get("like")

    if key != "gst":
        return jsonify({"error": "Invalid or missing API key 🔑"}), 403

    if not uid or not server_name:
        return jsonify({"error": "UID and server_name are required"}), 400

    try:
        tokens_data = load_tokens(server_name)
    except FileNotFoundError:
        return jsonify({"error": f"Token file for server {server_name} not found"}), 500
    except Exception as e:
        return jsonify({"error": f"Error loading tokens: {str(e)}"}), 500

    token = tokens_data[0]['token']
    encrypt = enc(uid)
    
    total_tokens = len(tokens_data)
    
    if like_param:
        if like_param.lower() == "max":
            num_requests = total_tokens
        else:
            try:
                num_requests = int(like_param)
                if num_requests > total_tokens:
                    num_requests = total_tokens
                elif num_requests < 1:
                    num_requests = 1
            except ValueError:
                num_requests = total_tokens
    else:
        num_requests = total_tokens

    before = make_request(encrypt, server_name, token)
    if before is None:
        return jsonify({
            "error": "Failed to connect to game server. Tokens may be invalid or expired.",
            "status": 503
        }), 503
    
    jsone = MessageToJson(before)
    data = json.loads(jsone)
    before_like = int(data['AccountInfo'].get('Likes', 0))

    if server_name == "IND":
        url = "https://client.ind.freefiremobile.com/LikeProfile"
    elif server_name in {"BR", "US", "SAC", "NA"}:
        url = "https://client.us.freefiremobile.com/LikeProfile"
    else:
        url = "https://clientbp.ggblueshark.com/LikeProfile"

    results = asyncio.run(send_multiple_requests(uid, server_name, url, num_requests))
    
    successful_requests = sum(1 for status in results if status == 200)
    failed_requests = len(results) - successful_requests
    success_rate = (successful_requests / len(results) * 100) if results else 0

    after = make_request(encrypt, server_name, token)
    if after is None:
        return jsonify({
            "error": "Failed to retrieve updated data from game server.",
            "status": 503
        }), 503
    
    jsone = MessageToJson(after)
    data = json.loads(jsone)

    after_like = int(data['AccountInfo']['Likes'])
    id = int(data['AccountInfo']['UID'])
    name = str(data['AccountInfo']['PlayerNickname'])

    like_given = after_like - before_like
    status = 1 if like_given != 0 else 2

    result = {
        "LikesGivenByAPI": like_given,
        "LikesAfterCommand": after_like,
        "LikesBeforeCommand": before_like,
        "PlayerNickname": name,
        "UID": id,
        "status": status,
        "TotalTokensAvailable": total_tokens,
        "TokensUsed": num_requests,
        "SuccessfulRequests": successful_requests,
        "FailedRequests": failed_requests,
        "SuccessRate": f"{success_rate:.1f}%"
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
