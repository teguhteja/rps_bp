import json
import glob
import re

# Dictionary mapping dari nuptk.md
NUPTK_MAP = {
    "Ida Bagus Teguh Teja Murti": "9234766667130303",
    "Made Edwin Wira Putra": "0547768669130333",
    "I Made Hendra Wijaya": "5138772673130293",
    "I Wayan Yudik Pradnyana": "4835771672130352",
    "Ni Putu Veny Narlianti": "0633771672230302",
    "I Wayan Septa Malan Vergantana": "0234772673130253",
    "I Gede Irvan Pramanta Andika": "6833771672130312",
    "Dody May Arfian": "6833771672130312",
    "I Kadek Krisna Angga Pamungkas": "7956775767130152",
    "Moch. Anw Ar Fery Rais": "3956752653130112",
    "Gede Riska Wiradarma": "8257772673130253",
    "Gusti Ayu Ovianti": "6945770671230272"
}

def clean_name(name):
    # Hilangkan gelar (S.Kom., M.Kom., dll)
    name = re.sub(r',.*$', '', name).strip()
    return name

def check_and_fix_nuptk():
    folders = ['input_3', 'input_4', 'input_5', 'input_6', 'input_7', 'input_8']
    
    total_files = 0
    fixed_files = 0
    errors = []

    for folder in folders:
        for filepath in glob.glob(f"{folder}/*.json"):
            total_files += 1
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if 'meta' in data and 'dosen_pengampu' in data['meta']:
                    dosen_full = data['meta']['dosen_pengampu']
                    dosen_clean = clean_name(dosen_full)
                    
                    # Cari NUPTK yang benar
                    correct_nuptk = None
                    for name_key, nuptk in NUPTK_MAP.items():
                        if name_key.lower() == dosen_clean.lower() or dosen_clean.lower() in name_key.lower():
                            correct_nuptk = nuptk
                            break
                    
                    if correct_nuptk:
                        current_nuptk = data['meta'].get('nuptk', '')
                        if current_nuptk != correct_nuptk:
                            print(f"Memperbaiki {filepath}:")
                            print(f"  Dosen: {dosen_full}")
                            print(f"  NUPTK lama: {current_nuptk}")
                            print(f"  NUPTK baru: {correct_nuptk}")
                            
                            data['meta']['nuptk'] = correct_nuptk
                            
                            with open(filepath, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            fixed_files += 1
                    else:
                        print(f"Warning: Tidak menemukan NUPTK untuk dosen '{dosen_clean}' di {filepath}")
            except Exception as e:
                errors.append(f"Error memproses {filepath}: {str(e)}")

    print("\n--- RINGKASAN ---")
    print(f"Total file JSON diperiksa: {total_files}")
    print(f"Total file JSON diperbaiki: {fixed_files}")
    if errors:
        print("Daftar Error:")
        for err in errors:
            print(f"  - {err}")

if __name__ == "__main__":
    check_and_fix_nuptk()
