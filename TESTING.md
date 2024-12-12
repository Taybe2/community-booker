# Testing Documentation

This document outlines the testing process for the Community Booker App, including manual testing, automated tests, and validation checks to ensure the application meets user and technical requirements.

## Manual Testing
This section outlines the manual testing process for the Community Centre Booking App, ensuring all features function as expected. Each section provides test cases for various functionalities, the steps to test them, the expected outcomes, and the results.

### 1. User Authentication

#### 1.1 Register a New User

- **Steps:**
  1. Navigate to the registration page.
  2. Fill in the registration form with valid details (username, email, password).
  3. Submit the form.
- **Expected Outcome:** The user is registered, logged in with their new account and a confirmation message is displayed.
- **Result:** Pass

#### 1.2 Login

- **Steps:**
  1. Navigate to the login page.
  2. Enter valid credentials and submit.
- **Expected Outcome:**  A confirmation message is displayed and the user is redirected to the homepage.
- **Result:** Pass

#### 1.3 Logout

- **Steps:**
  1. Click the logout button from the navigation menu.
- **Expected Outcome:** The user is logged out and redirected to the homepage, , a confirmation message is displayed.
- **Result:** Pass

---

### 2. Booking Management

#### 2.1 View Available Time Slots

- **Steps:**
  1. Navigate to the "Available Time Slots" page.
  2. Verify that time slots starting from tomorrow are displayed.
- **Expected Outcome:** Time slots are displayed, grouped by day, with available and booked slots clearly marked.
- **Result:** Pass

#### 2.2 Create a Booking

- **Steps:**
  1. Select an available time slot.
  2. Click the "Book Selected Time Slot" button.
  3. Fill out the booking form and submit.
- **Expected Outcome:** The booking is successfully created, a confirmation message is displayed, and the user is redirected to the "My Bookings" page.
- **Result:** Pass

#### 2.3 Edit a Booking

- **Steps:**
  1. Navigate to the "My Bookings" page.
  2. Select an upcoming booking and click "Edit".
  3. Change the booking details and save.
- **Expected Outcome:** The booking is updated successfully and a confirmation message is displayed.
- **Result:** Pass

#### 2.4 Cancel a Booking

- **Steps:**
  1. Navigate to the "My Bookings" page.
  2. Select an upcoming booking and click "Cancel".
  3. Confirm cancellation.
- **Expected Outcome:** The booking is removed from the list, and a success message is displayed.
- **Result:** Pass

---

### 3. Admin Functionality

#### 3.1 Generate Time Slots

- **Steps:**
  1. Log in as a staff member.
  2. Navigate to the "Generate Time Slots" page.
  3. Enter a valid date range and submit.
- **Expected Outcome:** Time slots are generated for the specified date range.
- **Result:** Pass

#### 3.2 Manage Bookings

- **Steps:**
  1. Log in as a staff member.
  2. Navigate to the admin panel.
  3. View, edit, or delete bookings.
- **Expected Outcome:** Bookings are managed successfully.
- **Result:** Pass

---

### 4. Error Handling

#### 4.1 Accessing Restricted Pages

- **Steps:**
  1. Attempt to access a booking or admin page without logging in.
- **Expected Outcome:** The user is redirected to the login page with an appropriate message.
- **Result:** Pass

#### 4.2 Invalid Booking Creation

