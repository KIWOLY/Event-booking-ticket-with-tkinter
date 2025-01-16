import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:8000"  # Update with your backend URL


# User Authentication
def signup_user(username, password, email):
    url = f"{BASE_URL}/api/signup/"
    data = {"username": username, "password": password, "email": email}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        messagebox.showinfo("Success", "User created successfully!")
        show_login_screen()
    else:
        messagebox.showerror("Error", response.json())


def login_user(username, password):
    url = f"{BASE_URL}/api/login/"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        show_events_menu(access_token)  # Show menu after login
    else:
        messagebox.showerror("Error", response.json())


def logout_user(access_token):
    url = f"{BASE_URL}/api/logout/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        messagebox.showinfo("Success", "You have been logged out!")
        # Optionally, redirect to the login screen
        show_login_screen()  # Function to show login screen or exit the app
    else:
        messagebox.showerror("Error", "Failed to log out. Please try again.")

# Events
def fetch_events(access_token):
    url = f"{BASE_URL}/api/events/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "Failed to fetch events")
        return []


def fetch_event_by_id(access_token, event_id):
    url = f"{BASE_URL}/api/events/{event_id}/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "Event not found")
        return None



def create_booking(access_token, event_id, ticket_count):
    url = f"{BASE_URL}/api/booking/"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"event": event_id, "ticket_count": ticket_count}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        messagebox.showinfo("Success", "Booking successful!")
        show_events_menu(access_token)  # Go back to events menu after successful booking
    else:
        messagebox.showerror("Error", response.json())


# User Bookings
def fetch_user_bookings(access_token):
    url = f"{BASE_URL}/api/my-bookings/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "Failed to fetch bookings")
        return []


def update_booking(access_token, booking_id, ticket_count):
    url = f"{BASE_URL}/api/booking/{booking_id}/update/"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"ticket_count": ticket_count}
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        messagebox.showinfo("Success", "Booking updated successfully!")
        show_user_bookings(access_token)
    else:
        messagebox.showerror("Error", "Failed to update booking")



def cancel_booking(access_token, booking_id):
    url = f"{BASE_URL}/api/booking/{booking_id}/cancel/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        messagebox.showinfo("Success", "Booking canceled successfully!")
        show_user_bookings(access_token)
    else:
        messagebox.showerror("Error", f"Failed to cancel booking: {response.json().get('error', 'Unknown error')}")





# GUI Screens

def show_signup_screen():
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="lightgray")
    

    tk.Label(root, text="Signup", font=("Arial", 24, "bold"), bg="lightblue", pady=10).pack(fill="x")
    

    frame = tk.Frame(root, bg="lightgray")
    frame.pack(pady=40)

    tk.Label(frame, text="Username:", font=("Arial", 12), bg="lightgray").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    username_entry = tk.Entry(frame, font=("Arial", 12))
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Password:", font=("Arial", 12), bg="lightgray").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12))
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Email:", font=("Arial", 12), bg="lightgray").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12))
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    # Signup Button
    tk.Button(root, text="Signup", font=("Arial", 14), command=lambda: signup_user(
        username_entry.get(), password_entry.get(), email_entry.get()
    ), bg="lightgreen", width=20).pack(pady=10)

    # Login link
    tk.Button(root, text="Already have an account? Login", font=("Arial", 12), command=show_login_screen, bg="lightblue").pack(pady=10)


def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="lightgray")
    
    # Header
    tk.Label(root, text="Login", font=("Arial", 24, "bold"), bg="lightblue", pady=10).pack(fill="x")

    # Form fields
    frame = tk.Frame(root, bg="lightgray")
    frame.pack(pady=20)

    tk.Label(frame, text="Username:", font=("Arial", 12), bg="lightgray").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    username_entry = tk.Entry(frame, font=("Arial", 12))
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Password:", font=("Arial", 12), bg="lightgray").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12))
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    # Login Button
    tk.Button(root, text="Login", font=("Arial", 14), command=lambda: login_user(
        username_entry.get(), password_entry.get()
    ), bg="lightgreen", width=20).pack(pady=10)

    # Signup link
    tk.Button(root, text="Don't have an account? Signup", font=("Arial", 12), command=show_signup_screen, bg="lightblue").pack(pady=10)




def show_events_menu(access_token):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Events Menu", font=("Arial", 20), bg="lightblue").pack(pady=10)

    tk.Button(root, text="Show All Events", command=lambda: show_all_events(access_token)).pack(pady=10)
    tk.Button(root, text="Search Event by ID", command=lambda: show_event_search(access_token)).pack(pady=10)
    tk.Button(root, text="View Your Bookings", command=lambda: show_user_bookings(access_token)).pack(pady=10)
    tk.Button(root, text="Logout", command=lambda: logout_user(access_token)).pack(pady=10)



