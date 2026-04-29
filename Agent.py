import json
from os_controller import OSController
from action_engine import ActionEngine
from task_planner import TaskPlanner

class AutonomousAgent:
    """Orchestrates the AI planning and system execution."""
    
    def __init__(self):
        self.os_controller = OSController()
        self.action_engine = ActionEngine(self.os_controller)
        self.planner = TaskPlanner()
        self.history = []
        
    def execute_task(self, user_request: str):
        """Processes a user request from start to finish."""
        print(f"Task Received: {user_request}")
        
        # 1. Plan the task
        print("Planning actions...")
        plan = self.planner.plan_task(user_request)
        
        print("Execution Plan:")
        print(json.dumps(plan, indent=2))
        
        results = []
        
        # 2. Execute actions
        for step in plan:
            action = step.get("action")
            
            if action == "error":
                print(f"Planning Error: {step.get('message')}")
                break
                
            parameters = step.get("parameters", {})
            print(f"\nExecuting: {action} with args {parameters}")
            
            result = self.action_engine.execute_action(action, parameters)
            
            # Log result
            print(f"Result: {result['status']}")
            if result['status'] == 'success':
                # Don't print massive outputs to console entirely
                data_str = str(result.get('data', ''))
                print(f"Data: {data_str[:200]}..." if len(data_str) > 200 else f"Data: {data_str}")
            else:
                print(f"Message: {result.get('message')}")
                
            results.append({
                "action": action,
                "parameters": parameters,
                "result": result
            })
            
        self.history.append({
            "request": user_request,
            "plan": plan,
            "results": results
        })
        
        return results

if __name__ == "__main__":
    agent = AutonomousAgent()
    agent.execute_task("Give me a quick system health check.")
