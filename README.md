# Design and OOP Concepts in the Flight Booking System
### 1. Design and Architecture
The flight booking system is designed to facilitate users in booking flights by providing an intuitive interface and robust backend processing. The architecture of the system is modular and follows an object-oriented design paradigm. The main components of the system include:

* **User Interface (UI)**: Built using Tkinter to provide an interactive graphical interface for users to select flights, enter personal details, and choose additional services.
* **Business Logic Layer**: Handles the core functionality of the system including flight search, seat reservation, and user management.
* **Data Storage**: Manages flight data, user information, and booking records. This can be implemented using file storage or a database depending on the system’s complexity.
### 2. Application of OOP Concepts
The system utilizes several Object-Oriented Programming (OOP) concepts to enhance modularity, maintainability, and reusability:

* **Encapsulation**: Each class in the system encapsulates its own data and methods. For example, the Flight class holds details about individual flights, while the User class manages user-related information. This ensures that the data is hidden from external access and can only be manipulated through well-defined interfaces.

* **Inheritance**: The system employs inheritance to extend functionalities. For instance, Flight and Reservation might inherit from a common base class BookingItem which provides shared attributes and methods. This helps in reducing code duplication and fostering a hierarchical structure.

* **Polymorphism**: Through polymorphism, the system allows for different classes to be treated as instances of a common base class. For example, methods in the BookingItem class can be overridden in derived classes like Flight and HotelReservation to provide specific implementations while maintaining a uniform interface.

*  **Abstraction**: Abstraction is applied by defining abstract classes or interfaces that outline common functionalities without specifying the exact implementation. For example, an abstract Service class might define methods like calculateCost and applyDiscount, which are implemented specifically in derived classes like FlightService and MealService.

### 3. Relationships Between Different Classes
The system’s class relationships are designed to reflect real-world interactions and dependencies:

* **Association**: Represents a "using" relationship where classes collaborate. For example, the Booking class associates with the Flight and User classes. A Booking object holds references to Flight and User objects, indicating that a booking is made by a user for a particular flight.

* **Aggregation**: This is a "has-a" relationship where one class contains another but can exist independently. For instance, a User might have a list of Bookings, where each Booking can exist without a specific user, but the User class aggregates multiple bookings.

* **Composition**: Represents a strong "part-of" relationship where components are integral to the whole. For example, a Flight might be composed of FlightSegment objects representing different legs of the journey. The Flight cannot function correctly without its FlightSegments.
