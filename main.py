import sys
import os
import qrcode 
import logging.config
import argparse
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import validators

load_dotenv()

QR_DIR = os.getenv('QR_CODE_DIR', 'qr_codes')
FILL_COLOR = os.getenv('FILL_COLOR', 'black')
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

def create_dir(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        exit(1)

def is_valid_url(url: str):
    if validators.url(url):
        return True
    logging.error(f"Invalid URL provided: {url}")
    return False

def create_qr_code(data, path, fill, back):
    if not is_valid_url(data):
        return

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill, back_color=back)

        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f"QR code saved successfully at {path}")
    
    except Exception as e:
        logging.error(f"An error has occured while created QR code: {e}")

def main():
    parser = argparse.ArgumentParser(description='Generate a QR code from a URL')
    parser.add_argument('--url', help='Specify the URL to encode to QR', default='https://google.com')
    args = parser.parse_args()

    setup_logging()

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"

    qr_full_path = Path.cwd() / QR_DIR / qr_filename

    create_dir(Path.cwd() / QR_DIR)

    create_qr_code(args.url, qr_full_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()