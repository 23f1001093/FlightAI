# ✈️ MakeMyTrip Flight Automation

This project automates the process of searching and optionally booking flights on [MakeMyTrip](https://www.makemytrip.com/) using Playwright (and optionally Scrapybara for cloud execution). The bot mimics human actions to navigate the site, fill search fields, extract flight results, and proceed to the booking flow.



##  How It Works: Step-by-Step

1. **Open Flights Homepage**  
   Navigates to homepage of makemytrip website

2. **Dismiss Overlays & Modals**  
   Closes any login popups, banners, or modal dialogs that block UI interaction.

3. **Enter Cities**  
   - Clicks on the **FROM** city input (`#fromCity`)
   - Types and selects "Delhi" from autosuggest
   - Clicks on the **TO** city input (`#toCity`)
   - Types and selects "Mumbai" from autosuggest

4. **Set Departure Date**  
   - Clicks on the departure date field (`#departure`)
   - Selects the next available (non-disabled) date

5. **Start the Flight Search**  
   - Clicks the Search button (`.primaryBtn.widgetSearchBtn`)
   - Waits for the flight results to load

6. **Extract & Display Results**  
   - Iterates through result cards (`.splitViewListing`)
   - Extracts and displays: airline name, departure time, arrival time, price

7. **Optionally Book a Flight**  
   - Clicks the "View Prices" button on first flight (`button:has(span[data-test="component-buttonText"])`)
   - Clicks the "Book Now" button (`button.buttonPrimary.buttonBig`)
   - Fills in passenger details (names, phone, email)
   - Completes booking form and saves review details

8. **Save and Export Results**  
   - Saves extracted flight info to `output/flight_results.json` and `output/flight_results.csv`
   - Optionally saves booking review to `output/booking_review.txt`

---

## 🖱️ UI Buttons and Selectors Used

| Step/Action          | Selector Used                                   |
|----------------------|-------------------------------------------------|
| Close overlays       | `.modalClose`, `span[data-cy='closeModal']`, etc.|
| From city input      | `#fromCity`                                     |
| To city input        | `#toCity`                                       |
| Departure date input | `#departure`                                    |
| Search button        | `.primaryBtn.widgetSearchBtn`                   |
| Flight result card   | `.splitViewListing`                             |
| Airline name         | `span.boldFont.blackText`                       |
| Departure time       | `div.timeInfoLeft span.flightTimeInfo span`      |
| Arrival time         | `div.timeInfoRight span.flightTimeInfo span`     |
| Price                | `div.splitfare p.blackText.fontSize16.blackFont` |
| View Prices button   | `button:has(span[data-test="component-buttonText"])` |
| Book Now button      | `button.buttonPrimary.buttonBig`                |
| Passenger fields     | `input[placeholder="First & Middle Name"]`, etc.|
| Review page          | `.reviewDtlsOverlayContent`                     |

---

## 📝 Notes

- All automation steps include random delays, human-like mouse clicks, and retry logic to mimic real user behavior and reduce bot detection.
- After all these steps --- bot is still detected



