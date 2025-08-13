# FitNet
Term 3 Year 10 Assessment Web Application Task

## Project Description - FitNet
Fitnet is a mobile app designed to help users build consistent gym habits by combining intuitive workout tracking with a motivational streak system. Inspired by the popular study app Yeolpumta (YPT), this fitness-focused tracker uses time logging, daily streaks, and personal goal setting to encourage commitment and discipline in training routines.

### Requirements
| **Functional** | **Non-Functional** |
| ----------- | ----------- |
| **Workout Timer Functionality**: The app shall allow users to start, pause, and stop a workout timer to record the duration of each session. | **Performance**: The app should respond to user inputs within 1 second and load logs and history within 3 seconds on average devices.|
| **Exercise Logging System**: Users shall be able to log exercises with details such as name, sets, reps, weight, and optional notes. | **Usability**: The user interface must be intuitive and user-friendly, requiring no more than 5 minutes for a new user to understand the core features.|
| **Login System**: The app shall allow users to create an account, log in securely using email/password or third-party authentication, and access their personal workout data. This allows users to create their own profile and add their friends to work along them. | **Aesthetics**: The app shall feature a clean, modern, and visually engaging interface with a dark and light mode, using a consistent colour scheme and minimalistic design to enhance user experience. |
| **Custom Workout Plans**: Allow users to create and save custom workout routines (e.g. “Push Day”, “Leg Day”) and load them quickly for repeated use. | **Reliability** The app should function consistently with no major crashes and preserve user data even after unexpected shutdowns or loss of internet connection. |

### Bonus Content
1. **Streak Tracking**
The app shall track the number of consecutive days a user logs a workout and display their current streak on the home screen.

2. **Rest Timer / Interval Alerts**
Add a built-in rest timer with vibration/sound alerts between sets, useful for circuit training or timed workouts.

3. **Body Progress Tracking**
Let users log body weight, measurements, or upload progress photos over time, visualised through graphs or a photo timeline.

4. **Motivational Quotes / Reminders**
Display daily motivational fitness quotes or custom reminders (e.g. “Leg day today!”) to boost user consistency.

5. **Voice Input & Control**
Add voice command functionality like “Start workout”, “Log 10 push-ups” or “End session”.

6. **Music Integration**
Connect with Spotify or Apple Music so users can control their workout playlist without leaving the app.

7. **Social Leaderboards**
Introduce a friend system with leaderboards based on total time, streaks, or workout days—like Yeolpumta’s rankings.

8. **Achievement Badges**
Reward users with badges for milestones like “7-day streak”, “First 100 reps logged”, or “First custom plan created”.

9. **Offline Mode**
Allow users to log workouts and use timers even without internet access, syncing when back online.

10. **Exercise Library**
Include an in-app library of exercises with animations or short videos showing proper form for each exercise.