def show_all_events(access_token):
    events = fetch_events(access_token)
    
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="lightgray")

    # Header
    tk.Label(root, text="All Events", font=("Arial", 24, "bold"), bg="lightblue", pady=10).grid(row=0, column=0, columnspan=7, pady=10, sticky="nsew")

    if events:
        # Create headers for the grid
        headers = ["Event ID", "Event Name", "Date & Time", "Location", "Price", "Available Tickets", "Actions"]
        for col, header in enumerate(headers):
            tk.Label(root, text=header, font=("Arial", 12, "bold"), bg="lightyellow", padx=10, pady=10).grid(row=1, column=col, sticky="nsew")

        # Display events in the grid
        for row, event in enumerate(events, start=2):
            tk.Label(root, text=event["id"], font=("Arial", 10), bg="lightgray", padx=10).grid(row=row, column=0, sticky="w", pady=5)  # Event ID
            tk.Label(root, text=event["name"], font=("Arial", 10), bg="lightgray", padx=10).grid(row=row, column=1, sticky="w", pady=5)
            tk.Label(root, text=f"{event['date']} {event['time']}", font=("Arial", 10), bg="lightgray", padx=10).grid(row=row, column=2, sticky="w", pady=5)
            tk.Label(root, text=event.get("location", "N/A"), font=("Arial", 10), bg="lightgray", padx=10).grid(row=row, column=3, sticky="w", pady=5)
            tk.Label(root, text=f"{event['price']} TZS", font=("Arial", 10), bg="lightgray", padx=10).grid(row=row, column=4, sticky="w", pady=5)
            tk.Label(root, text=event["available_tickets"], font=("Arial", 10), bg="lightgray", padx=10).grid(row=row, column=5, sticky="w", pady=5)

            # "Book Tickets" button
            tk.Button(
                root, text="Book Tickets",
                command=lambda event_id=event['id']: show_event_booking_for_event(event_id, access_token),
                bg="lightgreen", font=("Arial", 10), width=15
            ).grid(row=row, column=6, padx=10, pady=5, sticky="w")

    else:
        tk.Label(root, text="No events found.", font=("Arial", 12), bg="lightyellow").grid(row=2, column=0, columnspan=7, pady=10)

    # Back button
    tk.Button(root, text="Back to Events Menu", command=lambda: show_events_menu(access_token), bg="lightblue", font=("Arial", 12), width=20).grid(row=len(events) + 2, column=0, columnspan=7, pady=10)




def show_event_search(access_token):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Search Event by ID", font=("Arial", 20), bg="lightblue").pack(pady=10)

    tk.Label(root, text="Enter Event ID:").pack()
    event_id_entry = tk.Entry(root)
    event_id_entry.pack()

    def search_event():
        event_id = event_id_entry.get()
        if event_id.isdigit():
            event = fetch_event_by_id(access_token, int(event_id))
            if event:
                display_event_info(event, access_token)
        else:
            messagebox.showerror("Error", "Please enter a valid event ID.")

    tk.Button(root, text="Search", command=search_event).pack(pady=10)
    tk.Button(root, text="Back to Events Menu", command=lambda: show_events_menu(access_token)).pack(pady=10)


def display_event_info(event, access_token):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Event Details", font=("Arial", 20), bg="lightblue").pack(pady=10)

    event_info = (
        f"Event ID: {event['id']}\n"
        f"Name: {event['name']}\n"
        f"Date: {event['date']} {event['time']}\n"
        f"Location: {event.get('location', 'Not available')}\n"
        f"Available Tickets: {event['available_tickets']}\n"
        f"Price: {event['price']} TZS\n"
    )
    tk.Label(root, text=event_info, justify="left", anchor="w", padx=10, font=("Arial", 12), bg="lightyellow").pack(fill="x", pady=10)

    tk.Button(root, text="Book Tickets", command=lambda: show_event_booking_for_event(event['id'], access_token)).pack(pady=10)
    tk.Button(root, text="Back to Search", command=lambda: show_event_search(access_token)).pack(pady=10)
    tk.Button(root, text="Back to Events Menu", command=lambda: show_events_menu(access_token)).pack(pady=10)



