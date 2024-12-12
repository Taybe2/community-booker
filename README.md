
## Community Booker App
A simplified platform to manage and book time slots for community centers.
# **[Link to Live Site](https://community-booker-app-9f0552b871a8.herokuapp.com/)**  

#### Table of Contents
- [1. Project Overview](#1-project-overview)
- [2. Agile Methodology](#2-agile-methodology)
- [3. Features](#3-features)
- [4. Wireframes](#4-wireframes)
- [5. Entity Relationship Diagram (ERD)](#5-entity-relationship-diagram-erd)
- [6. Technologies Used](#6-technologies-used)
- [7. Installation Instructions](#7-installation-instructions)
- [8. Usage Guide](#8-usage-guide)
- [9. Screenshots](#9-screenshots)
- [10. Testing](#10-testing)
- [11. Deployment](#11-deployment)
- [12. Future Enchancements](#12-future-enchancements)
- [13. Contributing](#12-future-enchancements)
- [14. License](#14-license)
- [15. Credits](#15-credits)

###  1. Project Overview
The Community Booker App simplifies the process of booking and managing community center resources. Designed with user-friendliness and efficiency in mind, it caters to community centers, event organizers, and local residents.

------

### 2. Agile Methodology
In this project, I followed Agile practices to ensure incremental progress and iterative feedback. The development was organized into user stories, and tasks were tracked using a project board.

#### User Stories
Here are some of the key user stories for the project:
- As a **Site User** I can **register an account** so that **I can make a booking**
- As a **logged in user** I can **create a booking** so that **I can reserve a spot for my event**
- As an **admin** I can **create, update, and delete time slots for my community center** so that **users can book them**
- As a **user** I can **see all available time slots for the community center** so that **I can choose a convenient time to book**
- As a **logged in user** I can **view a list of my bookings** so that **I can keep track of the times I have reserved for the community center**
- As a **logged in user** I can **edit an upcoming booking** so that **I can update the occasion or reschedule to a different time slot**
- As a **logged in user** I can **cancel an upcoming booking** so that **the time slot becomes available for others**

#### Project Board
All the tasks, user stories, and issues were tracked on the project board. You can check out the project board for the latest updates and progress:

[Link to Project Board](https://github.com/users/Taybe2/projects/5/views/1)

------

### 3. Features
- **User Autentication:** Users can register, log in, reset their password, and manage their bookings, including checking past or upcoming bookings and editing or deleting them.
- **Booking System:** Allows users to view available time slots and book them instantly.
- **Admin Panel:** Django's built-in admin panel allows community center admins to manage bookings, update center details, and generate time slots.
- **Homepage:** Features a hero image with call-to-action button for quick access to Available Time Slots and Community Centre Details.
- **My Bookings Page:** Users can view, edit, or cancel their bookings.
- **Resposive Design:** Optimized for both desktop and mobile devices.

##### [ Back to Top ](#table-of-contents)

------
### 4. Wireframes
The wireframes below illustrate the initial design concepts for the Community Booker App, highlighting the layout and navigation flow of key pages such as the homepage, booking page, and user booking management pages.

#### Key Screens

- **Homepage:** Features a hero image with call-to-action buttons for quick access to available time slots and community center details.

![Homepage Wireframe](docs/wireframes/pngs/homepage.png)

- **Available Time Slots Page:** Displays the available time slots for booking, organized from tomorrow onward.

![Available Time Slots Wireframe](docs/wireframes/pngs/available_times.png)

- **My Bookings Page:** Allows users to view their bookings, with options to edit or cancel.

![My Bookings Wireframe](docs/wireframes/pngs/my_bookings.png)

- **Confirm Booking Page:** Allows users to provide booking details, such as occasion type and notes, before finalizing their booking.


![Confirm Booking Wireframe](docs/wireframes/pngs/confirm_booking.png)

#### Tools Used
These wireframes were created using Balsamiq, a user-friendly tool for creating low-fidelity wireframes that help visualize and plan application designs.

#### Note on Iterations
The wireframes served as the foundation for the app's UI design. Some elements have been refined during implementation to improve user experience.

##### [ Back to Top ](#table-of-contents)

------

### 5. Entity Relationship Diagram (ERD)
The Entity Relationship Diagram (ERD) outlines the database structure for the Community Booker App, showing how data entities relate to one another.

**ERD Overview:**
- **Users:** Represents authenticated users who can book the community center. The app utilizes Django's built-in User model, which provides essential functionality for handling user authentication, such as registration, login, and password management.
- **Bookings:** Stores details of each booking made by users.
- **CommunityCentre:** Holds information about the community center, such as name, address,featured image and operating hours.
- **TimeSlots:** Represents the available time slots at the community center for booking, including the start and end time for each slot.

Below is the Entity Relationship Diagram (ERD) that shows the structure of the database:

![ERD Diagram](docs/images/erd-diagram.png)

##### [ Back to Top ](#table-of-contents)

------

### 6. Technologies Used
- **Back-end:** Django 4.x, Python 3.x
- **Front End:** HTML5, CSS3, JavaScript
- **database:** SQLite (for development), PostgreSQL (for production)
- **Hosting:** Heroku
- **Media Storage:** Cloudinary
- **Tools:** Bootstrap, Django Crispy Forms

##### [ Back to Top ](#table-of-contents)

------

### 7. Installation Instructions
  1. Clone the repository:
  ```bash
  git clone https://github.com/Taybe2/community-booker.git
  cd community-booker
  ```
  2. Create a virtual environment and activate it:
  ```bash
  python -m venv env
  source env/bin/activate  # On Windows: env\Scripts\activate
  ```
  3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  4. Apply migrations:
  ```bash
  python manage.py migrate
  ```
  5. Create a superuser for admin access:
  ```bash
  python manage.py createsuperuser
  ```
  6. Run the development server:
  ```bash
  python manage.py runserver
  ```

##### [ Back to Top ](#table-of-contents)

------

### 8. Usage Guide
This guide provides step-by-step instructions on how to use the Community Booker App effectively.
  
  #### 1. Accessing the Application
  - Open your browser and navigate to the app’s URL: <a href="https://community-booker-app-9f0552b871a8.herokuapp.com/" target="_blank">Community Booker App</a>
  - You’ll be greeted with the homepage featuring a hero image and call-to-action button for quick navigation.
  - You will also see the Community Centre's details, including its address, opening hours, and operating days.
  
  #### 2. Registering an Account
  - Click on the Sign Up link in the navigation menu.
  - Fill out the registration form with your details (e.g., username, email, password).
  - Submit the form to create your account.
  - After registering, you can log in using your credentials.

  #### 3. Logging In
  - Click on the Log In link in the navigation menu.
  - Enter your username and password.
  - Click Sign In to access the My Bookings page, where you can view your bookings or make a new one.

  #### 4. Viewing Available Time Slots
  - Click on the Available Time Slots link in the navigation menu.
  - View the available time slots, starting from tomorrow, organized by date and time.
  - Use the Next 10 Days or Previous 10 Days buttons to navigate between dates.
  - To book a slot, you must first log in or register.

  #### 5. Making a Booking
  - Go to the Available Time Slots page and browse the available slots.
  - Select an available time slot by clicking on it.
  - Click the Book Selected Time Slot button to go to the booking page.
  - Fill in the booking details, including: Occassion, Occasion Type(Private/Public) and Notes(optional)
  - Choose whether you want your booking to be Public (viewable by others) or Private (not viewable by others).
  - After filling in all the details, click Confirm Booking to complete the booking process.

  #### 6. Managing Your Booking
  - Navigate to the "My Bookings" page from the navigation menu.
  - View all your bookings categorized as Upcoming or Past.
  - For **Upcoming Bookings**:
    - Edit the booking details using the Edit Booking button.
    - Cancel a booking using the Cancel Booking button.
  
  #### 7. Editing an Upcoming Booking
  - Navigate to the My Bookings page from the navigation menu.
  - Find the booking you want to edit.
  - Click the Edit button next to the booking.
  - Modify the details of your booking, such as the occasion name, type, or notes.
  - To change the time and/or date of your booking, click the Change Time Slot link.
  - You will be navigated to the Choose a Different Time Slot (Reschedule) page, where you can select a new time slot for your booking.
  - Once you've made the changes, click Save Changes to update your booking.

####  8. Logging Out
  - Click on the "Logged in as [username]" text in the navigation menu
  - A dropdown menu will appear with the option "Logout".
  - Click "Logout" to be redirected to the Sign Out page.
  - On the Sign Out page, you will be asked if you're sure you want to sign out.
  - Click the "Sign Out" button to complete the logout process.

##### [ Back to Top ](#table-of-contents)

------

### 9. Screenshots

------

### 10. Testing
#### 1. HTML Validation:  
  I used the [W3 HTML Validator](https://validator.w3.org/#validate_by_input+with_options) to check the HTML across my site, with most pages passing without errors. Issues were identified on a few pages, including unnecessary attributes and minor accessibility warnings, all of which were resolved, except for unclosed HTML tags in the Django Allauth templates on the Register Page, which I deferred fixing due to time constraints.

#### 2. CSS Validation:  
  I used the [W3 CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input) to check the styles.css file, and no errors were found. A warning about identical ``background-color`` and ``border-color`` in a specific selector was resolved by changing the ``border-color`` to ``transparent``.  
  ![CSS validation results](/docs/images/W3C_CSS.png)

#### 3. PEP8 Compliance Check:
  I used the [CI Python Linter](https://pep8ci.herokuapp.com/) to ensure my Python code follows the PEP8 style guide for readability and consistency. The linter flagged issues like line length, improper indentation, and missing or extra whitespace, which I reviewed and corrected across all files. After making the necessary adjustments, the code now complies with PEP8 standards.

  However, in some cases, like the following test assertion:

  ```python
  self.assertTrue(
      any("You are not authorized to edit this booking." in str(msg) for msg in messages),
      "Expected 'You are not authorized' message not found"
  )
  ```

  I couldn't shorten the line further while keeping the logic clear and readable. It checks whether the expected message exists in the list of messages, which requires iterating over the list, making it difficult to reduce the line length without sacrificing clarity.

#### 5. Manual Testing:

| **Test Case**                                      | **Expected Outcome** | **Result** |
|----------------------------------------------------|----------------------|------------|
| **1.1 Register a New User**                        | User registered       | Pass       |
| **1.2 Login**                                      | User logged in        | Pass       |
| **1.3 Logout**                                     | User logged out       | Pass       |
| **2.1 View Available Time Slots**                  | Time slots displayed  | Pass       |
| **2.2 Create a Booking**                           | Booking created       | Pass       |
| **2.3 Edit a Booking**                             | Booking updated       | Pass       |
| **2.4 Cancel a Booking**                           | Booking cancelled     | Pass       |
| **3.1 Generate Time Slots**                        | Slots generated       | Pass       |
| **3.2 Manage Bookings**                            | Bookings managed      | Pass       |
| **4.1 Accessing Restricted Pages**                 | Redirected to login   | Pass       |
| **4.2 Invalid Booking Creation**                   | Error displayed       | Pass       |
| **4.3 Accessing the Create Booking Page for an Already Booked Time Slot** | Redirected            | Pass       |
| **5.1 Accessing Another User's Booking**           | Access denied         | Pass       |
| **5.2 Choosing a Time Slot for a Booking Made by Another User** | Access denied         | Pass       |
| **5.3 Accessing Generate Time Slots Page Without Admin Privileges** | Access denied         | Pass       |
| **5.4 Accessing Admin Pages**                      | Access denied         | Pass       |
| **5.5 Navigation Bar**                             | Links functional      | Pass       |
| **5.6 Responsive Design**                          | UI adjusted           | Pass       |


#### 5. Django Automated Testing:  
  In addition to the above tools, I also utilized the Django automated testing within my Gitpod workspace to ensure the functionality and stability of the application.

For detailed information about testing, refer to the [TESTING.md](./TESTING.md) file.

------

### 11. Deployment
The Community Booker app is hosted on Heroku. Below are the steps to deploy it using the Heroku Dashboard:

**Prerequisites**
1. Ensure you have a Heroku account.
2. Make sure your project code is pushed to a GitHub repository.

**Steps to Deploy via Heroku Dashboard**
1. Log In to Heroku
    - Navigate to Heroku and log in to your account.
2. Create a New Heroku App
    - Click the New button in the top-right corner of the dashboard.
    - Select Create new app.
    - Provide a unique name for your app (e.g., community-booker) and choose your region.
    - Click Create app.
3. Connect the App to GitHub
    - On the app’s dashboard, go to the Deploy tab.
    - In the Deployment Method section, select GitHub.
    - In the Config Vars section, click Reveal Config Vars.
    - Add the required environment variables, such as:
      ```
      SECRET_KEY=<your-secret-key>
      DATABASE_URL=<your-database-url>
      CLOUDINARY_URL=<your-cloudinary-url>
      ```
    - If DISABLE_COLLECTSTATIC=1 was previously added, delete it once your static files are correctly configured. This will allow Heroku to run collectstatic during deployment.
4. Manual Deployment
    - If you want to deploy manually, scroll to the Manual Deploy section on the Deploy tab.
    - Choose the branch you want to deploy (e.g., main) and click Deploy Branch.
    - Wait for Heroku to build and deploy your app.
5. Access Your Deployed App
    - Once the deployment is complete, you will see a confirmation message with a link to your app.
    - Click the link to access your app in the browser.

**Notes**
  - Make sure DEBUG in settings.py is set to False for production.

##### [ Back to Top ](#table-of-contents)

------

### 12. Future Enchancements
#### 1. Multiple Community Centers Support
  Allow the app to support multiple community centers, where each center can have its own settings, time slots, and bookings. This will allow the platform to be used by various community centers, making it more scalable.

#### 2. Recurring Bookings
  Add support for recurring bookings, where users can book a time slot on a weekly, monthly, or custom repeating schedule.

#### 3. Payment Integration
  Add support for online payments for bookings (if applicable), allowing users to pay for their booking directly through the app.

#### 4. Admin Booking Approval
  Introduce a booking approval system where admins must review and approve or reject bookings before they are finalized. This ensures better control over the scheduling process and prevents conflicts or unauthorized bookings.

##### [ Back to Top ](#table-of-contents)

------

### 13. Contributing

Contributions are welcome! To get started:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes.
4. Commit your changes.
5. Push to your fork and create a pull request.

Thank you for your contributions!

##### [ Back to Top ](#table-of-contents)

------

### 14. License

------

### 15. Credits

This project makes use of the following open-source libraries and tools:

- **Django** - The web framework used to build the app.
- **Bootstrap** - A front-end framework for building responsive, mobile-first websites.
- **PostgreSQL** - The database used to store project data.
- **Cloudinary** - Used for image hosting and management.
- **pytest** - Testing framework used for unit tests.

The photo in the homepage welcome section was sourced from **Pixabay**, created by **This_is_Engineering**.

A special thanks to the developers and contributors of these libraries for their hard work and contributions.

#### Inspiration
- Inspired by [Lavender Hair Design](https://www.phorest.com/salon/lavenderhairdesign) for the layout idea of the Available Time Slots Page.
- Based on the Django Blog Project tutorial by Niel McEwen for Django best practices.

#### Acknowledgements
- Special thanks to my mentors for their support and guidance.

##### [ Back to Top ](#table-of-contents)