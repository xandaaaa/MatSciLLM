from mp_api.client import MPRester
import subprocess
import json
from dotenv import load_dotenv
import os

# Accesses Materials Project (MP) using API KEY

load_dotenv()
API_KEY = os.getenv("API_KEY")

def llm_extract_element(mat_name, model_name="llama3"):
    prompt_str = f"""
    Return ONLY a flat JSON array of chemical element symbols for the following material.
    - Format: ["O"], all symbols must be strings.
    - Do NOT include null, empty values, explanations, headings, or extra text.
    - Return an empty array [] if no elements can be determined.

    Examples:
    Material: Hydrogen
    Answer: ["H"]

    Material: Tungsten
    Answer: ["O"]

    Please give me the answer for the following material {mat_name}.

    """

    # Call LLM
    result = subprocess.run(
        ["ollama", "run", model_name, prompt_str],
        capture_output=True,    
        text=True
    )
    output = result.stdout.strip()
    print(output)

    # parse JSON
    try:
        data = json.loads(output)

        if isinstance(data, list):
            # Return if material is a string and in alphabet
            return [mat for mat in data if isinstance(mat, str) and mat.isalpha()]
    except json.JSONDecodeError:
        pass

    raise ValueError(f"Could not parse LLM output: {output}")

# Fetch composition of a material
def get_all_compositions(mat_name):

    element = llm_extract_element(mat_name)

    if element == []:
        return "Failed: no element could be extracted. (invalid element)"
    
    with MPRester(API_KEY) as mpr:
        results = mpr.materials.summary.search(
            elements=element,               
            is_stable=True,     # no metastable and unstable materials
            fields=["material_id", "formula_pretty", "elements"], 
            chunk_size=100
        )

        seen_comp = set()
        unique_mats = []

        for r in results:
            composition = tuple(sorted(r.elements))  # Sort so unique elements can be picked out
            if composition not in seen_comp:
                seen_comp.add(composition)
                unique_mats.append(r)

        if not unique_mats:
            return f"No compositions found with {element}."

        # Build output string
        lines = [f"ID: {mat.material_id} | Material: {mat.formula_pretty}" for mat in unique_mats]
        lines.append(f"\nTotal unique compositions with {element}: {len(unique_mats)}")
        return "\n".join(lines)


# if __name__ == "__main__":
#     mat_name = input("Enter material name: ")
#     get_all_compositions(mat_name)
#     #print(llm_extract_element(mat_name))