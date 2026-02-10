import json
import os
from utils.helpers import resource_path

# We'll use a local data file but we could shift this to AppData if we wanted
DATA_FILE = resource_path("data/tasks_data.json")

class TaskData:
    def __init__(self):
        self.tasks = []
        self.ensure_data_dir()
        self.load_data()

    def ensure_data_dir(self):
        data_dir = os.path.dirname(DATA_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)

    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
        except Exception as e:
            print(f"加载数据失败: {e}")
            self.tasks = []

    def save_data(self):
        try:
            data = {'tasks': self.tasks}
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def add_task(self, content, weekdays, time_str):
        # Generate a unique ID based on max existing ID
        max_id = max([t['id'] for t in self.tasks], default=0)
        task = {
            'id': max_id + 1,
            'content': content,
            'weekdays': weekdays,
            'time': time_str,
            'enabled': True,
            'last_triggered': None
        }
        self.tasks.append(task)
        self.save_data()
        return task

    def remove_task(self, task_id):
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_data()

    def get_active_tasks(self):
        return [t for t in self.tasks if t['enabled']]
