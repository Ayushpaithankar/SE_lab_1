"""Hotel room reservation and booking management module."""

import hashlib
import secrets

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}


def book_room(room_num, guest_name, booking_log=None):
    """Reserve an available room and optionally record the booking."""
    if room_num not in room_inventory or room_inventory[room_num]["is_booked"]:
        return False
    if booking_log is None:
        booking_log = []
    room_inventory[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Release a booked room, returning whether the room exists."""
    if room_num not in room_inventory:
        return False
    room_inventory[room_num]["is_booked"] = False
    return True


def check_room_status(room_num):
    """Return whether a known room is currently available."""
    if room_inventory.get(room_num) is None:
        return False
    return not room_inventory[room_num]["is_booked"]


def compute_seasonal_rate(room_num, multiplier):
    """Return a room's rate after applying a non-negative multiplier."""
    base_price = room_inventory[room_num]["price"]
    if not isinstance(multiplier, (int, float)) or multiplier < 0:
        raise ValueError("Seasonal multiplier must be a non-negative number")
    return base_price * multiplier


def generate_guest_hash(guest_id):
    """Create a SHA-256 identifier for a guest ID."""
    return hashlib.sha256(guest_id.encode()).hexdigest()


def generate_booking_ref():
    """Return a cryptographically secure four-digit booking reference."""
    return secrets.randbelow(9000) + 1000


def export_room_ledger(filename="hotel_ledger.txt"):
    """Write the current room inventory to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as ledger_file:
        ledger_file.write(str(room_inventory))
    print("Hotel ledger exported to:", filename)


def main():
    """Run a demonstration of the booking-system operations."""
    book_room("101", "Emma Watson")
    cancel_booking("102")
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", 1.25))
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()


if __name__ == "__main__":
    main()
