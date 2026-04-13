import os
import subprocess
import argparse
from pathlib import Path

def process_folder(input_folder, output_folder=None, template=None):
    """
    Menjalankan edit_rps.py untuk semua file JSON dalam folder input.
    """
    # Pastikan folder input ada
    if not os.path.isdir(input_folder):
        print(f"Error: Folder input '{input_folder}' tidak ditemukan.")
        return

    # Buat folder output jika dispesifikasikan dan belum ada
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    # Ambil semua file .json di folder tersebut
    json_files = list(Path(input_folder).glob('*.json'))
    
    if not json_files:
        print(f"Tidak ditemukan file .json di dalam folder '{input_folder}'.")
        return

    print(f"Menemukan {len(json_files)} file JSON. Memulai proses generate...\n")

    berhasil = 0
    gagal = 0

    for json_file in json_files:
        print(f"Memproses: {json_file.name}...")
        
        # Siapkan perintah untuk dijalankan
        command = ["uv", "run", "python", "edit_rps.py", "-i", str(json_file)]
        
        # Tambahkan output folder spesifik jika diberikan
        if output_folder:
            output_file = os.path.join(output_folder, f"{json_file.stem}.docx")
            command.extend(["-o", output_file])
            
        if template:
            command.extend(["--template", template])
            
        try:
            # Jalankan perintah
            result = subprocess.run(
                command, 
                check=True, 
                capture_output=True, 
                text=True
            )
            print(f"✅ Selesai: {json_file.name}")
            berhasil += 1
            
            # Print output dari script edit_rps.py jika ada
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    print(f"   > {line}")
                    
        except subprocess.CalledProcessError as e:
            print(f"❌ Gagal memproses {json_file.name}")
            print(f"   Error: {e.stderr.strip() if e.stderr else 'Unknown error'}")
            gagal += 1
            
        print("-" * 50)

    print("\n=== Ringkasan ===")
    print(f"Total file diproses : {len(json_files)}")
    print(f"Berhasil          : {berhasil}")
    print(f"Gagal             : {gagal}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch process RPS JSON files.')
    parser.add_argument('-f', '--folder', default='input', help='Folder berisi file JSON (default: "input")')
    parser.add_argument('-o', '--output', help='Folder tujuan penyimpanan file DOCX (opsional, akan dibuat jika belum ada)')
    parser.add_argument('-t', '--template', help='Template DOCX (opsional, default diatur oleh edit_rps.py)')
    
    args = parser.parse_args()
    
    process_folder(args.folder, args.output, args.template)