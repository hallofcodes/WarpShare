shared_path: str = "/"

def save_user_current_shared_path(path: str):
   shared_path = path

def retrieve_user_current_shared_path() -> str:
   return shared_path
