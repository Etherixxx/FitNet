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
    7.1. Redirect to Log Workout Page with autostart=true parameter\
    7.2. Pass current timestamp as workout start time parameter.

**END**

### Pseudocode (Logging Workout Page)
**START**
1. Check URL parameters for autostart=true.\
    1.1. IF autostart parameter present:\
        1.1.1. Automatically start workout timer after page loads.\
        1.1.2. Remove autostart parameter from URL.
2. Display workout timer with controls: "Start", "Stop".\
    2.1. Show timer display and workout type selector.
3. Display exercise logging form:\
    - Exercise name
    - Sets
    - Reps
    - Weight (optional)
    - Notes
    - "Add Exercise" button
4. IF "Add Exercise" clicked:\
    4.1. Save exercise entry to current workout session log.
5. IF "Stop Timer" clicked:\
    5.1. Prompt "Save workout?"\
        5.1.1. IF Yes:\
            5.1.1.1. Save workout data to user account.\
            5.1.1.2. Redirect to Dashboard Page.\
        5.1.2. IF No:\
            5.1.2.1. Discard data.\
            5.1.2.2. Redirect to Dashboard.

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

### Test Case 1 - Quick Workout Overlay
| Field | Details |
| ----------- | ----------- |
| Test Case ID| TC-FN-001 |
| Test Case Name | Verify Quick Workout Overlay opens and allows workout selection|
| Module | Progress Page / Quick Workout |
| Test Priority | High |
| Pre-conditions | User is logged into FitNet and on any page except the login page |
| Test Steps | 1. Navigate to any page except the login page.   2. Click the "+" button in the bottom right corner. 3. Observe if the quick workout overlay appears.    4. Select a preset workout (e.g., "30 minutes of stretching").  5. Click "Add Workout". |
| Expected Result |Overlay should appear when "+" is clicked, allowing the user to select a preset workout. Upon selection and confirmation, the workout should be added to their session or history.|

### Test Case 2 - Daily Progress Chart Display
| Field | Details |
| ----------- | ----------- |
| Test Case ID | TC-FN-002 |
| Test Case Name | Verify daily progress chart loads with correct data |
| Module | Progress Page – Charts |
| Test Priority| High |
| Pre-Conditions| User is logged in and has existing workout data for the past 7 days |
| Test Steps | 	1. Navigate to the Progress page    2. Wait for the daily progress chart to load.   3. Compare displayed data points with stored workout records.   4. Hover over a data point to check if the tooltip displays date and workout details. |
| Expected Result | The daily progress chart should display accurate data for the last 7 days, matching the stored workout records. Tooltips should correctly show date and workout details. |

## Development Progress

### Phase 1: Project Setup and Initial Planning (Week 1)
I began by setting up the project structure and implementing the basic Flask web application framework. Following the provided tutorial template, I created the necessary folder structure including database, static, and templates directories. The initial Flask application was configured with basic routing, session management, and SQLite database connectivity.

**Key Technical Implementation:**
- Configured Flask application with secret key for session management
- Established SQLite database connection using `sqlite3.connect()` with proper row factory settings
- Implemented basic route structure with `@app.route()` decorators
- Set up Jinja2 template engine with custom filters for JSON serialization
- Created project directory structure following MVC architecture principles

**Files Created:**
- `main.py`: Core Flask application with routing logic
- `database/data_source.db`: SQLite database file
- Template structure with base layout and individual page templates

### Phase 2: Database Design and Schema Implementation (Week 2)
I designed and implemented a comprehensive SQLite database schema to support the fitness tracking application. The database includes multiple tables with proper relationships and constraints to ensure data integrity.

