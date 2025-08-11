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
