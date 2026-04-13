import streamlit as st
# from jenkins_client import get_console_logs_from_url
from jenkins_client import get_console_logs_from_url, get_build_status
from ai_analyzer import analyze_logs

st.set_page_config(page_title="Jenkins-Pipeline Failure AI Analyzer", layout="wide")

st.title("🤖 Jenkins-Pipeline Failure  AI Failure Analyzer")

build_url = st.text_input("Paste Jenkins Build URL")
# # 🔥 Fix for Docker networking
# if build_url:
#     build_url = build_url.replace("localhost", "host.docker.internal")

# 🔥 Fix for Docker networking (only if localhost present)
if build_url and "localhost" in build_url:
    build_url = build_url.replace("localhost", "host.docker.internal")

username = st.text_input("Jenkins Username")
api_token = st.text_input("Jenkins API Token", type="password")

if st.button("Analyze Failure"):

    if not build_url or not username or not api_token:
        st.warning("⚠️ Please fill all fields")
    else:
        # Step 1: Check build status
        with st.spinner("🔍 Checking build status..."):
            status = get_build_status(build_url, username, api_token)

        if status == "SUCCESS":
            st.success("✅ Pipeline executed successfully. No failures detected.")
        
        elif status == "FAILURE":
            st.error("❌ Pipeline failed. Analyzing logs...")

            # Fetch logs
            with st.spinner("📡 Fetching logs..."):
                logs = get_console_logs_from_url(
                    build_url,
                    username,
                    api_token
                )

            if logs.startswith("Error"):
                st.error(logs)
            else:
                st.subheader("📄 Log Preview")
                st.code(logs[-1000:])  # show last part

                # AI Analysis
                with st.spinner("🧠 Analyzing with AI..."):
                    result = analyze_logs(logs)

                st.subheader("🔍 AI Analysis")
                st.write(result)

        else:
            st.warning(f"⚠️ Unknown build status: {status}")