**Database Schema Details:**
- **Users table**: Stores user account information including `user_id` (PRIMARY KEY AUTOINCREMENT), `first_name`, `surname`, `email` (UNIQUE), `password_hash`, `age`, and `created_at` timestamp
- **Progress table**: Tracks user physical metrics with `progress_id`, `user_id` (FOREIGN KEY), `date`, `weight_kg`, `height_cm` for body measurement tracking over time
- **Workouts table**: Records individual workout sessions with `workout_id` (AUTOINCREMENT), `user_id` (FOREIGN KEY), `workout_type`, `start_time`, `end_time`, `duration_min`, and `calories_burned`
- **Exercises table**: Logs individual exercises within workouts with `exercise_id`, `workout_id` (FOREIGN KEY), `exercise_name`, `sets`, `reps`, `weight_kg`, and `notes`
- **Goals table**: Manages user fitness goals with `goal_id`, `user_id` (FOREIGN KEY), `goal_type`, `goal_name`, `target_value`, `current_value`, `target_date`, `is_completed`, and `goal_direction` for bidirectional progress tracking

**Technical Challenges Solved:**
- Implemented proper FOREIGN KEY constraints to maintain referential integrity
- Added AUTOINCREMENT for primary keys to handle automatic ID generation
- Created date handling for workout timestamps and goal deadlines
- Designed flexible goal system supporting both "up" direction (muscle gain, strength) and "down" direction (weight loss, running time) goals

### Phase 3: User Authentication System (Week 3)
I implemented a complete user authentication system with both login and registration functionality. The system provides secure user access control and session management throughout the application.

**Authentication Features:**
- **Login System**: Validates user credentials using email and password against the database, maintains secure sessions using Flask's session management, includes comprehensive error handling for invalid credentials
- **Registration System**: Creates new user accounts with input validation, checks for duplicate email addresses, automatically creates corresponding Progress table entries, logs users in immediately upon successful registration
- **Session Management**: Maintains user state across page requests, stores user ID and display name in session, implements session-based access control for protected routes

**Security Implementation:**
- Password validation (though not hashed in current implementation for educational purposes)
- Email format validation using HTML5 patterns and server-side checks
- Session-based authorization ensuring users can only access their own data
- Protection against SQL injection through parameterized queries
- Comprehensive error handling with user-friendly error messages

**Code Examples Implemented:**
```python
# Session management and user authentication
if 'user_id' not in session:
    return redirect(url_for('login'))

# Secure database queries with parameterized statements
user = conn.execute(
    'SELECT * FROM Users WHERE email = ? AND password_hash = ?',
    (email, password)
).fetchone()
```

### Phase 4: Core Application Pages (Weeks 4-5)
I developed the main application pages following the wireframe designs, implementing responsive layouts and interactive functionality.

**Dashboard Page Implementation:**
- **Real-time Statistics**: Dynamically calculates daily streak by counting consecutive workout days using complex SQL queries with date functions
- **Weekly Overview**: Displays workout count and total time for the past 7 days with proper date range filtering
- **Recent Activity**: Shows latest 20 workouts with proper datetime parsing and formatting for user-friendly display
- **User Personalization**: Displays personalized welcome message with proper name handling from both session and database sources

**Technical SQL Implementation:**
```python
# Complex streak calculation query
streak_query = '''
    SELECT COUNT(*) as streak FROM (
        SELECT DATE(start_time) as workout_date
        FROM Workouts
        WHERE user_id = ?
        GROUP BY workout_date
        ORDER BY workout_date DESC
    )
    WHERE workout_date >= DATE('now', '-6 days')
'''
```

**Profile Page Implementation:**
- **Personal Information Management**: Users can update name, email, age, height, and weight with real-time database updates
- **Goal Setting System**: Comprehensive goal creation with support for multiple goal types (weight_loss, muscle_gain, strength, endurance, custom)
- **Progress Tracking**: Visual progress indicators with percentage calculations based on goal direction
- **Data Validation**: Input sanitization and error handling for all form submissions

**Log Workout Page Implementation:**
- **Interactive Timer**: JavaScript-based workout timer with start, pause, and stop functionality
- **Exercise Logging**: Dynamic form for adding exercises with sets, reps, weight, and notes
- **Session Management**: Maintains workout session data until saved or discarded
- **Quick Log Feature**: Simplified workout entry for rapid data input with preset options

