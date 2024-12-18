import google.generativeai as genai
import os
import sys
from typing import Dict, Optional

class CodeHelperAgent:
    """
    A smart coding assistant powered by Google's Gemini API.
    This agent can:
    1. Explain code in detail.
    2. Suggest improvements for better performance and readability.
    3. Help debug issues by identifying potential bugs and providing fixes.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the CodeHelperAgent with the given Gemini API key.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Define prompts for different coding tasks
        self.prompts = {
            'explain': (
                "You are a helpful coding assistant. Please explain the following code in detail, "
                "covering its purpose, functionality, and any important concepts used: "
            ),
            'improve': (
                "You are a helpful coding assistant. Please analyze the following code and suggest "
                "improvements for better efficiency, readability, and best practices: "
            ),
            'debug': (
                "You are a helpful coding assistant. Please help identify potential issues or bugs "
                "in the following code and suggest fixes: "
            )
        }
    
    async def explain_code(self, code: str) -> str:
        """
        Provide a detailed explanation of the given code.
        """
        try:
            prompt = self.prompts['explain'] + code
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while explaining the code: {e}"
    
    async def suggest_improvements(self, code: str) -> str:
        """
        Suggest improvements for the provided code.
        """
        try:
            prompt = self.prompts['improve'] + code
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while suggesting improvements: {e}"
    
    async def debug_code(self, code: str, error_message: Optional[str] = None) -> str:
        """
        Identify potential issues in the code and suggest fixes.
        Optionally, include an error message for context.
        """
        try:
            prompt = self.prompts['debug'] + code
            if error_message:
                prompt += f"\nError message received: {error_message}"
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while debugging the code: {e}"
    
    async def analyze_code(self, code: str) -> Dict[str, str]:
        """
        Perform a comprehensive analysis of the given code, including:
        - Explanation
        - Improvement suggestions
        - Debugging insights
        """
        return {
            'explanation': await self.explain_code(code),
            'improvements': await self.suggest_improvements(code),
            'debug_suggestions': await self.debug_code(code),
        }

async def main():
    """
    Main entry point for the Code Helper.
    Provides a menu for interacting with the agent.
    """
    # Prompt the user for their Gemini API key
    api_key = input("Please enter your Gemini API key: ")
    agent = CodeHelperAgent(api_key)
    
    while True:
        print("\n=== Code Helper Menu ===")
        print("1. Analyze code")
        print("2. Explain code")
        print("3. Suggest improvements")
        print("4. Debug code")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '5':
            print("\nGoodbye! See you next time!")
            break
        
        print("\nPaste your code below. Press Enter twice to finish input:")

        # Read multi-line input until an empty line is entered
        code_lines = []
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break  # Stop when an empty line is entered
            code_lines.append(line)

        # Combine the multi-line input into a single string
        code = " ".join(code_lines)

        # Process the user's choice
        if choice == '1':
            analysis = await agent.analyze_code(code)
            print("\n=== Code Explanation ===")
            print(analysis['explanation'])
            print("\n=== Suggested Improvements ===")
            print(analysis['improvements'])
            print("\n=== Debug Suggestions ===")
            print(analysis['debug_suggestions'])
        elif choice == '2':
            explanation = await agent.explain_code(code)
            print("\n=== Code Explanation ===")
            print(explanation)
        elif choice == '3':
            improvements = await agent.suggest_improvements(code)
            print("\n=== Suggested Improvements ===")
            print(improvements)
        elif choice == '4':
            error_msg = input("\nEnter an error message (if any) or press Enter to skip: ").strip()
            debug_suggestions = await agent.debug_code(code, error_message=error_msg or None)
            print("\n=== Debug Suggestions ===")
            print(debug_suggestions)
        else:
            print("\nInvalid choice. Please select a valid option.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
