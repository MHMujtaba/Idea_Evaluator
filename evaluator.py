from google import genai
import json
from prompts import EVALUATION_PROMPT

def load_gemini(api_key: str):
    client = genai.Client(api_key=api_key)  
    return client

def evaluate_idea(client, idea, market_size, team_skill, budget, timeline):
    
    prompt = EVALUATION_PROMPT.format(
        idea=idea,
        market_size=market_size,
        team_skill=team_skill,
        budget=budget,
        timeline=timeline
    )

    response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt,
    )
    
    try:
        temp = response.text.replace("```","")
        temp = temp.replace("json","")    
        data = json.loads(temp)
    except:
        data = {"error": "Invalid JSON returned by model.", "raw": response.text}

    return data