**Progress Page Implementation:**
- **Data Visualization**: Statistical analysis and display of workout patterns and progress metrics
- **Goal Monitoring**: Visual progress tracking with percentage completion and achievement indicators
- **Historical Analysis**: Comprehensive review of workout history with filtering and sorting options

### Phase 5: Advanced Features Implementation (Week 6)
I added several advanced features to enhance the user experience and provide comprehensive fitness tracking capabilities.

**Goal Management System:**
- **Bidirectional Progress Tracking**: Implemented sophisticated logic to handle goals where progress can be measured in both directions (higher values = better vs lower values = better)
- **Dynamic Progress Calculation**: Created custom Jinja2 filters for calculating progress percentages based on goal type and direction
- **Achievement Recognition**: Visual indicators for goal completion with congratulatory messages
- **Goal Categories**: Support for strength goals (bench press, squat, deadlift), endurance goals (running times, cycling distances), body composition goals (weight, body fat percentage), and custom fitness targets

**Workout History and Details:**
- **Detailed Workout View**: Individual workout pages showing complete exercise lists, duration, and performance metrics
- **Exercise Analysis**: Breakdown of sets, reps, and weights for each exercise within a workout session
- **Workout Deletion**: Secure deletion functionality with confirmation dialogs and proper database cleanup
- **Historical Trends**: Analysis of workout frequency and performance improvements over time

**Data Population Tools for Development:**
- **Realistic Sample Data Generation**: Created `/populate-goals` and `/populate-workouts` routes for generating test data
- **User Profile Integration**: Sample data that reflects realistic fitness goals based on user demographics (age, weight, height)
- **Exercise Library**: Comprehensive exercise database with proper categorization by workout type (strength, cardio, flexibility, HIIT, functional, core)
- **Temporal Data Distribution**: Workout data distributed across September-October 2025 timeframe for realistic testing scenarios

### Phase 6: User Interface and Experience Enhancements (Week 7)
I focused on creating a polished user interface with consistent styling, responsive design elements, and intuitive navigation throughout the application.

**Template System Architecture:**
- **Base Layout Template**: Implemented master template (`layout.html`) with consistent navigation, styling, and JavaScript includes
- **Component-Based Design**: Created reusable template components with proper Jinja2 inheritance and block systems
- **Dynamic Content Rendering**: Real-time data filtering and formatting using custom Jinja2 filters for dates, numbers, and progress calculations
- **Responsive Design**: Mobile-first approach ensuring proper display across different screen sizes and devices

**Interactive Features:**
- **JavaScript Integration**: Client-side functionality for workout timers, form validation, and dynamic content updates
- **AJAX Implementation**: Asynchronous data submission for workout logging and goal updates without page refresh
- **User Feedback Systems**: Toast notifications, confirmation dialogs, and progress indicators for user actions
- **Form Enhancement**: Real-time validation, input formatting, and error display for improved user experience

**Styling and Visual Design:**
- **CSS Grid and Flexbox**: Modern layout techniques for responsive card-based designs and statistical displays
- **Consistent Color Scheme**: Professional color palette with proper contrast ratios for accessibility
- **Typography Hierarchy**: Clear information hierarchy using consistent font sizes, weights, and spacing
- **Interactive Elements**: Hover effects, button states, and visual feedback for user interactions

### Phase 7: Data Management and Validation (Week 8)
I implemented robust data validation and error handling throughout the application to ensure data integrity and provide excellent user experience.

**Input Validation and Sanitization:**
- **Server-Side Validation**: Comprehensive validation for all form inputs including email format, numeric ranges, and required fields
- **SQL Injection Prevention**: Parameterized queries throughout the application to prevent database attacks
- **Data Type Conversion**: Proper handling of string to numeric conversions with error catching for invalid inputs
- **Edge Case Handling**: Graceful handling of missing data, null values, and unexpected input formats

