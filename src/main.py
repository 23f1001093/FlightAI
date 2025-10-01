from playwright.sync_api import sync_playwright
from selectors_makemytrip import SELECTORS
from AI_utils import generate_passenger_data
import json, csv, os, time

def search_and_book_flight():
    passenger = generate_passenger_data(use_ai=True)
    print(f"Generated passenger: {passenger}")

    with sync_playwright() as p:
        # Uncomment next three lines for mobile emulation if desktop blocks you
        # iphone_12 = p.devices['iPhone 12']
        # browser = p.chromium.launch(headless=False)
        # context = browser.new_context(**iphone_12)
        
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Randomize desktop headers, start with fresh cookies/localStorage
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        })
        context.clear_cookies()
        page.goto("https://www.makemytrip.com/flights/")
        time.sleep(3)
        
        try:
             page.evaluate("window.localStorage.clear()")
        except Exception as e:
             print("localStorage clear error (usually safe to ignore):", e)

        # Dismiss overlays
        for selector in [
            "span.commonModal__close", "span[data-cy='closeModal']",
            ".loginModal button.close", ".modalClose", "span[role='button'].modalClose",
            ".modalCloseIcon", ".widgetClose"
        ]:
            try:
                page.click(selector)
                print(f"Closed overlay: {selector}")
                time.sleep(0.5)
                break
            except Exception:
                continue

        try:
            page.click(SELECTORS.get("overlay_close_btn", ""))
        except Exception:
            pass
        page.mouse.click(10, 10)
        time.sleep(1)

        # FROM city: Delhi
        page.click(SELECTORS["from_city_input"])
        
        page.keyboard.type("Delhi")
        page.keyboard.press("Enter")
        time.sleep(2)

        # TO city: Mumbai (autosuggest)
        page.click(SELECTORS["to_city_input"])
        time.sleep(1)
        page.keyboard.type("Mumbai")
        time.sleep(2)
        page.wait_for_selector("li.react-autosuggest__suggestion")
        suggestions = page.query_selector_all("li.react-autosuggest__suggestion")
        found = False
        for suggestion in suggestions:
            if "Mumbai" in suggestion.inner_text() and "BOM" in suggestion.inner_text():
                suggestion.click()
                print("Selected Mumbai BOM from autosuggest.")
                found = True
                break
        if not found and suggestions:
            suggestions[0].click()
            print("Selected first autosuggest option as fallback")
        time.sleep(2)

        # Date picker: Workaround for sticky overlays
        page.mouse.click(10, 10)
        time.sleep(1)
        page.evaluate("window.scrollBy(0, 400)")
        time.sleep(1)
        page.click(SELECTORS["dep_date_input"], force=True)
        time.sleep(2)

        # Select first enabled date
        page.wait_for_selector(".dateInnerCell")
        date_cells = page.query_selector_all('.dateInnerCell')
        date_selected = False
        for cell in date_cells:
            if "disabled" not in (cell.get_attribute("class") or ""):
                cell.click()
                print("Selected departure date.")
                date_selected = True
                break
        if not date_selected:
            print("No valid departure date found.")
            context.close()
            return
        time.sleep(2)
        page.mouse.click(10, 10)
        time.sleep(2)

        # Click Search, wait for results, take screenshot for debugging
        page.click(SELECTORS["search_button"])
        print("Clicked Search. Waiting for flight results...")
        try:
            page.wait_for_selector(".splitViewListing, .fli-list, .splitVw__card", timeout=60000)
        except Exception:
            print("No flight results found. Check selector or try mobile emulation.")
            page.screenshot(path="output/results_debug.png")
            context.close()
            return
        page.screenshot(path="output/results_debug.png")

        # Flight extraction (most common selectors)
        flights = []
        for card in page.query_selector_all(".splitVw__card, .splitViewListing, .fli-list"):
            try:
                name = card.query_selector(SELECTORS["flight_name"]).inner_text()
                depart = card.query_selector(SELECTORS["depart_time"]).inner_text()
                arrive = card.query_selector(SELECTORS["arrive_time"]).inner_text()
                price = card.query_selector(SELECTORS["flight_price"]).inner_text()
                flights.append({
                    "flight": name,
                    "depart_time": depart,
                    "arrive_time": arrive,
                    "price": price
                })
            except Exception:
                continue

        print("\nFlight Results Found:")
        for flight in flights:
            print(flight)

        os.makedirs("output", exist_ok=True)
        with open("output/flight_results.json", "w") as f:
            json.dump(flights, f, indent=2)
        with open("output/flight_results.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["flight", "depart_time", "arrive_time", "price"])
            writer.writeheader()
            for flight in flights:
                writer.writerow(flight)
        print("Flight data saved to output/flight_results.json and output/flight_results.csv")

        # Book first flight if available
        review = None
        if flights:
            first_card = page.query_selector_all(".splitVw__card, .splitViewListing, .fli-list")[0]
            book_btn = first_card.query_selector(SELECTORS["book_now"])
            if book_btn:
                book_btn.click()
                full_name = passenger["name"].split(" ", 1)
                first_name = full_name[0]
                last_name = full_name[1] if len(full_name) > 1 else ""
                page.fill(SELECTORS["first_name_input"], first_name)
                page.fill(SELECTORS["last_name_input"], last_name)
                page.fill(SELECTORS["phone_input"], passenger["phone"])
                page.fill(SELECTORS["email_input"], passenger["email"])
                try:
                    page.wait_for_selector(SELECTORS["review_page"], timeout=7000)
                    review = page.query_selector(SELECTORS["review_page"]).inner_text()
                    print("\nBooking Review Details:\n", review)
                except Exception:
                    print("Review details not found.")
                    review = "No review details found"
        with open("output/booking_review.txt", "w") as f:
            f.write(review or "No booking attempted.")
        print("Booking review saved to output/booking_review.txt")
        context.close()

if __name__ == "__main__":
    search_and_book_flight()
