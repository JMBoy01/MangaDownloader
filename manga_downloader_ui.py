import manga_downloader
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import sys
import threading
from pyppeteer import launch
import asyncio

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        # Write message to the text widget
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Auto-scroll to the end

    def flush(self):
        # This is a no-op; needed for compatibility with file-like objects
        pass

class MangaDownloaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Manga Downloader")
        self.root.geometry("700x400")
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL Entry
        ttk.Label(main_frame, text="URL").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Vinkje voor meerdere hoofdstukken
        self.multiple_chapters_var = tk.BooleanVar()
        self.multiple_chapters_checkbox = ttk.Checkbutton(main_frame, text="Multiple Chapters", variable=self.multiple_chapters_var, command=self.toggle_chapter_entries)
        self.multiple_chapters_checkbox.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Hoofdstuk nummering
        self.chapter_start_label = ttk.Label(main_frame, text="Start:")
        self.chapter_start_entry = ttk.Entry(main_frame, width=10, validate="key")

        self.chapter_end_label = ttk.Label(main_frame, text="End:")
        self.chapter_end_entry = ttk.Entry(main_frame, width=10, validate="key")

        # Filename Entry
        ttk.Label(main_frame, text="Filename").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.filename_entry = ttk.Entry(main_frame, width=50)
        self.filename_entry.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Download Button
        self.download_button = ttk.Button(main_frame, text="Download", command=self.download)
        self.download_button.grid(row=5, column=0, sticky=tk.W)

        # Output Text Area
        ttk.Label(main_frame, text="Output").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, width=50, height=10)
        self.output_text.grid(row=7, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Redirect stdout to the text area
        sys.stdout = TextRedirector(self.output_text)

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

        # Verberg de hoofdstuk invoervelden standaard
        self.toggle_chapter_entries()

    def toggle_chapter_entries(self):
        if self.multiple_chapters_var.get():
            # Laat de invoervelden zien
            self.chapter_start_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
            self.chapter_start_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
            self.chapter_end_label.grid(row=0, column=2, sticky=tk.W, pady=(0, 5))
            self.chapter_end_entry.grid(row=1, column=2, sticky=tk.W, pady=(0, 10))

        else:
            # Verberg de invoervelden
            self.chapter_start_label.grid_forget()
            self.chapter_start_entry.grid_forget()
            self.chapter_end_label.grid_forget()
            self.chapter_end_entry.grid_forget()

    async def get_images(self, url):
        # Start de browser in headless modus
        browser = await launch(headless=True, executablePath='./chrome-win/chrome.exe')
        page = await browser.newPage()
        
        # Ga naar de URL
        await page.goto(url)

        # Verkrijg de afbeeldingen
        images = await page.querySelectorAllEval('img', 'imgs => imgs.map(img => img.src)')

        await browser.close()

        return images
    
    def download(self):
        # Get values from entries
        url = self.url_entry.get()
        filename = self.filename_entry.get()

        multiple = self.multiple_chapters_var.get()
        if multiple:
            start = int(self.chapter_start_entry.get())
            stop = int(self.chapter_end_entry.get())
            print("Start:", start, "| Stop:", stop)

            for i in range(start, stop+1):
                chapter_numb_in_url = url.split("-")[-1].split(".")[0]
                url_i = url.replace(chapter_numb_in_url, str(i))
                filename_i = filename + " " + str(i)

                print("chapter_numb_in_url:", chapter_numb_in_url, "url_i:", url_i, "filename_i:", filename_i)

                images = asyncio.run(self.get_images(url_i))

                threading.Thread(target=manga_downloader.download_and_create_pdf, args=(images, filename_i)).start()
        else:
            images = asyncio.run(self.get_images(url))

            download_thread = threading.Thread(target=manga_downloader.download_and_create_pdf, args=(images, filename))
            download_thread.start()

def main():
    root = tk.Tk()
    app = MangaDownloaderUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
