import os
import sys
import argparse
import glob

def convert_folder(input_folder, overwrite=True):
    try:
        import comtypes.client
    except ImportError:
        print("Error: 'comtypes' library is required. Please install it using 'pip install comtypes'")
        sys.exit(1)

    if not os.path.isdir(input_folder):
        print(f"Error: The folder '{input_folder}' does not exist.")
        sys.exit(1)

    # Find all docx files in the folder
    search_pattern = os.path.join(input_folder, "*.docx")
    docx_files = glob.glob(search_pattern)

    # Filter out temporary word files (starting with ~$)
    docx_files = [f for f in docx_files if not os.path.basename(f).startswith("~$")]

    if not docx_files:
        print(f"No .docx files found in '{input_folder}'.")
        return

    print(f"Found {len(docx_files)} .docx files in '{input_folder}'.")

    word = None
    try:
        # Initialize Word Application
        # This requires Microsoft Word to be installed on the Windows machine
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        
        for docx_file in docx_files:
            abs_docx_file = os.path.abspath(docx_file)
            abs_pdf_file = os.path.abspath(os.path.splitext(docx_file)[0] + ".pdf")
            
            # Check if PDF already exists
            if os.path.exists(abs_pdf_file) and not overwrite:
                print(f"Skipping '{os.path.basename(docx_file)}' - PDF already exists.")
                continue
                
            print(f"Converting: {os.path.basename(docx_file)} -> {os.path.basename(abs_pdf_file)}")
            doc = None
            try:
                # Open the document
                doc = word.Documents.Open(abs_docx_file)
                # 17 corresponds to wdFormatPDF in Word Interop
                doc.SaveAs(abs_pdf_file, FileFormat=17)
            except Exception as e:
                print(f"Failed to convert '{os.path.basename(docx_file)}': {e}")
            finally:
                if doc is not None:
                    doc.Close()
                    
    except Exception as e:
        print(f"Failed to initialize Word application: {e}")
        print("Make sure Microsoft Word is installed on this machine.")
    finally:
        if word is not None:
            word.Quit()

    print("Conversion complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert all DOCX files in a folder to PDF.")
    parser.add_argument("-i", "--input", required=True, help="Input folder containing DOCX files")
    parser.add_argument("--no-overwrite", action="store_true", help="Do not overwrite existing PDF files")
    
    args = parser.parse_args()
    
    # Overwrite by default, unless --no-overwrite is specified
    overwrite = not args.no_overwrite
    convert_folder(args.input, overwrite=overwrite)
