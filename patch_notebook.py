import json

notebook_path = "days6.ipynb"

try:
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    modified = False
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            new_source = []
            cell_modified = False
            for line in source:
                if 'input("Enter a text description' in line:
                    new_source.append('user_prompt = "A photo of an astronaut riding a horse on mars." # Default prompt\n')
                    new_source.append('print(f"Using default prompt: {user_prompt}")\n')
                    cell_modified = True
                    modified = True
                else:
                    new_source.append(line)
            
            if cell_modified:
                cell["source"] = new_source

    if modified:
        with open(notebook_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=2)
        print(f"Successfully patched {notebook_path}")
    else:
        print(f"No interactive input found in {notebook_path} or already patched.")

except Exception as e:
    print(f"Error patching notebook: {e}")