## App Design 1 - Laptop Layout
### Page 1 - Home Dashboard
![Wireframe Home Dashboard](https://github.com/user-attachments/assets/344f153d-2088-40a7-8999-666416251fbb)
### Page 2 - Log Workout
![Wireframe Log Workout](https://github.com/user-attachments/assets/44773b05-27b0-45ef-a22b-b2fea60974ee)
### Page 3 - Progress
![Wireframe Progress](https://github.com/user-attachments/assets/f0317bb5-dd9b-484b-a1e6-a996f1efe2c4)

### Best Practice Principles
1. **Visual Consistency**
   - **Navigation Bar:** The top navigation bar (Dashboard, Log Workout, Progress, Profile, Logout) is consistent across all screens in location, style, and layout.

    - **Card Layouts:** Statistic boxes (e.g., “Daily Streak,” “This Week,” “Total Time”) share the same border style, spacing, and font.

    - **Buttons:** Action buttons like Start Workout Timer, Schedule Workout, Save Workout, and Add Goal use a consistent rectangular shape and label style.

2. **Functional Consistency**
    - **Navigation:** Tabs work identically on all pages (clicking always takes the user to the intended section).

    - **Workout Logging:** The process of adding exercises, starting timers, and saving workouts is the same every time.

    - **Progress Display:** Graphs and progress bars follow the same format whether viewing weekly workouts, strength progress, or monthly overview.

3. **Internal Consistency**
    - **Layout Structure:** Across pages, navigation stays at the top, main content in the centre, and action buttons near the relevant sections.

    - **Terminology:** Terms like Workout, Goal, and Timer are used consistently, reducing user confusion.

    - **Interaction Patterns:** Dropdowns, input fields, and progress bars behave in the same way across different screens.

4. **External Consistency**
    - The app follows **common fitness tracker patterns** found in apps like Strava, MyFitnessPal, and Fitbit:
      - Dashboard summarises stats at a glance.
      - Progress page uses graphs and goal trackers.
      - Workout logging has a timer and exercise entry fields.
    - Users familiar with other fitness apps will find the interface intuitive.

5. **Aesthetic Consistency**
    - Elements are aligned and evenly spaced, maintaining a **balanced visual hierarchy.**

    - **Grouped sections** reduce visual clutter and make information scannable.

    - Icons, headings, and text follow a **predictable placement pattern** for ease of navigation.

## App Design 2 - Mobile Layout

### Page 1 and 2 - Home Dashboard and Log Workout
<img width="1474" height="1061" alt="image" src="https://github.com/user-attachments/assets/0089c94d-3f1c-4cfa-9f49-ed5559452c63" />

### Page 3 - Progress
<img width="987" height="1104" alt="image" src="https://github.com/user-attachments/assets/78cf0ae4-6e8e-4921-a7d4-fb822883dfff" />

### Best Practice Principles

1. **Visual Consistency**
    - **Navigation & Layout:** Logo, hamburger menu, and section structure are in the same position on every screen.

    - **Cards & Buttons:** Stats and action buttons share the same rounded rectangle style, spacing, and size.

    - **Colours:**
        - Black Background [000000] to make UI Elements pop out

        - Primary blue [0F52FF] background for main UI elements.

        - White text [FFFFFF] for readability.

        - Greyish-blue [BEBFCB] for text input to add consistency

        - Red (cardio) and green (stretch) 
        accents for workout types.\

        Overall tone is blue, allowing for consistency and blend throughout the whole design. Maintaining a minimalisitic structure and look.

    - **Fonts:** Bold Roboto for headings, lighter Roboto for body text. Consistent and minimalistic.

2. **Functional Consitency**
    - Menu works the same on all screens. 

    - Workout logging always follows the same flow: choose type → enter sets/reps/weight → save.

    - Graphs use the same interaction style and labelling.

3. **Internal Consistency**
- Screen layout order is always: stats → current session/graph → goals.

- Repeated terminology (Workout Type, Current Session, Fitness Goals).

- Inputs and dropdowns have identical styling.

4. **External Consistency**
- **Familiar fitness app patterns:** stat cards, graphs, and floating “+” button. Easy for users of apps like Fitbit or Strava to understand.

5. **Aesthetic Consistency**
- Blue as the primary colour, with accents only for workout categories.

- Same font sizes and weights for headings, labels, and body text.

- Matching icon style across all screens.



## Algorithm Design

### Pseudocode (Login Page)
**START**
1. Display Login Page with:
    - Email input field
    - Password input field
    - "Login" button
    - Branding/Logo
2. IF "Login" button clicked:\
    2.1. Retrieve email and password input.
3. IF Email or Password is empty:\
    3.1. Display "Please fill in all fields"\
    3.2. RETURN to Step 2.
4. IF Email format is invalid:\
    4.1. Display "Invalid email address"\
    4.2. RETURN to Step 2.
5. Authenticate user credentials with database.\
    5.1. IF authentication fails:\
        5.1.1. Display "Invalid email or password"\
        5.1.2. RETURN to Step 2.\
    5.2. IF authentication succeeds:\
        5.2.1. Redirect to Dashboard Page.

**END**

### Pseudocode (Global Components - Hamburger Menu)
**START**
1. Display hamburger icon in top right corner.
2. IF hamburger icon clicked:\
    2.1. Display dropdown menu with options:\
        - "Dashboard"\
        - "Log Workout"\
        - "Workout History"\
        - "Profile"\
        - "Sign Out"\
        - "Close Application"
3. IF "Dashboard" clicked:\
    3.1. Redirect to Dashboard Page.
4. IF "Log Workout" clicked:\
    4.1. Redirect to Log Workout Page.
5. IF "Workout History" clicked:\
    5.1. Redirect to Workout History Page.
6. IF "Profile" clicked:\
    6.1. Redirect to Profile Page.
7. IF "Sign Out" clicked:\
    7.1. Clear session/authentication token.\
    7.2. Redirect to Login Page.
8. IF "Close Application" clicked:\
    8.1. Prompt "Are you sure you want to close?".\
    8.2. IF confirmed:\
        8.2.1. Close the browser tab or window

**END**

### Pseudocode (Global Components - Quick Workout Overlay)
**START**
1. Display floating "+" button in bottom right corner.
2. IF "+" button clicked:\
    2.1. Display overlay modal with quick workout settings:\
        - Workout type dropdown (e.g., Stretching, Cardio, Strength)\
        - Duration selector (e.g., 10, 20, 30 minutes)\
        - "Start Workout" button
3. IF "Start Workout" clicked:\
    3.1. Redirect to Log Workout Page.\
    3.2. Auto-start workout timer with chosen duration.\
    3.3. Pre-fill workout log with selected workout type and duration.

**END**

### Pseudocode (Home Dashboard)
**START**
1. Verify if session token exists.
2. IF no token:\
    2.1. Redirect to Login Page.
3. Retrieve user's name, streak count, and latest workout summary from database.
4. Display welcome message with name.
5. Display streak counter.
6. Display total time worked out.
6. Display "Start Workout Timer" button.
7. IF "Start Workout Timer" clicked:\
    7.1. Redirect to Log Workout Page\
    7.2. Pass current timestamp as workout start time parameter.

**END**

### Pseudocode (Logging Workout Page)
**START**
1. Display active workout timer (started from Dashboard or Quick Workout overlay).\
    1.1. Show controls: "Pause", "Resume", "Stop".
2. Display exercise logging form:\
    - Exercise name
    - Sets
    - Reps
    - Weight (optional)
    - Notes
    - "Add Exercise" button
3. IF "Add Exercise" clicked:\
    3.1. Save exercise entry to current workout session log.
4. IF "Stop Timer" clicked:\
    4.1. Prompt "Save workout?"\
        4.1.1. IF Yes:\
            4.1.1.1. Save workout data to user account.\
            4.1.1.2. Redirect to Workout History Page.\
        4.1.2. IF No:\
            4.1.2.1. Discard data.\
            4.1.2.2. Redirect to Dashboard.

**END**

### Pseudocode (Workout History Page)
**START**
1. Display list of past workouts with:
    - Date
    - Duration
    - Exercises logged
2. Allow filtering by date range and workout type.
3. IF a workout entry clicked:\
    3.1. Display detailed view with all exercises, sets, and notes.

**END**

### Pseudocode (Progress Page)
**START**
1. Verify if session token exists.
2. IF no token:\
    2.1. Redirect to Login Page.
3. Display page header: "Your Progress" and "Track your fitness journey over time".
4. Display timeframe filter dropdown (e.g., "This Month").
5. Show summary cards with:\
    5.1. Total Workouts (e.g., 47)\
    5.2. Total Time (e.g., 32.5h)\
    5.3. Average Workout Duration (e.g., 42 min)\
    5.4. Personal Best (e.g., 95kg Bench Press)
6. Display data visualization section with tabs:\
    7.1. "Workout Frequency" tab:\
        7.1.1. Show bar chart displaying number of workouts per week/day (like Progress 1).\
    7.2. "Strength Progress" tab:\
        7.2.1. Show line chart tracking strength gains over time (like Progress 2).\
    7.3. "Monthly Overview" tab:\
        7.3.1. Show combined line/bar chart of workouts and performance metrics (like Progress 3).
7. Show "Fitness Goals" card displaying:\
    8.1. Current progress towards weekly workout goal (e.g., 4/5 Workouts).\
    8.2. Personal best target progress (e.g., Bench Press Goal).
8. Allow user to switch timeframe filter to update charts and data accordingly

**END**

### Pseudocode (Profile Page)
**START**
1. Display user profile info:
    - Name
    - Email
    - Age
    - Weight
    - Progress Pictures
    - Fitness goals
2. Allow editing of profile information.
3. IF "Save Changes" clicked:\
    3.1. Validate updated information.\
    3.2. Save changes to database.\
    3.3. Display "Profile updated successfully".

**END**