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
                # Remove interactive input if present (it should be already patched but just in case)
                if 'input("Enter a text description' in line:
                    new_source.append('user_prompt = "A photo of an astronaut riding a horse on mars." # Default prompt\n')
                    new_source.append('print(f"Using default prompt: {user_prompt}")\n')
                    cell_modified = True
                    modified = True
                # Replace cuda with cpu
                elif '.to("cuda")' in line:
                    new_source.append(line.replace('.to("cuda")', '.to("cpu")'))
                    cell_modified = True
                    modified = True
                elif "cuda" in line and "pipeline = pipeline.to" in line: # Handle other variations if any
                     new_source.append(line.replace('"cuda"', '"cpu"'))
                     cell_modified = True
                     modified = True
                # Replace float16 with float32 for CPU
                elif 'torch.float16' in line:
                    new_source.append(line.replace('torch.float16', 'torch.float32'))
                    cell_modified = True
                    modified = True
                else:
                    new_source.append(line)
            
            if cell_modified:
                cell["source"] = new_source

    if modified:
        with open(notebook_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=2)
        print(f"Successfully patched {notebook_path} for CPU")
    else:
        print(f"No changes needed or already patched for CPU.")

except Exception as e:
    print(f"Error patching notebook: {e}")
