let timer = 0;
let timerInterval;
let isRunning = false;
let isPaused = false;
let sessionLog = [];
let workoutStartTime = null;

// Load timer state from localStorage on page load
function loadTimerState() {
    const savedState = localStorage.getItem('fitnet_workout_state');
    console.log('Loading timer state:', savedState);
    
    if (savedState) {
        try {
            const state = JSON.parse(savedState);
            console.log('Parsed state:', state);
            
            if (state.isRunning || state.isPaused) {
                timer = state.timer || 0;
                workoutStartTime = state.startTime;
                isPaused = state.isPaused || false;
                isRunning = state.isRunning || false;
                
                // If it was running, recalculate timer based on elapsed time
                if (state.isRunning && state.startTime) {
                    const now = Date.now();
                    const elapsedSeconds = Math.floor((now - state.startTime) / 1000);
                    timer = elapsedSeconds;
                }
                
                console.log('Restoring timer - seconds:', timer, 'isRunning:', isRunning, 'isPaused:', isPaused);
                
                // Restore workout type if available
                if (state.workoutType) {
                    const workoutTypeSelect = document.getElementById('workoutType');
                    if (workoutTypeSelect) {
                        workoutTypeSelect.value = state.workoutType;
                    }
                }
                
                // Restore session log if available
                if (state.sessionLog && Array.isArray(state.sessionLog)) {
                    sessionLog = state.sessionLog;
                }
                
                // Update UI based on state
                updateUIForState();
                updateTimerDisplay();
                updateSessionDisplay();
                
                // If it was running, start the interval
                if (isRunning) {
                    startTimerInterval();
                }
                
                console.log('Timer state restored');
            }
        } catch (error) {
            console.error('Error loading timer state:', error);
            localStorage.removeItem('fitnet_workout_state');
        }
    }
}

function updateUIForState() {
    const startButton = document.getElementById('startTimer');
    const stopButton = document.getElementById('stopTimer');
    
    if (isRunning) {
        if (startButton) startButton.style.display = 'none';
        if (stopButton) stopButton.style.display = 'inline-block';
    } else if (isPaused) {
        if (startButton) {
            startButton.style.display = 'inline-block';
            startButton.textContent = 'Resume';
        }
        if (stopButton) stopButton.style.display = 'none';
    } else {
        if (startButton) {
            startButton.style.display = 'inline-block';
            startButton.textContent = 'Start Timer';
        }
        if (stopButton) stopButton.style.display = 'none';
    }
}

function startTimerInterval() {
    if (timerInterval) clearInterval(timerInterval);
    
    timerInterval = setInterval(() => {
        timer++;
        updateTimerDisplay();
        if (timer % 10 === 0) {
            saveTimerState();
        }
    }, 1000);
}

// Save timer state to localStorage
function saveTimerState() {
    const workoutTypeSelect = document.getElementById('workoutType');
    const state = {
        isRunning: isRunning,
        isPaused: isPaused,
        timer: timer,
        startTime: workoutStartTime,
        sessionLog: sessionLog,
        workoutType: workoutTypeSelect ? workoutTypeSelect.value : '',
        savedAt: Date.now()
    };
    
    try {
        localStorage.setItem('fitnet_workout_state', JSON.stringify(state));
        console.log('Timer state saved:', state);
    } catch (error) {
        console.error('Error saving timer state:', error);
    }
}

// Clear timer state from localStorage
function clearTimerState() {
    localStorage.removeItem('fitnet_workout_state');
    console.log('Timer state cleared');
}

// Timer functionality
function startTimer() {
    console.log('startTimer called - isRunning:', isRunning, 'isPaused:', isPaused);
    
    if (isPaused) {
        // Resume from pause
        isRunning = true;
        isPaused = false;
        
        // Recalculate start time to maintain accurate timer
        workoutStartTime = Date.now() - (timer * 1000);
        
        startTimerInterval();
        updateUIForState();
        saveTimerState();
        
        console.log('Timer resumed from pause');
    } else if (!isRunning) {
        // Start new timer
        const now = Date.now();
        workoutStartTime = now;
        timer = 0;
        isRunning = true;
        isPaused = false;
        
        startTimerInterval();
        updateUIForState();
        saveTimerState();
        
        console.log('Timer started fresh');
        
        // Remove autostart parameter from URL
        if (window.location.search.includes('autostart=true')) {
            const url = new URL(window.location);
            url.searchParams.delete('autostart');
            window.history.replaceState({}, document.title, url.pathname);
        }
    }
}

function stopTimer() {
    console.log('stopTimer called');
    
    if (isRunning) {
        clearInterval(timerInterval);
        isRunning = false;
        isPaused = true;
        
        saveTimerState();
        showStopModal();
        
        console.log('Timer paused, showing modal');
    }
}

