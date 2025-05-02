import pyperclip
import time
import keyboard
import threading
import queue
from tkinter import *
from tkinter import ttk
from summarization_service import summarize_text_openrouter
from notion_integration import (
    create_notion_page,
    get_database_pages,
    append_to_page
)
import os
from dotenv import load_dotenv

import threading
import time
import os
import sys

try:
    from pystray import MenuItem as item
    import pystray
    from PIL import Image, ImageDraw
    HAS_PYSTRAY = True
except ImportError:
    HAS_PYSTRAY = False
    print("pystray not available, running without system tray")

tray_icon = None

def create_tray_icon():
    """Create and run system tray icon in a separate thread"""
    global tray_icon
    
    img = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (63, 63)], outline=(0, 0, 255), width=3)
    draw.line([(10, 10), (54, 54)], fill=(0, 0, 255), width=3)
    draw.line([(54, 10), (10, 54)], fill=(0, 0, 255), width=3)
    
    def on_quit(icon):
        print("Quitting application from system tray")
        icon.stop()
        os._exit(0)  
    
    menu = (item('Quit', on_quit),)
    tray_icon = pystray.Icon("GlobalIntegrator", img, "Global Integrator", menu)
    
    try:
        print("Starting system tray icon")
        tray_icon.run()
    except Exception as e:
        print(f"Error running system tray icon: {e}")

def start_system_tray():
    if HAS_PYSTRAY:
        tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
        tray_thread.start()
        print("System tray thread started")
    else:
        print("System tray not available (pystray not installed)")

load_dotenv()
notion_token = os.getenv('NOTION_API_TOKEN')
database_id = os.getenv('NOTION_DATABASE_ID')

class GlobalIntegrator:
    def __init__(self):
        self.selected_text = ""
        self.database_id = database_id  
        self.token = notion_token  
        self.action_queue = queue.Queue()

    def capture_text(self):
        keyboard.send('ctrl+c')
        time.sleep(0.2)
        self.selected_text = pyperclip.paste()
        self.action_queue.put('show_popup')

    def show_notion_selection(self):
        popup = Toplevel()
        popup.title("Notion Integration")
        popup.geometry("400x250")
        popup.resizable(False, False)

        pages = get_database_pages(self.token, self.database_id)
        page_options = [name for name, _ in pages]
        page_dict = {name: page_id for name, page_id in pages}

        Label(popup, text="📄 Select existing page to append:", font=("Arial", 11)).pack(pady=(15, 5))
        page_combo = ttk.Combobox(popup, values=page_options, state="readonly")
        page_combo.set("Select a page (optional)")
        page_combo.pack(pady=5, ipadx=5)

        Label(popup, text="or ✨ create a new page:", font=("Arial", 11)).pack(pady=(20, 5))
        new_page_entry = Entry(popup, font=("Arial", 10))
        placeholder_text = "Enter new page name..."
        new_page_entry.insert(0, placeholder_text)
        new_page_entry.pack(pady=5, ipadx=5, ipady=2)

        def on_entry_click(event):
            if new_page_entry.get() == placeholder_text:
                new_page_entry.delete(0, "end")
                new_page_entry.config(fg="black")

        new_page_entry.bind("<FocusIn>", on_entry_click)

        def process_selection():
            selected_page_name = page_combo.get()
            new_page_name = new_page_entry.get().strip()
            popup.destroy()

            if new_page_name and new_page_name != placeholder_text:
                threading.Thread(target=self.process_new_page, args=(new_page_name,)).start()
            elif selected_page_name and selected_page_name in page_dict:
                page_id = page_dict[selected_page_name]
                threading.Thread(target=self.process_append_page, args=(page_id,)).start()
            else:
                print("⚠️ No valid selection made.")

        Button(popup, text="Submit", command=process_selection, font=("Arial", 11), bg="#4CAF50", fg="white").pack(pady=20, ipadx=10, ipady=3)

    def process_new_page(self, page_name):
        if not self.selected_text.strip():
            print("No text captured")
            return

        summary = summarize_text_openrouter(self.selected_text)
        if not summary:
            print("Summarization failed")
            return

        response = create_notion_page(
            token=self.token,
            database_id=self.database_id,
            title=page_name,
            content=summary
        )
        print("✅ Created new page. Notion response:", response)
        self.action_queue.put('show_success')

    def process_append_page(self, page_id):
        if not self.selected_text.strip():
            print("No text captured")
            return

        summary = summarize_text_openrouter(self.selected_text)
        if not summary:
            print("Summarization failed")
            return

        response = append_to_page(
            token=self.token,
            page_id=page_id,
            content=summary
        )
        print("✅ Appended to existing page. Notion response:", response)
        self.action_queue.put('show_success')

    def show_success_message(self):
        popup = Toplevel()
        popup.title("Success ✅")
        popup.geometry("300x150")
        popup.resizable(False, False)

        Label(popup, text="✅ Summary uploaded successfully!", font=("Arial", 12)).pack(padx=20, pady=30)
        Button(popup, text="OK", command=popup.destroy, font=("Arial", 11), bg="#4CAF50", fg="white").pack(pady=10, ipadx=10, ipady=3)

    def setup_hotkey(self):
        threading.Thread(target=lambda: keyboard.add_hotkey('ctrl+q', self.capture_text), daemon=True).start()

    def run(self):
        start_system_tray()
        root = Tk()
        root.withdraw()
        self.setup_hotkey()
        print("Hotkey listener active (Ctrl+Q)")

        def check_queue():
            while not self.action_queue.empty():
                action = self.action_queue.get()
                if action == 'show_popup':
                    self.show_notion_selection()
                elif action == 'show_success':
                    self.show_success_message()
            root.after(100, check_queue)

        check_queue()
        root.mainloop()


if __name__ == "__main__":
    integrator = GlobalIntegrator()
    integrator.run()
