
"""Warehouse asset maintenance and inspection tracking system."""

import json
import tempfile
from datetime import datetime, timedelta

# Application state and configuration.
assets = {}
registration_log = []
CONFIG = {"service_interval_days": 90}


def register_asset(asset_id, machine_type, logs=None):
    """Register a warehouse asset and record the registration."""
    if not asset_id or not asset_id.strip():
        print("Cannot register asset: asset ID cannot be empty")
        return

    if logs is None:
        logs = registration_log

    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime("%Y-%m-%d"),
    }
    logs.append(asset_id)
    print(
        "Registered",
        asset_id,
        "- total registrations this run:",
        len(logs),
    )


def update_service_date(asset_id, service_date):
    """Update an existing asset's service date after validating it."""
    try:
        datetime.strptime(service_date, "%Y-%m-%d")
        assets[asset_id]["last_service"] = service_date
    except KeyError:
        print("Could not update", asset_id)
    except (TypeError, ValueError):
        print("Invalid service date for", asset_id)


def due_for_inspection():
    """Return asset IDs whose service dates exceed the configured interval."""
    due = []
    for asset_id, asset in assets.items():
        last_service = datetime.strptime(
            asset["last_service"], "%Y-%m-%d"
        )
        if datetime.now() - last_service > timedelta(
            days=CONFIG["service_interval_days"]
        ):
            due.append(asset_id)
    return due


def change_interval(days):
    """Set a positive service interval in days."""
    if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
        raise ValueError("Service interval must be a positive integer")
    CONFIG["service_interval_days"] = days


def export_service_report(file="maintenance.json"):
    """Export registered assets to a JSON report."""
    with open(file, "w", encoding="utf-8") as report_file:
        json.dump(assets, report_file, indent=2)
    print("Report written to", file)


def write_scratch_copy():
    """Write assets to a securely created temporary JSON file."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        encoding="utf-8",
        delete=False,
    ) as scratch_file:
        json.dump(assets, scratch_file)
        path = scratch_file.name
    print("Scratch copy at", path)


def print_alerts():
    """Print an alert for every asset overdue for inspection."""
    for asset_id in due_for_inspection():
        print(
            "ALERT: inspection overdue for",
            asset_id,
            assets[asset_id]["type"],
        )


def main():
    """Run the sample warehouse maintenance workflow."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(90)

    service_date = input(
        "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
    )
    if service_date:
        update_service_date("CV-07", service_date)

    if not assets:
        raise ValueError("No assets are registered")

    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
