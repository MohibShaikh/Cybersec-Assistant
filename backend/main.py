from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from utils import scan_virustotal, scan_shodan, scan_abuseipdb
from fastapi.responses import JSONResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "AI Security Agent is running!"}


@app.get("/scan/ip/{ip_address}")
async def scan_ip(ip_address: str):
    vt_result = scan_virustotal(ip_address)
    shodan_result = scan_shodan(ip_address)
    abuseipdb_result = scan_abuseipdb(ip_address)

    return {
        "VirusTotal": vt_result,
        "Shodan": shodan_result,
        "AbuseIPDB": abuseipdb_result
    }