# 🚀 Cybersecurity AI Agent  

An AI-powered cybersecurity assistant that scans IP addresses for potential threats using multiple security APIs.  

## 📌 Features  
👉 Scan IPs for threats using VirusTotal, Shodan, and AbuseIPDB  
👉 AI-powered risk assessment using OpenAI SDK  
👉 FastAPI backend & Svelte frontend  
👉 Rate limiting & security best practices  

---

## 📂 Project Structure  
```
Cybersec-Assistant/
│── backend/              # FastAPI backend
│   ├── main.py           # API entry point
│   ├── security.py       # Security utilities
│   ├── api_clients.py    # API integrations
│   ├── requirements.txt  # Backend dependencies
│── frontend/             # Svelte frontend
│   ├── src/
│   ├── package.json
│   ├── tailwind.config.js
│── README.md             # Project documentation
│── .gitignore            # Ignore unnecessary files
```

---

## 🔧 Setup  

### 1️⃣ **Backend (FastAPI)**
```sh
cd backend
python -m venv venv  # Create virtual environment
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate  # (Windows)
pip install -r requirements.txt
uvicorn main:app --reload  # Run FastAPI
```

### 2️⃣ **Frontend (Svelte + TailwindCSS)**
```sh
cd frontend
npm install
npm run dev  # Start frontend
```

---

## 🚀 Usage  
1️⃣ Open `http://localhost:5173/` in your browser  
2️⃣ Enter an **IP address** and click **Scan**  
3️⃣ View AI-powered **threat analysis**  

---

## 🛠️ API Endpoints  
| Method | Endpoint               | Description                     |
|--------|------------------------|---------------------------------|
| `GET`  | `/scan/ip/{ip}`        | Scan IP for threats            |
| `GET`  | `/health`              | Check server status            |

---

## 🔒 Security  
👉 **CORS Protection** in FastAPI  
👉 **Rate Limiting** using SlowAPI  
👉 **API Key Handling** for external services  

---

## 💜 License  
MIT License  

---

## ⭐ Contribute  
1. Fork the repo  
2. Create a new branch  
3. Make changes & commit  
4. Open a pull request  

---

### 🔧 Git Setup  
Now commit & push it to GitHub:  
```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/cybersec-agent.git
git push -u origin main
```
