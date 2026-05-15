def find_folder_path(tree: dict, target_name: str, current_path: str = "") -> str | None:
    for key, value in tree.items():
        path = f"{current_path}/{key}" if current_path else key
        if key == target_name:
            return path
        if isinstance(value, dict) and "folders" in value:
            result = find_folder_path(value["folders"], target_name, path)
            if result:
                return result
    return None
