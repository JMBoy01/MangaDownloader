from PIL import Image
import os
import asyncio
from pyppeteer import launch
import requests
from io import BytesIO

# Functie om afbeeldingen te laden en samen te voegen
def create_pdf_from_images(image_folder, output_pdf_path):
    # Lijst van afbeelding bestanden in de map ophalen en sorteren
    image_files = sorted(
        [file for file in os.listdir(image_folder) if file.endswith(('.png', '.jpg', '.jpeg'))]
    )

    # Controleer of er afbeeldingen zijn gevonden
    if not image_files:
        print("Geen afbeeldingen gevonden in de opgegeven map.")
        return

    # Eerste afbeelding openen en omzetten naar PDF formaat
    first_image_path = os.path.join(image_folder, image_files[0])
    first_image = Image.open(first_image_path).convert("RGB")

    # Volgende afbeeldingen openen en omzetten naar PDF formaat
    additional_images = [
        Image.open(os.path.join(image_folder, file)).convert("RGB") for file in image_files[1:]
    ]

    # Alle afbeeldingen samenvoegen tot een PDF
    if not output_pdf_path.endswith(".png"):
        output_pdf_path += ".pdf"
    
    output_pdf_path = "./PDF/" + output_pdf_path

    first_image.save(output_pdf_path, save_all=True, append_images=additional_images)
    print(f"PDF succesvol opgeslagen als: {output_pdf_path}")

def download_images(images, output_folder):
    # Maak een nieuwe map aan om de bestanden op te slaan
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Download de afbeeldingen
    for img_url in images:
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # Controleer of de aanvraag succesvol was

            img = Image.open(BytesIO(response.content))
            minSize = 350
            if img.size[0] < minSize or img.size[1] < minSize:
                print(f"Afbeelding {img_url} is kleiner dan {minSize}x{minSize} pixels en wordt overgeslagen.")
                continue  # Sla de afbeelding over

            # Haal de bestandsnaam uit de URL
            filename = os.path.join(output_folder, img_url.split("/")[-1])

            # Sla de afbeelding op
            with open(filename, "wb") as f:
                f.write(response.content)

            print(f"Afbeelding gedownload: {filename}")

        except requests.HTTPError as http_err:
            print(f"HTTP-fout opgetreden bij {img_url}: {http_err}")
        except Exception as err:
            print(f"Een fout opgetreden bij {img_url}: {err}")   

    print(f"Alle bestanden zijn opgeslagen in de map: {output_folder}")

def download_and_create_pdf(images, output_pdf_path):
    image_folder = "./Raw Images/" + output_pdf_path + " - images"

    download_images(images, image_folder)

    # PDF maken van afbeeldingen
    create_pdf_from_images(image_folder, output_pdf_path)

# def main():
    # # Voer de functie uit
    # url = 'https://manga4life.com/read-online/Hunter-X-Hunter-chapter-405.html'
    # image_folder = "HxH_Ch_405"
    # asyncio.get_event_loop().run_until_complete(download_images(url, image_folder))

    # # Map met afbeeldingen en de naam van de uitvoer PDF
    # output_pdf_path = 'Hunter X Hunter Chapter 405.pdf'

    # # PDF maken van afbeeldingen
    # create_pdf_from_images(image_folder, output_pdf_path)

# if __name__ == "__main__":
#     main()
