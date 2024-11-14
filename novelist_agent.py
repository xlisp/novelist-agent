import autogen

# Configure the agents
config_list = [
    {
        "model": "gpt-4",
        "api_key": "your-api-key-here"
    }
]

# Create assistant configurations
story_planner_config = {
    "name": "StoryPlanner",
    "system_message": """You are a story planner specialized in game-related narratives.
    Your responsibilities:
    - Create story outlines and plot structures
    - Define key story beats and progression
    - Ensure the gaming elements are well-integrated into the plot
    - Coordinate with other agents to maintain story consistency"""
}

character_developer_config = {
    "name": "CharacterDeveloper",
    "system_message": """You are a character development specialist.
    Your responsibilities:
    - Create detailed character profiles
    - Define character relationships and dynamics
    - Ensure character motivations align with gaming elements
    - Design character arcs and development throughout the story"""
}

narrative_writer_config = {
    "name": "NarrativeWriter",
    "system_message": """You are a narrative writer focusing on game-related stories.
    Your responsibilities:
    - Write engaging prose and dialogue
    - Translate plot points into compelling scenes
    - Maintain consistent tone and style
    - Incorporate gaming terminology and concepts naturally"""
}

# Initialize the agents
story_planner = autogen.AssistantAgent(
    name="story_planner",
    system_message=story_planner_config["system_message"],
    llm_config={"config_list": config_list}
)

character_developer = autogen.AssistantAgent(
    name="character_developer",
    system_message=character_developer_config["system_message"],
    llm_config={"config_list": config_list}
)

narrative_writer = autogen.AssistantAgent(
    name="narrative_writer",
    system_message=narrative_writer_config["system_message"],
    llm_config={"config_list": config_list}
)

# Create human user agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10
)

# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, story_planner, character_developer, narrative_writer],
    messages=[],
    max_round=50
)

manager = autogen.GroupChatManager(groupchat=groupchat)

# Example usage
message = """Let's write a novel about a professional esports player's journey. 
Start by discussing the basic plot structure and main character."""

user_proxy.initiate_chat(manager, message=message)