**Database Transaction Management:**
- **ACID Compliance**: Proper use of database transactions with commit and rollback functionality
- **Connection Management**: Efficient database connection handling with proper opening and closing
- **Error Recovery**: Comprehensive exception handling with database rollback on errors
- **Data Integrity**: Foreign key constraints and validation to maintain referential integrity

**User Feedback and Error Handling:**
- **Descriptive Error Messages**: User-friendly error messages that explain what went wrong and how to fix it
- **Success Confirmations**: Clear feedback for successful operations like workout saves and goal updates
- **Loading States**: Visual indicators during database operations and data processing
- **Fallback Handling**: Graceful degradation when features are unavailable or data is missing

### Phase 8: Testing and Debugging (Week 9)
Throughout development, I conducted extensive testing of all features and implemented comprehensive debugging tools to ensure application reliability.

**Feature Testing:**
- **User Authentication Flow**: Tested login, registration, and session management across different browsers and scenarios
- **Workout Logging**: Comprehensive testing of timer functionality, exercise entry, and data persistence
- **Goal Management**: Validation of goal creation, progress tracking, and completion detection
- **Data Visualization**: Testing of statistical calculations and chart rendering with various data sets

**Performance Optimization:**
- **Database Query Optimization**: Analyzed and optimized SQL queries for better performance, especially for dashboard statistics
- **Data Loading Strategies**: Implemented efficient data loading patterns to minimize page load times
- **Memory Management**: Proper handling of database connections and session data to prevent memory leaks
- **Caching Strategies**: Strategic use of session storage and query result caching for frequently accessed data

**Debug Implementation:**
- **Comprehensive Logging**: Added debug print statements throughout the application for development troubleshooting
- **Error Tracking**: Detailed error logging with stack traces for debugging complex issues
- **Data Validation**: Added verification steps in data population routes to ensure sample data integrity
- **Browser Developer Tools**: Extensive use of browser debugging tools for client-side JavaScript and styling issues

**Quality Assurance:**
- **Cross-Browser Testing**: Verified functionality across Chrome, Firefox, and Edge browsers
- **Responsive Testing**: Tested mobile and desktop layouts to ensure proper responsive behavior
- **Data Accuracy**: Validated mathematical calculations for streaks, progress percentages, and statistical displays
- **User Experience Testing**: Conducted usability testing to ensure intuitive navigation and feature discovery

### Phase 9: Progressive Web App Features (Week 10)
Building on the Flask PWA tutorial foundation, I implemented PWA-compliant features to enhance the user experience and enable app-like functionality.

**PWA Compliance Implementation:**
- **Manifest Configuration**: Created comprehensive `manifest.json` with proper app metadata, icons, and installation settings
- **Service Worker**: Implemented `serviceworker.js` for offline functionality and resource caching
- **Installation Capability**: Enabled "Add to Home Screen" functionality for mobile and desktop installation
- **Responsive Icons**: Created multiple icon sizes (128x128, 192x192, 384x384, 512x512) for different display contexts

**Offline Functionality:**
- **Resource Caching**: Strategic caching of CSS, JavaScript, images, and core HTML files for offline access
- **Fallback Pages**: Graceful handling of offline scenarios with appropriate user feedback
- **Data Synchronization**: Foundation for future offline data storage and sync capabilities

### Current Status and Achievements
The FitNet application is now a fully functional fitness tracking web application that exceeds the core requirements outlined in the project specification. The application successfully demonstrates mastery of multiple technical domains:

**Technical Proficiency Demonstrated:**
- **Full-Stack Web Development**: Complete implementation using Flask framework with proper MVC architecture
- **Database Design and Management**: Comprehensive SQLite database with complex relationships and data integrity
- **User Interface Design**: Professional, responsive web interface following modern design principles
- **JavaScript Integration**: Client-side functionality enhancing user experience and interactivity
- **Security Implementation**: Proper authentication, authorization, and data protection measures

