import json
import copy

# Load the original notebook (assuming it's the base state before my CPU patches, 
# but if I patched it in place, I might need to revert or be careful. 
# I modified 'days6.ipynb' in place with the patch script. 
# So I should start from that or 'patch_notebook.py' logic but aiming for Colab.)

input_path = "days6.ipynb"
output_path = "days6_colab.ipynb"

try:
    with open(input_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # 1. Add !pip install cell at the beginning
    install_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Install required libraries\n",
            "!pip install torch diffusers transformers accelerate scipy safetensors\n"
        ]
    }
    nb["cells"].insert(0, install_cell)

    # 2. Modify cells to ensure GPU usage and restore/improve interactivity
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            new_source = []
            for line in source:
                # Revert CPU patch if present, enforce CUDA/GPU
                if '.to("cpu")' in line:
                    new_source.append(line.replace('.to("cpu")', '.to("cuda")'))
                elif 'torch.float32' in line:
                    new_source.append(line.replace('torch.float32', 'torch.float16'))
                
                # Check for the prompt line
                elif 'user_prompt =' in line and 'A photo of' in line:
                    # Switch to Colab form for better UX
                    new_source.append('user_prompt = "A photo of an astronaut riding a horse on mars." #@param {type:"string"}\n')
                elif 'input(' in line:
                     # If we see original input, replace with Colab param too
                    new_source.append('user_prompt = "A photo of an astronaut riding a horse on mars." #@param {type:"string"}\n')
                else:
                    new_source.append(line)
            
            cell["source"] = new_source

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    
    print(f"Created {output_path} for Google Colab.")

except Exception as e:
    print(f"Error creating Colab notebook: {e}")
