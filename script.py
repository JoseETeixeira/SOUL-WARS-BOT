import pyautogui
import pytesseract
import mss  # For multi-monitor screenshot capture
from PIL import Image
import time

# Configure pytesseract to use the correct Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


faceByak = False

# Function to capture a screenshot of all screens
def capture_all_screens():
    with mss.mss() as sct:
        # Capture all monitors
        screenshot = sct.shot(mon=-1, output="temp_screenshot.png")
        return Image.open("temp_screenshot.png")

def click_on_text(target_text):
    screenshot = capture_all_screens()  # Capture all monitors

    # Use pytesseract to perform OCR on the screenshot
    ocr_result = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    # Iterate through detected text to find the target
    for i, text in enumerate(ocr_result['text']):
        if target_text.lower() in text.lower():
            # Get the bounding box of the detected text
            x, y, width, height = (ocr_result['left'][i], ocr_result['top'][i],
                                   ocr_result['width'][i], ocr_result['height'][i])

            # Check if the detected box has valid dimensions
            if width > 0 and height > 0:
                # Calculate the center of the bounding box
                center_x = x + width // 2
                center_y = y + height // 2

                # Optional: Add an offset to fine-tune the click position
                offset_y = height // 2  # Adjust this if necessary
                center_y += offset_y

                # Move the mouse to the center of the text and click
                pyautogui.moveTo(center_x, center_y, duration=0.2)
                pyautogui.click()
                print(f"Clicked on '{target_text}' at ({center_x}, {center_y})")
                return True

    print(f"Text '{target_text}' not found on the screen.")
    return False


# Function to find an image on the screen and click on it within a specific region
def click_on_image(image_path, region=None,confidence=0.4):
    try:
        # Capture all screens
        screenshot = capture_all_screens()

        if region:
            # Crop to the specified region
            screenshot = screenshot.crop(region)

        # Locate the image on the captured screenshot
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
        if location:
            # Get the center of the located image
            center_x, center_y = pyautogui.center(location)
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            pyautogui.click()
            print(f"Clicked on image '{image_path}' at ({center_x}, {center_y})")
            return True
        print(f"Image '{image_path}' not found in the specified region.")
        return False
    except Exception as e:
        print(f"Image not found {e}")
        return False
    
def locate_image(image_path, region=None,confidence=0.4):
    try:
        # Capture all screens
        screenshot = capture_all_screens()

        if region:
            # Crop to the specified region
            screenshot = screenshot.crop(region)

        # Locate the image on the captured screenshot
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
        if location:
            return True
        print(f"Image '{image_path}' not found in the specified region.")
        return False
    except Exception as e:
        return False
    
def handle_event(event_name, open_image, event_image):
    print(f"Checking if {event_name} is open.")
    is_open = locate_image(open_image, confidence=0.9)
    if is_open:
        print(f"{event_name} is open")
        events = click_on_image(__file__.replace("script.py", "Events.png"), confidence=0.6)
        if events:
            print(f"Clicked on Events for {event_name}")
            time.sleep(1)
            event = click_on_image(event_image, confidence=0.8)
            if event:
                print(f"Clicked on {event_name}")
                print("Waiting for 5 minutes before continuing...")
                time.sleep(300)  # Wait for 5 minutes
                return True
            else:
                print(f"{event_name} not found")
        else:
            print("Events not found")
    else:
        print(f"{event_name} not open")
    return False

def handle_event_started(event_name, started_image):
    hasEventStarted = locate_image(started_image,region=None,confidence=0.8)
    if hasEventStarted:
        print(f"{event_name} has started")
        return True
        
    else:
        print(f"{event_name} has not started")
        return False
    
def handle_event_ended(event_name, ended_image):
    hasEventEnded= locate_image(ended_image,region=None,confidence=0.5)
    if hasEventEnded:
        print(f"{event_name} has ended")
        return True
        
    else:
        print(f"{event_name} has not ended")
        return False



def doRoutine():
    load = click_on_image(__file__.replace("script.py", "Load.png"))
    if load:
        print("Character loaded")
    else:
        print("Failed to load. Text not found.")

    time.sleep(5)

    if handle_event("Byakuya", __file__.replace("script.py", "ByakOpen.png"), __file__.replace("script.py", "Byak.png")):
        time.sleep(5)
        if handle_event_started("Byakuya", __file__.replace("script.py", "ByakStarted.png")):
            return
        
    if handle_event("CTF", __file__.replace("script.py", "CTFOpen.png"), __file__.replace("script.py", "CTF.png")):
        time.sleep(5)
        if handle_event_started("CTF", __file__.replace("script.py", "CTFStarted.png")):
            if suicide():
                return
            else:
                time.sleep(5)
                suicide()
                return

    if handle_event("TDM", __file__.replace("script.py", "TDMOpen.png"), __file__.replace("script.py", "TDM.png")):
        time.sleep(5)
        if handle_event_started("TDM", __file__.replace("script.py", "TDMStarted.png")):
            if suicide():
                suicide()
                suicide()
                return
            else:
                suicide()
                suicide()
                suicide()
                return
    if  handle_event("KOTH", __file__.replace("script.py", "KOTHOpen.png"), __file__.replace("script.py", "KOTH.png")):
        if handle_event_started("KOTH", __file__.replace("script.py", "KOTHStarted.png")):
            if suicide():
                return
            else:
                time.sleep(5)
                suicide()
                return
    

def suicide():
    commands = click_on_image(__file__.replace("script.py", "Commands.png"),region=None,confidence=0.6)
    if commands:
        print("Clicked on commands")
        time.sleep(2)
        suicide = click_on_image(__file__.replace("script.py", "Suicide.png"),region=None,confidence=0.6)
        if suicide:
            print("Clicked on Suicide")
            return True
        else:
            print("Suicide not found")
            return False
    else:
        print("Commands not found")
        return False


if __name__ == "__main__":
    while True:
        # Locate and click the language selection image
        language = click_on_image(__file__.replace("script.py", "Image.png"),region=None,confidence=0.6)
        if language:
            time.sleep(5)  # Wait for the popup to appear
            # Locate and click the "X" button in the popup
            pyautogui.hotkey("alt", "f4")
            print("Closed the popup using Alt+F4")
            doRoutine()
        else:
            print("Language not found")
            doRoutine()

        # Wait for 10 seconds before the next iteration
        time.sleep(10)
