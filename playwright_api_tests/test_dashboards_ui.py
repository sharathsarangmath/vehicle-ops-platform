import pytest
from playwright.sync_api import expect


# ─── Page Loads ──────────────────────────────────────────

def test_page_title_correct(dashboard):
    dashboard.goto()
    expect(dashboard.page).to_have_title(
        "Vehicle Operations Platform"
    )

def test_heading_visible(dashboard):
    dashboard.goto()
    expect(dashboard.page.locator("h1")).to_contain_text(
        "Vehicle Operations Platform"
    )

def test_table_visible(dashboard):
    dashboard.goto()
    expect(dashboard.table).to_be_visible()

def test_all_stat_cards_visible(dashboard):
    dashboard.goto()
    expect(dashboard.card_total).to_be_visible()
    expect(dashboard.card_alerts).to_be_visible()
    expect(dashboard.card_safe).to_be_visible()

def test_all_filter_buttons_visible(dashboard):
    dashboard.goto()
    expect(dashboard.btn_all).to_be_visible()
    expect(dashboard.btn_alerts).to_be_visible()
    expect(dashboard.btn_safe).to_be_visible()

def test_submit_form_visible(dashboard):
    dashboard.goto()
    expect(dashboard.input_vehicle_id).to_be_visible()
    expect(dashboard.input_speed).to_be_visible()
    expect(dashboard.input_fuel).to_be_visible()
    expect(dashboard.btn_submit).to_be_visible()

# ─── Stat Cards ──────────────────────────────────────────

def test_total_count_is_number(dashboard):
    dashboard.goto()
    count = dashboard.get_total_count()
    assert isinstance(count, int)
    assert count >= 0

def test_total_equals_alerts_plus_safe(dashboard):
    dashboard.goto()
    total  = dashboard.get_total_count()
    alerts = dashboard.get_alert_count()
    safe   = dashboard.get_safe_count()
    assert total == alerts + safe

# ─── Filter Buttons ──────────────────────────────────────

def test_alerts_filter_shows_no_safe_rows(dashboard):
    dashboard.goto()
    dashboard.click_alerts_only()
    assert dashboard.get_safe_row_count() == 0

def test_safe_filter_shows_no_alert_rows(dashboard):
    dashboard.goto()
    dashboard.click_safe_only()
    assert dashboard.get_alert_row_count() == 0

def test_all_filter_shows_rows(dashboard):
    dashboard.goto()
    dashboard.click_all_records()
    assert dashboard.get_row_count() > 0

# ─── Submit Form ─────────────────────────────────────────

def test_submit_valid_data_shows_success(dashboard):
    dashboard.goto()
    dashboard.submit_telemetry(
        vehicle_id="VH-UI-001",
        speed=80,
        fuel=50,
        lat=53.3498,
        lon=-6.2603
    )
    assert "Submitted" in dashboard.get_submit_message()

def test_submit_success_has_correct_class(dashboard):
    dashboard.goto()
    dashboard.submit_telemetry(
        vehicle_id="VH-UI-002",
        speed=80,
        fuel=50,
        lat=53.3498,
        lon=-6.2603
    )
    assert dashboard.get_submit_message_class() == "success"

def test_submit_alert_data_shows_two_alerts(dashboard):
    dashboard.goto()
    dashboard.submit_telemetry(
        vehicle_id="VH-UI-ALERT",
        speed=150,
        fuel=5,
        lat=53.3498,
        lon=-6.2603
    )
    assert "2" in dashboard.get_submit_message()

# ─── Parametrize ─────────────────────────────────────────

@pytest.mark.parametrize("speed,fuel,expected_alerts", [
    (80,  50, "0"),
    (150, 50, "1"),
    (80,  5,  "1"),
    (150, 5,  "2"),
])
def test_alert_counts(dashboard, speed, fuel, expected_alerts):
    dashboard.goto()
    dashboard.submit_telemetry(
        vehicle_id=f"VH-{speed}-{fuel}",
        speed=speed,
        fuel=fuel,
        lat=53.3498,
        lon=-6.2603
    )
    assert expected_alerts in dashboard.get_submit_message()