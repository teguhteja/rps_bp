import os
import subprocess
import argparse
from pathlib import Path

def load_config(config_file):
    config = {}
    if not os.path.exists(config_file):
        print(f"Error: {config_file} not found.")
        return config
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    config[parts[0].strip()] = parts[1].strip()
    return config

def run_script(script, args_list):
    command = ["uv", "run", "python", script] + args_list
    try:
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def process_docx(mode, config):
    if mode == 'rps':
        input_dir = config.get('input_rps')
        output_dir = config.get('output_rps')
        script = 'edit_rps.py'
        is_folder_output = False
    elif mode == 'kontrak':
        input_dir = config.get('input_kontrak')
        output_dir = config.get('output_kontrak')
        script = 'edit_konkul.py'
        is_folder_output = False
    elif mode == 'sap':
        input_dir = config.get('input_sap')
        output_dir = config.get('output_sap')
        script = 'edit_sap.py'
        is_folder_output = True
    else:
        return

    if not input_dir or not output_dir:
        print(f"Error: Konfigurasi untuk {mode} tidak ditemukan di generate.conf")
        return

    if not os.path.isdir(input_dir):
        print(f"Error: Folder input {input_dir} tidak ditemukan untuk {mode}.")
        return

    print(f"\n=== Memulai proses DOCX untuk {mode.upper()} ===")
    
    success_count = 0
    fail_count = 0

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                input_file = os.path.join(root, file)
                rel_path = os.path.relpath(root, input_dir)
                
                if rel_path == '.':
                    current_out_dir = output_dir
                else:
                    current_out_dir = os.path.join(output_dir, rel_path)
                
                os.makedirs(current_out_dir, exist_ok=True)
                
                args_list = ["-i", input_file]
                if is_folder_output:
                    # Khusus SAP output target foldernya
                    args_list.extend(["-o", current_out_dir])
                else:
                    # RPS dan Kontrak output berupa nama file target
                    stem = Path(file).stem
                    if mode == 'kontrak':
                        out_file = os.path.join(current_out_dir, f"{stem}_kontrak.docx")
                    else:
                        out_file = os.path.join(current_out_dir, f"{stem}.docx")
                    args_list.extend(["-o", out_file])
                
                print(f"Memproses: {file}")
                success, output = run_script(script, args_list)
                if success:
                    print(f"✅ Berhasil: {file}")
                    success_count += 1
                else:
                    print(f"❌ Gagal memproses {file}")
                    print(f"   Error: {output.strip() if output else 'Unknown error'}")
                    fail_count += 1
    
    print(f"=== Ringkasan DOCX {mode.upper()} ===")
    print(f"Total berhasil : {success_count}")
    print(f"Total gagal    : {fail_count}\n")


def process_pdf(mode, config):
    target = mode.split('-')[1] # rps, sap, atau kontrak
    output_dir = config.get(f'output_{target}')
    
    if not output_dir:
        print(f"Error: Konfigurasi untuk output {target} tidak ditemukan di generate.conf.")
        return
        
    if not os.path.isdir(output_dir):
        print(f"Error: Folder output {output_dir} tidak ditemukan. Jalankan generate DOCX terlebih dahulu.")
        return
        
    print(f"\n=== Memulai proses konversi PDF untuk {target.upper()} ===")
    
    script = 'docx_to_pdf_folder.py'
    
    # Kumpulkan semua folder yang di dalamnya terdapat file .docx
    dirs_with_docx = set()
    for root, _, files in os.walk(output_dir):
        if any(f.endswith('.docx') for f in files):
            dirs_with_docx.add(root)
            
    if not dirs_with_docx:
        print(f"Tidak ada file DOCX ditemukan di {output_dir} untuk dikonversi.")
        return
        
    success_count = 0
    fail_count = 0
    for d in dirs_with_docx:
        print(f"Mengkonversi DOCX ke PDF di folder: {d}")
        success, output = run_script(script, ["-i", d])
        if success:
            print(f"✅ Selesai")
            success_count += 1
        else:
            print(f"❌ Gagal konversi di {d}")
            print(f"   Error: {output.strip() if output else 'Unknown error'}")
            fail_count += 1
            
    print(f"=== Ringkasan PDF {target.upper()} ===")
    print(f"Total folder berhasil dikonversi : {success_count}")
    print(f"Total folder gagal dikonversi    : {fail_count}\n")

def main():
    parser = argparse.ArgumentParser(description='Batch process JSON ke DOCX dan DOCX ke PDF.')
    parser.add_argument('mode', choices=['rps', 'sap', 'kontrak', 'pdf-rps', 'pdf-sap', 'pdf-kontrak', 'all'], 
                        help='Pilih mode yang ingin dijalankan')
    args = parser.parse_args()
    
    config = load_config('generate.conf')
    
    if args.mode == 'all':
        for m in ['rps', 'sap', 'kontrak']:
            process_docx(m, config)
        for m in ['rps', 'sap', 'kontrak']:
            process_pdf(f"pdf-{m}", config)
    elif args.mode.startswith('pdf-'):
        process_pdf(args.mode, config)
    else:
        process_docx(args.mode, config)

if __name__ == '__main__':
    main()
