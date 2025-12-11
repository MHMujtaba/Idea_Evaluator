EVALUATION_PROMPT = """
You are an AI feasibility evaluator. Analyze the following idea and return ONLY valid JSON.

Idea:
"{idea}"

Based on this idea and parameters:
Market Size: {market_size}
Team Skill: {team_skill}
Budget: {budget}
Timeline: {timeline}

Return JSON in this EXACT format:

{{
  "feasibility_score": "",
  "difficulty_score": "",
  "estimated_time": "",
  "estimated_cost": "",
  "potential_roi": "",
  "success_probability": "",
  "key_risks": [],
  "major_bottlenecks": [],
  "viability_summary": ""
}}

The values should look like this:

  "feasibility_score": (1-10),
  "difficulty_score": (1-10),
  "estimated_time": "string in days or weeks",
  "estimated_cost": "string cost range",
  "potential_roi": "string or number",
  "key_risks": ["list", "of", "risks"],
  "major_bottlenecks": ["list", "of", "bottlenecks"],
  "success_probability": "(%) number 0-100",
  "viability_summary": "short paragraph summary"

"""