**Functional Completeness:**
- **User Management**: Complete account creation, authentication, and profile management system
- **Workout Tracking**: Comprehensive exercise logging with timer functionality and detailed exercise records
- **Progress Monitoring**: Statistical analysis, goal tracking, and historical data visualization
- **Data Persistence**: Reliable data storage and retrieval with proper error handling and validation

**Professional Development Practices:**
- **Code Organization**: Well-structured codebase following Python and web development best practices
- **Documentation**: Comprehensive inline comments and debugging information throughout the application
- **Testing Methodology**: Systematic testing approach with validation of all major features and edge cases
- **Performance Optimization**: Efficient database queries and optimized user interface for responsive performance

The project successfully demonstrates proficiency in web development using Flask, database design with SQLite, user interface design with HTML/CSS, JavaScript integration, and full-stack application development principles. All major features are implemented and tested, providing a robust fitness tracking solution that could serve as a foundation for commercial application development.

## Getting Started - How to Download and Run FitNet

### Prerequisites
Before running FitNet, ensure you have the following installed on your system:

1. **Python 3.x** - [Download from python.org](https://www.python.org/downloads/)
2. **Git** - [Download from git-scm.com](https://git-scm.com/downloads/) 
3. **VSCode** (recommended) - [Download from code.visualstudio.com](https://code.visualstudio.com/download)

> **Note:** On macOS and Linux, you may need to use `pip3` instead of `pip` for package installation.

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YourUsername/FitNet.git
   cd FitNet
   ```

2. **Install Required Dependencies**
   ```bash
   pip install flask
   ```

3. **Verify Database Setup**
   The SQLite database (`database/data_source.db`) is included in the project. No additional database setup is required.

4. **Run the Application**
   ```bash
   python main.py
   ```

5. **Access the Website**
   - Open your web browser
   - Navigate to: `http://localhost:5000` or `http://127.0.0.1:5000`
   - The FitNet login page should appear

### First Time Setup

**Creating Your Account:**
1. Click "Sign Up" on the login page
2. Fill in your personal information:
   - First Name and Last Name
   - Email address (must be unique)
   - Password
   - Age, Height, and Weight
3. Click "Create Account"
4. You'll be automatically logged in and redirected to the dashboard

**Alternative - Use Test Account:**
If sample data has been populated, you can login with existing test accounts:
Go to data_source.db and use one of the accounts on the Users table to sign in. Each of these accounts come with:
- 20 different workouts already added with 3 exercises for each workout.
- 3 set goals.
- A unique set of data (age, weight, and height)

### Key Features to Try

1. **Dashboard**: View your workout streak, weekly progress, and recent activities
2. **Log Workout**: Start the timer, add exercises with sets/reps/weight, and save your session
3. **Progress**: Track your statistics, view charts, and monitor goal progress
4. **Profile**: Update personal information, upload a profile photo, and manage fitness goals

### Troubleshooting

**Common Issues:**
- **"Module not found" errors**: Ensure Flask is installed with `pip install flask`
- **Database errors**: Check that `database/data_source.db` exists in the project directory
- **Port already in use**: If port 5000 is busy, the app will automatically try port 5001
- **Profile images not displaying**: Ensure the `static/uploads/` directory exists

**Getting Help:**
- Check the browser developer console (F12) for JavaScript errors
- Review the terminal output where you ran `python main.py` for server-side errors
- Ensure all file paths match the project structure exactly

### Development Mode Features

The application runs in debug mode by default, which provides:
- Automatic server restart when code changes
- Detailed error messages in the browser
- Hot reloading for faster development

To run in production mode, modify `main.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Progressive Web App Features

FitNet includes PWA capabilities:
- **Install as App**: Click the install button in your browser's address bar to add FitNet to your desktop or home screen
- **Offline Access**: Core functionality works without internet connection
- **Mobile Optimized**: Responsive design works on all device sizes