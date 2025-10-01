from selectors_makemytrip import SELECTORS
import time

def search_flights(page, from_city, to_city, dep_date):
    #from city
    page.click(SELECTORS["from_city_input"])
    page.keyboard.type(from_city)
    page.keyboard.press("Enter")
    time.sleep(0.7)

    #to city 
    page.click(SELECTORS["to_city_input"])
    page.keyboard.type(to_city)
    page.wait_for_selector("li.react-autosuggest__suggestion", timeout=7000)
    suggestions = page.query_selector_all("li.react-autosuggest__suggestion")
    if suggestions:
        suggestions[0].click()
    else:
        page.keyboard.press("Enter")
    time.sleep(0.7)

    
    page.click(SELECTORS["dep_date_input"])
    page.wait_for_selector(".dateInnerCell")
    date_cells = page.query_selector_all('.dateInnerCell')
    for cell in date_cells:
        if "disabled" not in (cell.get_attribute("class") or ""):
            cell.click()
            break
    time.sleep(0.7)

    #search btn
    page.click(SELECTORS["search_button"])
    page.wait_for_selector(SELECTORS["results_list"])

    flights = []
    for card in page.query_selector_all(SELECTORS["flight_card"]):
        try:
            name = card.query_selector(SELECTORS["flight_name"]).inner_text()
            depart = card.query_selector(SELECTORS["depart_time"]).inner_text()
            arrive = card.query_selector(SELECTORS["arrive_time"]).inner_text()
            price = card.query_selector(SELECTORS["flight_price"]).inner_text()
            flights.append({
                "card": card,
                "flight": name,
                "depart_time": depart,
                "arrive_time": arrive,
                "price": price
            })
        except Exception:
            continue

    return flights

def book_flight(page, card, profile):
    
    if "first_name" not in profile or "last_name" not in profile:
        full_name = profile["name"].split(" ", 1)
        profile["first_name"] = full_name[0]
        profile["last_name"] = full_name[1] if len(full_name) > 1 else ""

    book_btn = card.query_selector(SELECTORS["book_now"])
    if book_btn:
        book_btn.click()
        time.sleep(0.7)
        #passenger details
        page.fill(SELECTORS["first_name_input"], profile["first_name"])
        page.fill(SELECTORS["last_name_input"], profile["last_name"])
        page.fill(SELECTORS["phone_input"], profile["phone"])
        page.fill(SELECTORS["email_input"], profile["email"])
        #page.click("button[type='submit']") 
        try:
            page.wait_for_selector(SELECTORS["review_page"], timeout=7000)
            review = page.query_selector(SELECTORS["review_page"]).inner_text()
        except Exception:
            review = None
        return review
    return None
