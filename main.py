import sys
from agent import AutonomousAgent

def print_welcome():
    print("="*50)
    print("Autonomous AI OS Agent - CLI Mode")
    print("="*50)
    print("Type 'exit' or 'quit' to close.")
    print("Type your task below and the agent will execute it.")
    print("-" * 50)

def main():
    agent = AutonomousAgent()
    print_welcome()
    
    while True:
        try:
            user_input = input("\nAgent> ")
            if user_input.lower() in ['exit', 'quit']:
                print("Shutting down agent...")
                break
            
            if not user_input.strip():
                continue
                
            agent.execute_task(user_input)
            
        except KeyboardInterrupt:
            print("\nShutting down agent...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

