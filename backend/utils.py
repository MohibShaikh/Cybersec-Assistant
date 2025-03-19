import os
import requests
import openai
import json
from dotenv import load_dotenv

# Load API keys
load_dotenv()
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI setup
openai.api_key = OPENAI_API_KEY

def scan_virustotal(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def scan_shodan(ip):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
    response = requests.get(url)
    return response.json()

def scan_abuseipdb(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": "90"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def analyze_scan_results(scan_results):
    """
    Analyzes scan results and categorizes the threat level.
    """
    return "The IP has been flagged for multiple malicious activities. Proceed with caution."

def classify_threat(scan_results):
    """
    Classifies the threat level based on scan results.
    """
    # Example logic: If VirusTotal shows more than 5 detections, mark as 'High'
    if scan_results.get("VirusTotal", {}).get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0) > 5:
        return "High"
    return "Low to Moderate"

def suggest_remediation(threat_level):
    """
    Suggests actions based on the threat level.
    """
    if threat_level == "High":
        return "Block the IP immediately and monitor for further attacks."
    return "Monitor the IP for unusual activity."

def calculate_reputation_score(scan_results):
    """
    Assigns a numerical risk score based on the scan results.
    """
    malicious_reports = scan_results.get("VirusTotal", {}).get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0)
    abuse_score = scan_results.get("AbuseIPDB", {}).get("data", {}).get("abuseConfidenceScore", 0)
    
    # Weighted scoring system
    score = (malicious_reports * 10) + (abuse_score * 2)
    
    return min(score, 100)

def analyze_with_openai(ip, results):
    """
    Uses OpenAI's function calling to analyze scan results and perform various security tasks.
    """
    functions = [
        {
            "name": "analyze_scan_results",
            "description": "Analyzes scan results and returns a summary of the threat level.",
            "parameters": {
                "type": "object",
                "properties": {
                    "scan_results": {
                        "type": "object",
                        "description": "The scan results from various security APIs."
                    }
                },
                "required": ["scan_results"]
            }
        },
        {
            "name": "classify_threat",
            "description": "Classifies the IP threat level based on scan results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "scan_results": {
                        "type": "object",
                        "description": "The scan results from security APIs."
                    }
                },
                "required": ["scan_results"]
            }
        },
        {
            "name": "suggest_remediation",
            "description": "Suggests remediation actions based on the threat level.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threat_level": {
                        "type": "string",
                        "description": "Threat level classification (e.g., Low, Moderate, High)."
                    }
                },
                "required": ["threat_level"]
            }
        },
        {
            "name": "calculate_reputation_score",
            "description": "Calculates a reputation score for the IP address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "scan_results": {
                        "type": "object",
                        "description": "The scan results from security APIs."
                    }
                },
                "required": ["scan_results"]
            }
        }
    ]

    prompt = f"""
    Analyze the following scan results for IP {ip}:

    VirusTotal: {results['VirusTotal']}
    Shodan: {results['Shodan']}
    AbuseIPDB: {results['AbuseIPDB']}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a cybersecurity AI agent."},
            {"role": "user", "content": prompt}
        ],
        functions=functions,
        function_call="auto"
    )

    message = response["choices"][0]["message"]

    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])

        if function_name == "analyze_scan_results":
            return analyze_scan_results(function_args["scan_results"])
        elif function_name == "classify_threat":
            return classify_threat(function_args["scan_results"])
        elif function_name == "suggest_remediation":
            return suggest_remediation(function_args["threat_level"])
        elif function_name == "calculate_reputation_score":
            return calculate_reputation_score(function_args["scan_results"])

    return message.get("content", "No analysis available.")
