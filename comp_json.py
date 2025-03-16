import json
from collections.abc import Mapping

def load_json(file_path):
    """Charge un fichier JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def flatten_json(d, prefix=''):
    """Aplatit un JSON imbriqué en un dictionnaire à clé unique."""
    items = {}
    if isinstance(d, Mapping):
        for k, v in d.items():
            new_key = f"{prefix}.{k}" if prefix else k
            items.update(flatten_json(v, new_key))
    elif isinstance(d, list):
        for i, v in enumerate(d):
            items.update(flatten_json(v, f"{prefix}[{i}]") if isinstance(v, (Mapping, list)) else {f"{prefix}[{i}]": v})
    else:
        items[prefix] = d
    return items

def compare_json(dump_json, api_json):
    """Compare deux fichiers JSON et détecte les différences."""
    dump_flat = flatten_json(dump_json)
    api_flat = flatten_json(api_json)
    
    dump_keys = set(dump_flat.keys())
    api_keys = set(api_flat.keys())
    
    common_keys = dump_keys & api_keys
    missing_in_dump = api_keys - dump_keys
    missing_in_api = dump_keys - api_keys
    
    differences = []
    for key in common_keys:
        if dump_flat[key] != api_flat[key]:
            differences.append({
                "key": key,
                "dump_value": dump_flat[key],
                "api_value": api_flat[key],
                "type": "format_difference" if isinstance(dump_flat[key], str) and isinstance(api_flat[key], str) else "value_mismatch"
            })
    
    return {
        "summary": {
            "total_keys_dump": len(dump_keys),
            "total_keys_api": len(api_keys),
            "common_keys": len(common_keys),
            "missing_in_dump": len(missing_in_dump),
            "missing_in_api": len(missing_in_api)
        },
        "missing_keys_in_dump": list(missing_in_dump),
        "missing_keys_in_api": list(missing_in_api),
        "differences": differences
    }

def main(dump_file, api_file, output_file):
    dump_json = load_json(dump_file)
    api_json = load_json(api_file)
    result = compare_json(dump_json, api_json)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print(f"Comparaison terminée ! Résultat enregistré dans {output_file}")

# Exemple d'utilisation
if __name__ == "__main__":
    main("G1_2020.json", "G1_2025.json", "comparison_result.json")
