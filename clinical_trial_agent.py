# FIXED VERSION - Works with latest LangChain + Ollama
from langchain_ollama import OllamaLLM
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import pandas as pd

# Load your clinical trial data (adjust path if needed)
try:
    df = pd.read_csv('outputs/study1_final_dqi.csv')
except FileNotFoundError:
    print("Creating dummy data for testing...")
    df = pd.DataFrame({
        'Subject ID': ['PT001', 'PT002', 'PT003'],
        'Site ID': ['Site 05', 'Site 08', 'Site 12'],
        'Final_DQI': [65, 78, 45]
    })

# Define tools using @tool decorator (new syntax)
@tool
def query_high_risk_patients() -> str:
    """Find patients with DQI < 70"""
    high_risk = df[df['Final_DQI'] < 70]
    return f"Found {len(high_risk)} high-risk patients: {high_risk['Subject ID'].tolist()}"

@tool
def query_site_performance(site_id: str) -> str:
    """Get performance for a specific site. Input should be site ID like 'Site 05'."""
    site_data = df[df['Site ID'] == site_id]
    if len(site_data) == 0:
        return f"No data found for {site_id}"
    avg_dqi = site_data['Final_DQI'].mean()
    return f"Site {site_id}: Average DQI = {avg_dqi:.2f}, Patients: {len(site_data)}"

tools = [query_high_risk_patients, query_site_performance]

# Initialize Ollama LLM
llm = OllamaLLM(model="llama3.2")

# Pull the ReAct prompt from LangChain hub
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Test the agent!
if __name__ == "__main__":
    print("🤖 Testing Clinical Trial Agent...\n")
    
    # Test 1: Find high-risk patients
    result1 = agent_executor.invoke({"input": "Which patients need urgent attention?"})
    print("📊 RESULT 1:", result1['output'], "\n")
    
    # Test 2: Site performance
    result2 = agent_executor.invoke({"input": "What's the quality score for Site 05?"})
    print("📊 RESULT 2:", result2['output'])
