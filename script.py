import pyautogui
import pytesseract
import mss  # For multi-monitor screenshot capture
from PIL import Image
import time

# Configure pytesseract to use the correct Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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

def doRoutine():
    load = click_on_image(__file__.replace("script.py", "Load.png"))
    if load:
        print("Character loaded")
    else:
        print("Failed to load. Text not found.")
    
    time.sleep(5)
    isByakOpen = locate_image(__file__.replace("script.py", "ByakOpen.png"),region=None,confidence=0.9)
    if isByakOpen:
        print("Byak is open")
        events = click_on_image(__file__.replace("script.py", "Events.png"),region=None,confidence=0.6)
        if events:
            print("Clicked on Events")
            time.sleep(1)
            byak = click_on_image(__file__.replace("script.py", "Byak.png"),region=None,confidence=0.8)
            if byak:
                print("Clicked on Byak")
            else:
                print("Byak not found")
        else:
            print("Events not found")
    else:
        print("Byak not open")
    isCTFOpen = locate_image(__file__.replace("script.py", "CTFOpen.png"),region=None,confidence=0.8)
    if isCTFOpen:
        print("CTF is open")
        events = click_on_image(__file__.replace("script.py", "Events.png"),region=None,confidence=0.6)
        if events:
            print("Clicked on Events")
            time.sleep(2)
            ctf = click_on_image(__file__.replace("script.py", "CTF.png"),region=None,confidence=0.8)
            if ctf:
                print("Clicked on CTF")
            else:
                print("CTF not found")
        else:
            print("Events not found")
    else:
        print("CTF not open")
    hasCTFStarted = locate_image(__file__.replace("script.py", "CTFStarted.png"),region=None,confidence=0.8)
    if hasCTFStarted:
        print("CTF has started")
        commands = click_on_image(__file__.replace("script.py", "Commands.png"),region=None,confidence=0.6)
        if commands:
            print("Clicked on commands")
            time.sleep(2)
            suicide = click_on_image(__file__.replace("script.py", "Suicide.png"),region=None,confidence=0.6)
            if suicide:
                print("Clicked on Suicide")
            else:
                print("Suicide not found")
        else:
            print("Events not found")
    else:
        print("CTF not started")

    isTDMOpen = locate_image(__file__.replace("script.py", "TDMOpen.png"),region=None,confidence=0.8)
    if isTDMOpen:
        print("TDM is open")
        events = click_on_image(__file__.replace("script.py", "Events.png"),region=None,confidence=0.6)
        if events:
            print("Clicked on Events")
            time.sleep(2)
            tdm = click_on_image(__file__.replace("script.py", "TDM.png"),region=None,confidence=0.8)
            if tdm:
                print("Clicked on TDM")
            else:
                print("TDM not found")
        else:
            print("Events not found")
    else:
        print("TDM not open")

    hasTDMStarted = locate_image(__file__.replace("script.py", "TDMStarted.png"),region=None,confidence=0.8)
    if hasTDMStarted:
        print("TDM has started")
        hasSuicidedBefore = locate_image(__file__.replace("script.py", "LivesLeft.png"),region=None,confidence=0.8)
        if not hasSuicidedBefore:
            commands = click_on_image(__file__.replace("script.py", "Commands.png"),region=None,confidence=0.6)
            if commands:
                print("Clicked on commands")
                time.sleep(2)
                suicide = click_on_image(__file__.replace("script.py", "Suicide.png"),region=None,confidence=0.6)
                if suicide:
                    print("Clicked on Suicide")
                else:
                    print("Suicide not found")
            else:
                print("Events not found")
        else:
            print("Already suicided")
    else:
        print("TDM not started")

    isKOTHOpen = locate_image(__file__.replace("script.py", "KOTHOpen.png"),region=None,confidence=0.8)
    if isKOTHOpen:
        print("KOTH is open")
        events = click_on_image(__file__.replace("script.py", "Events.png"),region=None,confidence=0.6)
        if events:
            print("Clicked on Events")
            time.sleep(2)
            tdm = click_on_image(__file__.replace("script.py", "KOTH.png"),region=None,confidence=0.8)
            if tdm:
                print("Clicked on KOTH")
            else:
                print("KOTH not found")
        else:
            print("Events not found")
    else:
        print("KOTH not open")
    
    hasKOTHStarted = locate_image(__file__.replace("script.py", "KOTHStarted.png"),region=None,confidence=0.8)
    if hasKOTHStarted:
        print("KOTH has started")
        commands = click_on_image(__file__.replace("script.py", "Commands.png"),region=None,confidence=0.6)
        if commands:
            print("Clicked on commands")
            time.sleep(2)
            suicide = click_on_image(__file__.replace("script.py", "Suicide.png"),region=None,confidence=0.6)
            if suicide:
                print("Clicked on Suicide")
            else:
                print("Suicide not found")
        else:
            print("Events not found")

    else:
        print("KOTH not started")
    
    
        


if __name__ == "__main__":
    while True:
        # Locate and click the language selection image
        language = click_on_image(__file__.replace("script.py", "Image.png"),region=None,confidence=0.6)
        print(__file__.replace("script.py", "Image.png"))
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