function showStopModal() {
    // Remove existing modal if it exists
    const existingModal = document.getElementById('stopModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create new modal
    const modal = document.createElement('div');
    modal.id = 'stopModal';
    modal.className = 'stop-modal';
    modal.innerHTML = `
        <div class="stop-modal-overlay"></div>
        <div class="stop-modal-content">
            <h3>Workout Paused</h3>
            <p>Timer: ${Math.floor(timer / 60)}:${(timer % 60).toString().padStart(2, '0')}</p>
            <p>What would you like to do?</p>
            <div class="stop-modal-buttons">
                <button id="resumeBtn" class="resume-btn">Resume</button>
                <button id="resetBtn" class="reset-btn">Reset</button>
                <button id="saveBtn" class="save-btn">Save Workout</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    // Add event listeners
    document.getElementById('resumeBtn').addEventListener('click', resumeTimer);
    document.getElementById('resetBtn').addEventListener('click', resetWorkout);
    document.getElementById('saveBtn').addEventListener('click', saveWorkoutFromModal);
    
    // Close modal when clicking overlay
    modal.querySelector('.stop-modal-overlay').addEventListener('click', hideStopModal);
    
    updateUIForState();
}

function hideStopModal() {
    const modal = document.getElementById('stopModal');
    if (modal) {
        modal.remove();
    }
}

function resumeTimer() {
    hideStopModal();
    startTimer(); // This will handle the resume logic
}

function resetWorkout() {
    console.log('resetWorkout called');
    
    // Clear everything
    clearInterval(timerInterval);
    isRunning = false;
    isPaused = false;
    timer = 0;
    workoutStartTime = null;
    sessionLog = [];
    
    // Reset UI
    updateTimerDisplay();
    updateSessionDisplay();
    updateUIForState();
    
    const workoutTypeSelect = document.getElementById('workoutType');
    if (workoutTypeSelect) workoutTypeSelect.value = '';
    
    clearForm();
    hideStopModal();
    clearTimerState();
    
    console.log('Workout reset complete');
}

function saveWorkoutFromModal() {
    const workoutType = document.getElementById('workoutType').value;
    if (!workoutType) {
        alert('Please select a workout type before saving');
        return;
    }
    
    if (sessionLog.length === 0) {
        alert('Please add at least one exercise before saving');
        return;
    }
    
    hideStopModal();
    saveWorkout();
}

function updateTimerDisplay() {
    const minutes = Math.floor(timer / 60);
    const seconds = timer % 60;
    const timerElement = document.getElementById('timer');
    if (timerElement) {
        timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
}

// Add exercise functionality
function addExercise() {
    const exerciseSelect = document.getElementById('exerciseName');
    const exerciseName = exerciseSelect.value;
    const sets = document.getElementById('sets').value;
    const reps = document.getElementById('reps').value;
    const weight = document.getElementById('weight').value;
    const notes = document.getElementById('notes').value;

    if (!exerciseName || !sets || !reps) {
        alert('Please select an exercise and fill in sets and reps');
        return;
    }

    const exercise = {
        name: exerciseName,
        sets: parseInt(sets),
        reps: parseInt(reps),
        weight: parseFloat(weight) || 0,
        notes: notes
    };

    sessionLog.push(exercise);
    updateSessionDisplay();
    clearForm();
    saveTimerState();
}

function updateSessionDisplay() {
    const sessionLogElement = document.getElementById('sessionLog');
    const saveButton = document.getElementById('saveWorkout');

    if (sessionLog.length === 0) {
        sessionLogElement.innerHTML = '<p class="empty-state">No exercises logged yet. Add your first exercise above!</p>';
        if (saveButton) saveButton.style.display = 'none';
    } else {
        sessionLogElement.innerHTML = `
            <p>${sessionLog.length} exercises logged</p>
            <div class="exercise-list">
                ${sessionLog.map((exercise, index) => `
                    <div class="exercise-item">
                        <span class="exercise-name">${exercise.name}</span>
                        <span class="exercise-details">${exercise.sets} sets × ${exercise.reps} reps @ ${exercise.weight}kg</span>
                        <button onclick="removeExercise(${index})" class="remove-btn">×</button>
                    </div>
                `).join('')}
            </div>
        `;
        if (saveButton) saveButton.style.display = 'inline-block';
    }
}

function removeExercise(index) {
    sessionLog.splice(index, 1);
    updateSessionDisplay();
    saveTimerState();
}

function clearForm() {
    const exerciseName = document.getElementById('exerciseName');
    const sets = document.getElementById('sets');
    const reps = document.getElementById('reps');
    const weight = document.getElementById('weight');
    const notes = document.getElementById('notes');
    
    if (exerciseName) exerciseName.value = '';
    if (sets) sets.value = '3';
    if (reps) reps.value = '12';
    if (weight) weight.value = '0';
    if (notes) notes.value = '';
}

function saveWorkout() {
    const workoutType = document.getElementById('workoutType').value;
    
    if (!workoutType) {
        alert('Please select a workout type');
        return;
    }

    if (sessionLog.length === 0) {
        alert('Please add at least one exercise');
        return;
    }

    const workoutData = {
        workoutType: workoutType,
        duration: timer,
        sessionLog: sessionLog
    };

    fetch('/log-workout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(workoutData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Workout saved successfully!');
        resetWorkout();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving workout');
    });
}

// Event listeners and initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing timer...');
    
    // Load any existing timer state first
    loadTimerState();
    
    // Set up event listeners
    const startButton = document.getElementById('startTimer');
    const stopButton = document.getElementById('stopTimer');
    const addButton = document.getElementById('addExercise');
    const saveButton = document.getElementById('saveWorkout');
    
    if (startButton) startButton.addEventListener('click', startTimer);
    if (stopButton) stopButton.addEventListener('click', stopTimer);
    if (addButton) addButton.addEventListener('click', addExercise);
    if (saveButton) saveButton.addEventListener('click', saveWorkout);
    
    // Handle autostart functionality (only if no existing workout)
    const urlParams = new URLSearchParams(window.location.search);
    const autostart = urlParams.get('autostart');
    
    if (autostart === 'true' && !isRunning && !isPaused) {
        console.log('Autostart requested');
        setTimeout(function() {
            if (!isRunning && !isPaused) {
                startTimer();
            }
        }, 100);
    }
});

// Save timer state when navigating away
window.addEventListener('beforeunload', function() {
    if (isRunning || isPaused) {
        saveTimerState();
        console.log('Page unloading, timer state saved');
    }
});

// Handle visibility changes
document.addEventListener('visibilitychange', function() {
    if (isRunning || isPaused) {
        saveTimerState();
        console.log('Visibility changed, timer state saved');
    }
});
