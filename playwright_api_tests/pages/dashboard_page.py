
from playwright.sync_api import Page, expect

class DashboardPage:

    URL = "http://localhost:3000"

    def __init__(self, page:Page):

        self.page = page

        #the cards
        self.card_total = page.locator("#card-total") 
        self.card_alerts = page.locator("#card-alerts")
        self.card_safe = page.locator("#card-safe")

        #the numbers in the card
        self.stat_total = page.locator("#stat-total")
        self.stat_alerts = page.locator("#stat-alerts")
        self.stat_safe   = page.locator("#stat-safe")

        # ── Filter Buttons ────────────────────────────────
        self.btn_all    = page.locator("#btn-all")
        self.btn_alerts = page.locator("#btn-alerts")
        self.btn_safe   = page.locator("#btn-safe")

        # ── Submit Form ───────────────────────────────────
        self.input_vehicle_id = page.locator("#input-vehicle-id")
        self.input_speed      = page.locator("#input-speed")
        self.input_fuel       = page.locator("#input-fuel")
        self.input_lat        = page.locator("#input-lat")
        self.input_lon        = page.locator("#input-lon")
        self.btn_submit       = page.locator("#btn-submit")
        self.submit_message   = page.locator("#submit-message")

         # ── Table ─────────────────────────────────────────
        self.table      = page.locator("table")
        self.table_body = page.locator("tbody")
        self.table_rows = page.locator("tbody tr")        # all rows
        self.alert_rows = page.locator("tr.alert-row")   # red rows
        self.safe_rows  = page.locator("tr.safe-row")    # green rows

        # ── Table Headers ─────────────────────────────────
        self.table_headers = page.locator("th")

    def goto(self):
       
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000) 

    # ── Filter Button Actions ─────────────────────────────

    def click_all_records(self):
        
        self.btn_all.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector("tbody tr")

    def click_alerts_only(self):
        
        self.btn_alerts.click()
        self.page.wait_for_load_state("networkidle")

    def click_safe_only(self):
        
        self.btn_safe.click()
        self.page.wait_for_load_state("networkidle")

    # ── Form Actions ─────────────────────────────────────

    def submit_telemetry(self, vehicle_id, speed, fuel, lat, lon):
       
        # str() converts numbers to string for fill()
        self.input_vehicle_id.fill(str(vehicle_id))
        self.input_speed.fill(str(speed))
        self.input_fuel.fill(str(fuel))
        self.input_lat.fill(str(lat))
        self.input_lon.fill(str(lon))
        self.btn_submit.click()
        # Wait for API call to complete
        self.page.wait_for_timeout(3000)

    def clear_form(self):
       
        self.input_vehicle_id.clear()
        self.input_speed.clear()
        self.input_fuel.clear()
        self.input_lat.clear()
        self.input_lon.clear()

    # ── Stat Card Getters ─────────────────────────────────

    def get_total_count(self):
        
        return int(self.stat_total.text_content())

    def get_alert_count(self):
        
        return int(self.stat_alerts.text_content())

    def get_safe_count(self):
        
        return int(self.stat_safe.text_content())

    # ── Table Getters ─────────────────────────────────────

    def get_row_count(self):
       
        return self.table_rows.count()

    def get_alert_row_count(self):
        
        return self.alert_rows.count()

    def get_safe_row_count(self):
        
        return self.safe_rows.count()

    def get_first_row_vehicle_id(self):
        
        return self.table_rows.first.locator("td").first.text_content()

    def get_row_data(self, row_index):
       
        row = self.table_rows.nth(row_index)
        cells = row.locator("td")
        return [cells.nth(i).text_content() for i in range(cells.count())]

    # ── Submit Message Getters ────────────────────────────

    def get_submit_message(self):
        
        return self.submit_message.text_content()

    def get_submit_message_class(self):
        
        return self.submit_message.get_attribute("class")

    def is_submit_success(self):
        
        return self.get_submit_message_class() == "success"

    def is_submit_error(self):
        
        return self.get_submit_message_class() == "error"

    # ── Visibility Checks ────────────────────────────────

    def is_table_visible(self):
        
        return self.table.is_visible()

    def is_loading_visible(self):
        
        return self.page.locator("#loading").is_visible()

    def is_error_visible(self):
        
        return self.page.locator("#error-message").is_visible()

    # ── Screenshot ───────────────────────────────────────

    def take_screenshot(self, filename="screenshot.png"):
       
        self.page.screenshot(path=filename)

