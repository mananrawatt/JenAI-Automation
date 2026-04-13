import requests

def extract_error_lines(logs):
    error_keywords = [
        "ERROR",
        "Error",
        "FAIL",
        "Failed",
        "Exception",
        "Traceback",
        "denied",
        "unauthorized",
        "permission",
        "not found"
    ]

    lines = logs.split("\n")

    # Filter relevant lines
    filtered_lines = [
        line for line in lines
        if any(keyword in line for keyword in error_keywords)
    ]

    # Take last 5000 relevant lines (most important)
    return "\n".join(filtered_lines[-5000:])


def analyze_logs(logs):
    try:
        error_context = extract_error_lines(logs)

        # Fallback if nothing found
        if not error_context.strip():
            error_context = logs[-10000:]

        prompt = f"""
You are a senior DevOps engineer.

The Jenkins pipeline has FAILED.

Analyze the failure details below and provide:

1. Root cause of failure
2. Failed stage (if identifiable)
3. Simple explanation
4. Suggested fix

Logs:
{error_context}
"""

        response = requests.post(
            # "http://localhost:11434/api/generate",  when used locally without docker or k8s
            # "http://ollama:11434/api/generate",     when soing docker multi conatiner setup
              "http://ollama-service:11434/api/generate",           
            json={
                # "model": "llama3:8b",
                "model": "phi",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Ollama Error: {response.text}"

    except Exception as e:
        return f"AI Error: {str(e)}"






# import requests

# def extract_relevant_logs(logs):
#     # Focus on failure (last part of logs)
#     return logs[-400000:]

# def analyze_logs(logs):
#     try:
#         relevant_logs = extract_relevant_logs(logs)

#         prompt = f"""
# You are a senior DevOps engineer.

# The Jenkins pipeline has FAILED.

# Analyze ONLY the failure section of logs below and provide:

# 1. Exact root cause of failure
# 2. Which stage failed (e.g., Docker Build, Docker Push, Maven, etc.)
# 3. Simple explanation
# 4. Suggested fix

# Logs:
# {relevant_logs}
# """

#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "llama3",
#                 "prompt": prompt,
#                 "stream": False
#             }
#         )

#         if response.status_code == 200:
#             return response.json()["response"]
#         else:
#             return f"Ollama Error: {response.text}"

#     except Exception as e:
#         return f"AI Error: {str(e)}"