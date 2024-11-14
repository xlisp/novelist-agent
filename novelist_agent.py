import autogen
import requests
import json
import os

# OpenRouter API configuration
OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']

# Custom LLM configuration using OpenRouter
class OpenRouterLLM:
    def __init__(self, model="openai/gpt-4o-2024-08-06"):
        self.model = model
        
    def create_completion(self, messages):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}"
            },
            data=json.dumps({
                "model": self.model,
                "messages": messages,
                "top_p": 1,
                "temperature": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "repetition_penalty": 1,
                "top_k": 0,
            })
        )
        return response.json()

# Configure the LLM
llm = OpenRouterLLM()

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

# Custom function to create messages for OpenRouter API
def create_messages(system_message, user_message):
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

# Initialize the agents with custom configuration
class CustomAssistantAgent(autogen.AssistantAgent):
    def generate_reply(self, sender=None, messages=None):
        if messages is None:
            messages = self._oai_messages
            
        if not messages:
            return None
            
        system_message = self.system_message
        
        # Extract the last message content
        last_message = messages[-1]
        if isinstance(last_message, dict):
            last_message_content = last_message.get('content', '')
        else:
            last_message_content = str(last_message)
        
        api_messages = create_messages(system_message, last_message_content)
        response = llm.create_completion(api_messages)
        
        try:
            reply = response['choices'][0]['message']['content']
            return reply
        except KeyError:
            return "I apologize, but I encountered an error processing your request."

# Initialize the agents
story_planner = CustomAssistantAgent(
    name="story_planner",
    system_message=story_planner_config["system_message"]
)

character_developer = CustomAssistantAgent(
    name="character_developer",
    system_message=character_developer_config["system_message"]
)

narrative_writer = CustomAssistantAgent(
    name="narrative_writer",
    system_message=narrative_writer_config["system_message"]
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