- **Steps:**
  1. Attempt to create a booking for a past time slot by manipulating the URL (e.g., by using an ID smaller than those of today's time slots).
- **Expected Outcome:** An error message is displayed, user is redirected to time slots page and the booking is not created.
- **Result:** Pass

#### 4.3 Booking Creation for Non-Existing Time Slot

- **Steps:**
  1. Attempt to create a booking for a non-existent time slot by manipulating the URL (e.g., by using an ID that doesn't exist).
- **Expected Outcome:** An error message is displayed, user is redirected to time slots page and the booking is not created.
- **Result:** Pass

#### 4.4 Accessing the Create Booking Page for an Already Booked Time Slot

- **Scenario:** A user tries to access the **Create Booking** page for a time slot that has already been booked.

- **Steps:**
  1. Ensure a time slot is already booked.
  2. Attempt to access the **Create Booking** page directly via the URL (e.g., `/bookings/create/<booked_time_slot_id>`).

- **Expected Outcome:** 
  - The user is redirected to the **Available Time Slots** page.
  - A message is displayed indicating that the time slot is already reserved.

- **Result:** [Pass]

#### 4.5 Accessing the Edit Booking Page for a Non-existent Time Slot

- **Scenario:** A user tries to access the **Edit Booking** page with a new time slot that doesn't exist.

- **Steps:**
  1. Ensure a time slot doesn't exist.
  2. Attempt to access the **Edit Booking** page directly via the URL (e.g., `/bookings/<booking_slug>/edit/<non_existent_time_slot_id>`).

- **Expected Outcome:** 
  - The user is redirected to the **Available Time Slots** page.
  - A message is displayed indicating that the time slot doesn't exist.

- **Result:** [Pass]

#### 4.5 Accessing the Edit Booking Page for Already Booked Time Slot

- **Scenario:** A user tries to access the **Edit Booking** page with a new time slot that is booked for another occasion.

- **Steps:**
  1. Ensure a time slot is booked for another event.
  2. Attempt to access the **Edit Booking** page directly via the URL (e.g., `/bookings/<booking_slug>/edit/<booked_time_slot_id>`).

- **Expected Outcome:** 
  - The user is redirected to the **Available Time Slots** page.
  - A message is displayed indicating that the time slot is already booked for another event.

- **Result:** [Pass]

---

### 5. Accessing Other Users' Data

#### **5.1 Accessing Another User's Booking**

- **Scenario:** A user tries to access a booking belonging to another user.
- **Steps:**
  1. Log in as User A.
  2. Attempt to view, edit, or cancel a booking belonging to User B by manipulating the URL (e.g., by using another booking's slug).
- **Expected Outcome:** Access is denied, and the user is redirected to a safe page (e.g., "Home" or "My Bookings") with an error message such as "You are not authorized to access this booking."
- **Result:** [Pass]

#### **5.2 Choosing a Time Slot for a Booking, made by another user**

- **Scenario:** A user attempts to choose a different Time slot for anoother user's booking.
- **Steps:**
  1. Log in as User A.
  2. Attempt to access User B's private booking details via the "Available Time Slots".
- **Expected Outcome:**  Access is denied, and the user is redirected to a safe page (e.g., "Home" or "My Bookings") with an error message such as "You are not authorized to edit this booking."
- **Result:** [Pass]

#### **5.3 Accessing Generate Time Slots Page Without Admin Privileges**

- **Scenario:** A regular user tries to view generate time slots page intended for admins.
- **Steps:**
  1. Log in as a regular user.
  2. Attempt to access the "Generate Time Slots" page.
- **Expected Outcome:** Access is denied, and the user is asked to login with a different account.
- **Result:** [Pass]

#### **5.4 Non-Admin User Accessing Admin Pages**

- **Scenario:** A non-admin user attempts to access the admin panel or admin-only views.
- **Steps:**
  1. Log in as a non-admin user.
  2. Attempt to access an admin page directly (e.g., `/admin/`).
- **Expected Outcome:**  Access is denied, and the user is asked to login with a different account.
- **Result:** [Pass]

---

### 5. UI and Navigation

#### 5.1 Navigation Bar

- **Steps:**
  1. Test all navigation links for logged-in and logged-out users.
- **Expected Outcome:** Links are functional and redirect to the correct pages.
- **Result:** Pass

#### 5.2 Responsive Design

- **Steps:**
  1. Test the application on various screen sizes and devices.
  2. Resize the browser window to observe the responsive design.
- **Expected Outcome:** The UI adjusts correctly for all tested resolutions.
- **Result:** Pass

---

## Automated Testing

## Automated Testing

Automated testing was implemented to ensure the robustness and reliability of the key features in the Community Centre Booking App. The following test files were created, focusing on forms and views:

### 1. `test_booking_form.py`
- **Purpose:** To verify that the booking form works as expected and validates user inputs correctly.
- **Key Tests:**
  - Validation of required fields.
  - Handling of invalid or missing inputs.
  - Successful form submission with valid data.

### 2. `test_cancel_booking_view.py`
- **Purpose:** To test the cancellation of bookings.
- **Key Tests:**
  - Ensuring only authorized users can cancel their bookings.
  - Verifying that the booking is properly removed upon cancellation.
  - Handling invalid or non-existent bookings gracefully.

### 3. `test_create_booking_view.py`
- **Purpose:** To ensure that the booking creation process works correctly.
- **Key Tests:**
  - Proper rendering of the create booking page.
  - Successful creation of a booking with valid inputs.
  - Prevention of duplicate bookings for the same time slot.
  - Redirection and appropriate messaging for invalid time slots.

### 4. `test_edit_booking_view.py`
- **Purpose:** To test the functionality of editing existing bookings.
- **Key Tests:**
  - Rendering of the edit page with pre-filled data.
  - Successful update of a booking's details.
  - Prevention of changes to non-existent or unauthorized bookings.

### 5. `test_timeslot_view.py`
- **Purpose:** To validate the functionality of viewing available time slots.
- **Key Tests:**
  - Displaying time slots starting from the next day.
  - Differentiating between available and booked slots.
  - Proper handling of edge cases like empty or invalid time slot data.

### Results
All automated tests were executed using the Django testing framework. The test suite passed successfully, indicating that the app's core functionalities are likely to perform as intended under various scenarios.

### Command to Run Tests
To execute the automated test suite, use the following command:  
```bash
python3 manage.py test
```

## Validation Testing
Validation checks for HTML, CSS and Python

### HTML Validation
- **Tool Used:** W3C Validator.

- **Results:**
  
  - **Homepage:** Passed with no errors or warnings.
  
  - **Available Time Slots Page:**
    - **Issue Identified:** The input elements with type="radio" had an unnecessary role="radio", which caused accessibility warnings.
    - **Resolution:** Removed the role="radio" attribute from the input elements, which resolved all accessibility issues for this page.
  
  - **Confirm Booking Page:**
    - **No errors or warnings reported.**
  
  - **My Bookings Page:**
    - **Issue Identified:** 
      1. **Error:** Bad value ``button`` for attribute type on element `a`: Subtype missing.
      2. **Error:** Element `a` is missing required attribute href.
      3. **Error:** The ``aria-controls`` attribute must point to an element in the same document.
      4. **Warning:**  Empty heading.
    - **Resolution:**  
      1. To resolve the error, I removed the ``type="button"`` attribute from the anchor tag. If a button element is needed for behavior, it should be used instead of an anchor tag.
      2. To fix this error, I added a ``href="#"`` attribute to the anchor tag, because the link was intended for JavaScript functionality.  This placeholder ensures the anchor tag is valid while still performing the desired JavaScript action.
      3. To resolve this, I added the appropriate element IDs to ensure that the ``aria-controls`` attribute references an existing element within the same document.
      4. To resolve the warning, I added a heading with text content. Additionally, if dynamic content needs to be added to the heading, I used JavaScript to append the remainder of the content to the heading.
  
  - **Edit Booking Page:**
    - **Issue Identified:** Error: Bad value submit for attribute type on element a: Subtype missing
    - **Resolution:** To resolve the error, I removed the ``type="submit"`` attribute from the ``<a>`` tag, as anchor elements do not support the type attribute. If the element was intended to behave like a submit button, it should be replaced with a ``<button>`` tag instead.

  - **Log Out Page:**
    - **No errors or warnings reported.**
  
  - **Log In Page:**
    - **No errors or warnings reported.**
  

  - **Register Page:**
    - Observed unclosed HTML tags in the template generated by Django Allauth.
    - Root Cause: The default Allauth templates use unclosed tags.
    - Resolution: Documented the issue but deferred fixing due to time constraints. Will address in future.


### CSS Validation
- **Tool Used:** W3C CSS Validator (https://jigsaw.w3.org/css-validator/).

- **Results:**
  - **Stylesheet:** styles.css
  - **Outcome:** No errors. Warning regarding same color for `background-color` and `border-color` in the `.btn-check:checked + .btn-timeslot` selector.
- **Actions Taken:** Replaced the `border-color` with `transparent` to avoid having the same color for both properties.

### PEP8 Compliance Check

**Objective:**  
To ensure that the Python code adheres to the PEP8 style guide, which promotes readability and consistency in Python code.

**Method:**  
I manually checked all Python files in the project using the CI Python Linter. The linter flagged any deviations from PEP8 standards, such as improper indentation, excessive line length, missing/extra whitespace.

**Actions Taken:**  
- Reviewed each Python file individually through the CI Python Linter.
- Corrected all flagged issues, including:
  - Lines exceeding 79 characters.
  - Missing or extra whitespace.
  - Improper indentation.
  - Any other PEP8-related errors or warnings.

**Result:**  
After thorough review and adjustments, the Python code complies with PEP8 standards as verified by the CI Python Linter, with a few minor exceptions that don't affect functionality.

**Date:** [12/12/2024]