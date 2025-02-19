from agent_utilities import initialize_env, AgentManager
from config_manager import ConfigManager
from final_main_without_oops import personal_agent

# Initialize environment variables
initialize_env()

# Create an instance of AgentManager
agent_manager = AgentManager()

# Create agents
github_agent = agent_manager.create_github_agent()
medium_agent = agent_manager.create_medium_agent()
general_agent = agent_manager.create_general_agent()
linkedin_agent = agent_manager.create_linkedin_agent()

# Create a personal agent combining multiple agents into a team
personal_agent = agent_manager.create_personal_agent()

# Run the personal agent
run_response = personal_agent.run("Provide in brief description about and engaging profile about Jiten Bhalavat. Start with a generic title, mention his Bachelor's and Master's Education. Highlight his skills in Python, Machine Learning, and AI. Discuss his role at Plutomen Technologies, his projects from Github, and then provide his Medium Blog posts. Conclude with his volunteer work and achievements. Keep it simple, professional, and engaging.")

# Print the response
print(run_response.content)
