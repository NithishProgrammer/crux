import os
from google import genai

def analyze_problem_and_solution(problem_statement , solution):
    # 1. Your VIP pass to talk to Google's servers
    api_key ="AQ.Ab8RN6IxP4rmo3-Tvc0263EIroMPc5gqFGjAVUNFCGtEedLoMQ"
    client = genai.Client(api_key=api_key)

    print("=== Problem & Solution Analyzer ===")
    
    # 2. Taking input from you (Just like Class 12 Python!)
    # 3. Wrapping your input into a neat instruction (Prompt) for the LLM
    prompt = f"""
    You are an expert project evaluator. 
    Evaluate this Problem Statement and Solution, and suggest improvements. Generate in 100 words and below

    Problem Statement: {problem_statement}
    Solution: {solution}
    """

    print("\nSending request to the LLM... Please wait...\n")

    # 4. Sending it through the API and getting the reply back
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,
    )


    txt = str(response.text)
    

    # 5. Printing the LLM's answer on your screen
    print("=== LLM Output ===")

    return txt


