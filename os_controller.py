import os
import subprocess
import psutil
import pyautogui
from typing import Dict, Any, List

class OSController:
    """Handles direct interactions with the Operating System."""
    
    def __init__(self):
        # We can configure safelists or permissions here later
        pass
        
    def get_system_stats(self) -> Dict[str, Any]:
        """Returns current CPU, Memory, and Disk usage."""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu,
            "memory_percent": memory.percent,
            "memory_used_gb": round(memory.used / (1024 ** 3), 2),
            "memory_total_gb": round(memory.total / (1024 ** 3), 2),
            "disk_percent": disk.percent
        }
        
    def list_running_processes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns a list of top running processes by memory usage."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        # Sort by memory usage
        processes = sorted(processes, key=lambda p: p['memory_percent'] or 0, reverse=True)
        return processes[:limit]
        
    def execute_command(self, command: str) -> str:
        """Executes a terminal command and returns the output."""
        try:
            # We use shell=True because we're on Windows and want access to builtins
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error executing command: {result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return "Command execution timed out."
        except Exception as e:
            return f"An exception occurred: {str(e)}"
            
    def get_screen_size(self):
        """Returns the primary monitor screen size."""
        return pyautogui.size()
        
    def click_at(self, x: int, y: int):
        """Simulates a mouse click at specific coordinates."""
        pyautogui.click(x=x, y=y)
        return f"Clicked at ({x}, {y})"
        
    def type_text(self, text: str, interval: float = 0.05):
        """Simulates typing text via keyboard."""
        pyautogui.write(text, interval=interval)
        return f"Typed text: {text}"
        
    def press_key(self, key: str):
        """Presses a specific keyboard key."""
        pyautogui.press(key)
        return f"Pressed key: {key}"

if __name__ == "__main__":
    controller = OSController()
    print("System Stats:", controller.get_system_stats())
    print("Top 3 Processes:", controller.list_running_processes(limit=3))
