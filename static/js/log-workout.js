let timer = 0;
let timerInterval;
let isRunning = false;
let sessionLog = [];

// Timer functionality
function startTimer() {
    if (!isRunning) {
        timerInterval = setInterval(() => {
            timer++;
            updateTimerDisplay();
        }, 1000);
        isRunning = true;
        document.getElementById('startTimer').style.display = 'none';
        document.getElementById('stopTimer').style.display = 'inline-block';
    }
}

function stopTimer() {
    if (isRunning) {
        clearInterval(timerInterval);
        isRunning = false;
        document.getElementById('startTimer').style.display = 'inline-block';
        document.getElementById('stopTimer').style.display = 'none';
    }
}

function updateTimerDisplay() {
    const minutes = Math.floor(timer / 60);
    const seconds = timer % 60;
    document.getElementById('timer').textContent = 
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
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
}

function updateSessionDisplay() {
    const sessionLogElement = document.getElementById('sessionLog');
    const saveButton = document.getElementById('saveWorkout');

    if (sessionLog.length === 0) {
        sessionLogElement.innerHTML = '<p class="empty-state">No exercises logged yet. Add your first exercise above!</p>';
        saveButton.style.display = 'none';
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
        saveButton.style.display = 'inline-block';
    }
}

function removeExercise(index) {
    sessionLog.splice(index, 1);
    updateSessionDisplay();
}

function clearForm() {
    document.getElementById('exerciseName').value = '';
    document.getElementById('sets').value = '3';
    document.getElementById('reps').value = '12';
    document.getElementById('weight').value = '0';
    document.getElementById('notes').value = '';
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
        // Reset the form
        sessionLog = [];
        timer = 0;
        stopTimer();
        updateTimerDisplay();
        updateSessionDisplay();
        document.getElementById('workoutType').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving workout');
    });
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('startTimer').addEventListener('click', startTimer);
    document.getElementById('stopTimer').addEventListener('click', stopTimer);
    document.getElementById('addExercise').addEventListener('click', addExercise);
    document.getElementById('saveWorkout').addEventListener('click', saveWorkout);
});
