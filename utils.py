import os
def get_order_state(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            state = file.read().strip()
            if state:
                return int(state)
            return 0
    else:
        return 0

def set_order_state(file_path, state):
    with open(file_path, "w") as file:
        file.write(str(state))