def show_event_booking_for_event(event_id, access_token):
    def book_ticket():
        ticket_count = ticket_count_entry.get()
        if not ticket_count or not ticket_count.isdigit():
            messagebox.showerror("Error", "Please enter a valid ticket count.")
            return
        create_booking(access_token, event_id, int(ticket_count))

    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="lightgray")
    
    # Header
    tk.Label(root, text="Book Tickets", font=("Arial", 24, "bold"), bg="lightblue", pady=10).pack(fill="x")

    # Ticket Count Field
    frame = tk.Frame(root, bg="lightgray")
    frame.pack(pady=20)

    tk.Label(frame, text="Ticket Count:", font=("Arial", 12), bg="lightgray").grid(row=0, column=0, sticky="w", padx=15, pady=10)
    ticket_count_entry = tk.Entry(frame, font=("Arial", 12))
    ticket_count_entry.grid(row=0, column=1, padx=15, pady=10)

    # Book Button
    tk.Button(root, text="Book", command=book_ticket, font=("Arial", 14), bg="lightgreen", width=20).pack(pady=10)

    # Navigation Buttons
    tk.Button(root, text="Back to Event Details", command=lambda: display_event_info(fetch_event_by_id(access_token, event_id), access_token),
              font=("Arial", 12), bg="lightblue", width=20).pack(pady=5)
    
    tk.Button(root, text="Back to Events Menu", command=lambda: show_events_menu(access_token), 
              font=("Arial", 12), bg="lightblue", width=20).pack(pady=5)



def show_user_bookings(access_token):
    # Fetch bookings again after canceling a booking
    bookings = fetch_user_bookings(access_token)
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Your Bookings", font=("Arial", 20), bg="lightblue").grid(row=0, column=0, columnspan=4, pady=10)

    if bookings:
        # Headers
        tk.Label(root, text="Booking ID", font=("Arial", 12, "bold"), bg="lightyellow").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Label(root, text="Event Name", font=("Arial", 12, "bold"), bg="lightyellow").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Label(root, text="Ticket Count", font=("Arial", 12, "bold"), bg="lightyellow").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        tk.Label(root, text="Actions", font=("Arial", 12, "bold"), bg="lightyellow").grid(row=1, column=3, padx=5, pady=5, sticky="w")
        tk.Label(root, text="Actions", font=("Arial", 12, "bold"), bg="lightyellow").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        #  i suupose to loop so as i can get all user booking
        for idx, booking in enumerate(bookings, start=2):
            event = fetch_event_by_id(access_token, booking['event'])

            tk.Label(root, text=booking['id'], font=("Arial", 12), bg="lightyellow").grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            tk.Label(root, text=event['name'], font=("Arial", 12), bg="lightyellow").grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            tk.Label(root, text=booking['ticket_count'], font=("Arial", 12), bg="lightyellow").grid(row=idx, column=2, padx=5, pady=5, sticky="w")

            # Update button: Trigger function to show the update screen
            tk.Button(
                root,
                text="Update",
                command=lambda b=booking: show_update_booking_screen(access_token, b['id'], b['ticket_count'])
            ).grid(row=idx, column=3, padx=5, pady=5, sticky="w")

            # Cancel button: Trigger function to cancel the booking and update UI
            tk.Button(
                root,
                text="Cancel",
                command=lambda b=booking: cancel_booking_and_remove_from_ui(access_token, b['id'])
            ).grid(row=idx, column=4, padx=5, pady=5, sticky="w")

    else:
        tk.Label(root, text="No bookings found.", font=("Arial", 12), bg="lightyellow").grid(row=2, column=0, columnspan=4, pady=10)

    # Back button to navigate to the events menu
    tk.Button(root, text="Back to Events Menu", command=lambda: show_events_menu(access_token)).grid(row=len(bookings) + 3, column=0, columnspan=4, pady=10)


def cancel_booking_and_remove_from_ui(access_token, booking_id):
    url = f"{BASE_URL}/api/booking/{booking_id}/cancel/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        messagebox.showinfo("Success", "Booking canceled successfully!")
        show_user_bookings(access_token)  # Refresh the bookings list to remove the canceled booking
    else:
        messagebox.showerror("Error", f"Failed to cancel booking: {response.json().get('error', 'Unknown error')}")



def show_update_booking_screen(access_token, booking_id, current_ticket_count):
    def update_booking_action():
        new_ticket_count = ticket_count_entry.get()
        if new_ticket_count.isdigit():
            new_ticket_count = int(new_ticket_count)
            if new_ticket_count != current_ticket_count:
                update_booking(access_token, booking_id, new_ticket_count)
                show_user_bookings(access_token)
            else:
                messagebox.showinfo("Info", "Ticket count is the same as before.")
        else:
            messagebox.showerror("Error", "Please enter a valid ticket count.")

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Update Booking", font=("Arial", 20), bg="lightblue").pack(pady=10)

    tk.Label(root, text=f"Current Ticket Count: {current_ticket_count}").pack()
    tk.Label(root, text="New Ticket Count:").pack()
    ticket_count_entry = tk.Entry(root)
    ticket_count_entry.pack()

    tk.Button(root, text="Update", command=update_booking_action).pack(pady=10)
    tk.Button(root, text="Back to Your Bookings", command=lambda: show_user_bookings(access_token)).pack(pady=10)


root = tk.Tk()
root.title("Event Ticket Booking System")
root.geometry("400x500")
root.config(bg="lightblue")


show_login_screen()

root.mainloop()
