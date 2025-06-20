##  Setup Instructions(Backend)

### 1. Clone the Repository

```bash
git clone https://github.com/nav-jk/chatgpt-financial-bot-backend.git
cd chatgpt-financial-bot-backend/chatgpt-financial-bot-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Set Environment Variables

Create a .env file in the root directory:

```bash
OPEN_AI_KEY=your_openai_api_key
# OPEN_AI_ORG=your_optional_org_id
ELEVENLABS_KEY=your_elevenlabs_api_key
```

### 4. Run the Server
```bash
uvicorn main:app --reload
```
##  API Endpoints
## 'POST /talk'

**Description:**
Accepts an audio file via form-data, transcribes it, gets a chat response using GPT, and returns an audio reply.

**Returns:**
MP3 audio file of the assistant's response.

## 'GET /clear'

**Description:**
Clears the chat history stored in database.json.

**Returns:**
```json
{ "message": "Chat history has been cleared" }
```
##  Setup Instructions(Frontend)

Move to root directory and 
```bash
cd financial-bot-frontend
```

```bash
npm install
npm start
```
Or optionally
```bash
npm run dev
```

```The app should open in your browser at http://localhost:3000.```

```The frontend expects the backend to run at http://localhost:8000 if not make required changes in App.jsx```
