from typing import Dict, Any, Callable
from os_controller import OSController

class ActionEngine:
    """Maps AI-generated intents/actions to actual OS Controller functions."""
    
    def __init__(self, os_controller: OSController):
        self.os = os_controller
        self.actions: Dict[str, Callable] = {
            "get_system_stats": self._action_get_system_stats,
            "list_processes": self._action_list_processes,
            "run_command": self._action_run_command,
            "click_ui": self._action_click_ui,
            "type_text": self._action_type_text,
            "press_key": self._action_press_key
        }
        
    def execute_action(self, action_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Executes the mapped action with given parameters."""
        if parameters is None:
            parameters = {}
            
        if action_name not in self.actions:
            return {"status": "error", "message": f"Action '{action_name}' not found."}
            
        try:
            result = self.actions[action_name](**parameters)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": f"Failed to execute action '{action_name}': {str(e)}"}
            
    # --- Action Implementations ---
    
    def _action_get_system_stats(self) -> Dict[str, Any]:
        return self.os.get_system_stats()
        
    def _action_list_processes(self, limit: int = 10) -> list:
        return self.os.list_running_processes(limit=limit)
        
    def _action_run_command(self, command: str) -> str:
        # Note: In a production system, this needs strict sandboxing
        return self.os.execute_command(command)
        
    def _action_click_ui(self, x: int, y: int) -> str:
        return self.os.click_at(x=x, y=y)
        
    def _action_type_text(self, text: str) -> str:
        return self.os.type_text(text=text)
        
    def _action_press_key(self, key: str) -> str:
        return self.os.press_key(key=key)

if __name__ == "__main__":
    # Test the action engine
    controller = OSController()
    engine = ActionEngine(controller)
    
    print(engine.execute_action("get_system_stats"))
    print(engine.execute_action("run_command", {"command": "echo Hello from Action Engine"}))
