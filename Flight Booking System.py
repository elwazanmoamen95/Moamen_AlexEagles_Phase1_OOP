import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from datetime import datetime, timedelta

# Utility function for advanced dynamic pricing
def advanced_dynamic_pricing(base_price, demand_factor, booking_time, historical_data, user_behavior):
    current_time = datetime.now()
    hours_to_flight = (booking_time - current_time).total_seconds() / 3600
    if hours_to_flight <= 0:
        hours_to_flight = 1  # Prevent division by zero

    demand_multiplier = demand_factor / hours_to_flight
    
    # Example of incorporating historical data and user behavior
    historical_multiplier = historical_data.get('price_increase_factor', 1)
    behavior_multiplier = user_behavior.get('user_spending_multiplier', 1)
    
    price_multiplier = max(1, demand_multiplier * historical_multiplier * behavior_multiplier)
    return int(base_price * price_multiplier)

class Flight:
    def __init__(self, flight_number, airline, departure, arrival, price, seats, date):
        self.flight_number = flight_number
        self.airline = airline
        self.departure = departure
        self.arrival = arrival
        self.price = price
        self.seats = seats  # Seat availability chart (2D list)
        self.booked_seats = []
        self.date = date

    def select_seat(self, row, col):
        if self.seats[row][col] == 'O':  # O indicates the seat is open
            self.seats[row][col] = 'X'  # X indicates the seat is booked
            self.booked_seats.append((row, col))
            return True
        return False


    def cancel_seat(self, row, col):
        if self.seats[row][col] == 'X':  # X indicates the seat is booked
            self.seats[row][col] = 'O'  # O indicates the seat is open
            self.booked_seats.remove((row, col))
            return True
        return False

class Service:
    def __init__(self, name, price, image=None):
        self.name = name
        self.price = price
        self.image = image  # Optional image for preview

class Booking:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.flights = []
        self.total_cost = 0
        self.selected_services = []
        self.itinerary = ""

    def add_flight(self, flight, seat_row, seat_col):
        if not flight.select_seat(seat_row, seat_col):
            self.flights.append(flight)
            self.total_cost += flight.price
            self.itinerary += f"Flight: {flight.flight_number}, Airline: {flight.airline}, " \
                              f"Departure: {flight.departure}, Arrival: {flight.arrival}, Date: {flight.date}, " \
                              f"Seat: {seat_row+1}-{seat_col+1}\n"
        else:
            raise Exception("Seat already booked")

    def add_service(self, service):
        self.selected_services.append(service)
        self.total_cost += service.price
        self.itinerary += f"Service: {service.name}, Price: {service.price}\n"

    def generate_itinerary(self):
        return f"Customer: {self.customer_name}\n" + self.itinerary + f"Total Cost: ${self.total_cost}"

class FlightBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Booking System")

        self.customer_name = tk.StringVar()
        self.selected_seats = []  # Ensure this list is properly populated
        self.services = [
            Service("In-flight Movie", 15, "movie.png"),
            Service("Extra Luggage", 50, "luggage.png"),
            Service("Special Meal", 25, "meal.png"),
            Service("Wi-Fi Access", 10, "wifi.png"),
        ]
        self.historical_data = {'price_increase_factor': 1.2}  # Example historical data
        self.user_behavior = {'user_spending_multiplier': 1.1}  # Example user behavior

        # Flight Data (Placeholder)
        self.available_flights = [
            Flight("AA123", "American Airlines", "New York", "Los Angeles", 
                   advanced_dynamic_pricing(300, 2, datetime(2024, 9, 5, 15, 0), self.historical_data, self.user_behavior), 
                   [["O"]*6 for _ in range(6)], "2024-09-05"),
            Flight("AC183", "Spain Airlines", "barcelona", "Los Angeles", 
                   advanced_dynamic_pricing(300, 2, datetime(2024, 9, 5, 15, 0), self.historical_data, self.user_behavior), 
                   [["O"]*6 for _ in range(6)], "2024-09-05"),
            Flight("BA456", "British Airways", "London", "New York", 
                   advanced_dynamic_pricing(600, 1.5, datetime(2024, 9, 6, 10, 0), self.historical_data, self.user_behavior), 
                   [["O"]*6 for _ in range(6)], "2024-09-06"),
            Flight("DL789", "Delta Airlines", "Atlanta", "Paris", 
                   advanced_dynamic_pricing(450, 1.8, datetime(2024, 9, 7, 12, 0), self.historical_data, self.user_behavior), 
                   [["O"]*6 for _ in range(6)], "2024-09-07"),
            Flight("UA987", "United Airlines", "San Francisco", "Tokyo", 
                   advanced_dynamic_pricing(700, 1.6, datetime(2024, 9, 8, 20, 0), self.historical_data, self.user_behavior), 
                   [["O"]*6 for _ in range(6)], "2024-09-08"),
            Flight("AF654", "Air France", "Paris", "Tokyo", 
                   advanced_dynamic_pricing(650, 1.4, datetime(2024, 9, 9, 18, 0), self.historical_data, self.user_behavior), 
                   [["O"]*6 for _ in range(6)], "2024-09-09")
        ]

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Customer Name:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.customer_name).grid(row=0, column=1)

        tk.Label(self.root, text="Travel Date:").grid(row=1, column=0)
        self.date_slider = tk.Scale(self.root, from_=0, to=4, orient=tk.HORIZONTAL, command=self.update_date_label)
        self.date_slider.grid(row=1, column=1)
        self.update_date_label()
        tk.Label(self.root, text=f"today: {self.selected_date}").grid(row=1, column=2)

        tk.Label(self.root, text="Available Cities:").grid(row=2, column=0)
        self.city_combo = ttk.Combobox(self.root, values=["New York","barcelona", "Los Angeles", "London", "Paris", "Tokyo"])
        self.city_combo.grid(row=2, column=1)

        tk.Button(self.root, text="Search Flights by Date", command=self.search_flights_by_date).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text="Search Flights by City", command=self.search_flights_by_city).grid(row=4, column=0, columnspan=2)

        self.flight_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.flight_listbox.grid(row=5, column=0, columnspan=2)

        tk.Button(self.root, text="Select seat(s)", command=self.select_seat).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Book Flight(s)", command=self.book_flights).grid(row=7, column=0, columnspan=2)

        self.service_vars = []
        for service in self.services:
            var = tk.BooleanVar()
            tk.Checkbutton(self.root, text=f"{service.name} (${service.price})", variable=var).grid(row=8, column=self.services.index(service))
            self.service_vars.append(var)


    def update_date_label(self, value=None):
        date_index = self.date_slider.get()
        base_date = datetime(2024, 9, 5)
        selected_date = base_date + timedelta(days=date_index)
        self.selected_date = selected_date.strftime('%Y-%m-%d')
        

    def search_flights_by_date(self):
        self.flight_listbox.delete(0, tk.END)
        for flight in self.available_flights:
            if flight.date == self.selected_date:
                self.flight_listbox.insert(tk.END, f"{flight.flight_number} - {flight.airline} - {flight.departure} to {flight.arrival} - Price: ${flight.price} - Date: {flight.date}")

    def search_flights_by_city(self):
        self.flight_listbox.delete(0, tk.END)
        selected_city = self.city_combo.get()
        if selected_city:
            for flight in self.available_flights:
                if flight.departure == selected_city or flight.arrival == selected_city:
                    self.flight_listbox.insert(tk.END, f"{flight.flight_number} - {flight.airline} - {flight.departure} to {flight.arrival} - Price: ${flight.price} - Date: {flight.date}")

    def select_seat(self):
        selected_indices = self.flight_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "No flight selected.")
            return
        
        for index in selected_indices:
            flight_info = self.flight_listbox.get(index)
            flight_number = flight_info.split(' - ')[0]
            flight = next((f for f in self.available_flights if f.flight_number == flight_number), None)
            if flight:
                self.open_seat_selection_window(flight)
            else:
                messagebox.showerror("Error", f"Flight {flight_number} not found.")

    def open_seat_selection_window(self, flight):
        seat_window = tk.Toplevel(self.root)
        seat_window.title(f"Select Seat for Flight {flight.flight_number}")

        tk.Label(seat_window, text=f"Flight: {flight.flight_number} - {flight.airline}").pack()

        for row in range(len(flight.seats)):
            row_frame = tk.Frame(seat_window)
            row_frame.pack()
            for col in range(len(flight.seats[row])):
                seat_button = tk.Button(row_frame, text=f"Row {row+1} Col {col+1}",
                                    command=lambda r=row, c=col, win=seat_window: self.book_seat(flight, r, c, win))
                seat_button.pack(side=tk.LEFT, padx=2, pady=2)

    def book_seat(self, flight, row, col, window=None):
        if flight.select_seat(row, col):
            messagebox.showinfo("Success", f"Seat {row+1}-{col+1} booked on flight {flight.flight_number}.")
            if window:
                window.destroy()
                self.selected_seats.append(flight)  # Add the booked flight to selected seats
        else:
            messagebox.showerror("Error", "Seat is already booked. Please choose another seat.")

    def book_flights(self):
        if not self.customer_name.get():
            messagebox.showerror("Error", "Customer name is required.")
            return

        if not self.selected_seats:
            messagebox.showerror("Error", "No flights selected.")
            return

        booking = Booking(self.customer_name.get())
        for flight in self.selected_seats:
            if flight.booked_seats:
                seat_row, seat_col = flight.booked_seats[-1]
                # Recalculate price for each selected flight
                booked_price = advanced_dynamic_pricing(
                    base_price=flight.price,
                    demand_factor=2,
                    booking_time=datetime.now(),
                    historical_data=self.historical_data,
                    user_behavior=self.user_behavior
                )
                flight.price = booked_price
                try:
                    booking.add_flight(flight, seat_row, seat_col)
                except Exception as e:
                    messagebox.showerror("Booking Error", str(e))
                    return

        for i, var in enumerate(self.service_vars):
            if var.get():
                booking.add_service(self.services[i])

        itinerary = booking.generate_itinerary()
        self.display_booking_summary(itinerary)



    def display_booking_summary(self, itinerary):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Booking Summary")

        tk.Label(summary_window, text="Booking Complete!", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(summary_window, text="Itinerary:").grid(row=1, column=0, sticky=tk.W)
        itinerary_text = tk.Text(summary_window, wrap=tk.WORD, height=12, width=72)
        itinerary_text.grid(row=2, column=0, columnspan=2)
        itinerary_text.insert(tk.END, itinerary)
        itinerary_text.config(state=tk.DISABLED)

        tk.Button(summary_window, text="Close", command=summary_window.destroy).grid(row=3, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingApp(root)
    root.mainloop()
