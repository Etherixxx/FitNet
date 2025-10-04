document.addEventListener('DOMContentLoaded', () => {
  let sessionLog = [];
  let workoutType = '';
  let isTimerActive = false;
  let timerSeconds = 0;
  let timerInterval;

  const timerDisplay = document.getElementById('timer-display');
  const workoutTypeSelect = document.getElementById('workout-type');
  const addExerciseForm = document.getElementById('add-exercise-form');
  const sessionLogContainer = document.getElementById('session-log');
  const saveWorkoutButton = document.getElementById('save-workout');

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const toggleTimer = () => {
    isTimerActive = !isTimerActive;
    if (isTimerActive) {
      timerInterval = setInterval(() => {
        timerSeconds++;
        timerDisplay.textContent = formatTime(timerSeconds);
      }, 1000);
    } else {
      clearInterval(timerInterval);
    }
  };

  const addExercise = (event) => {
    event.preventDefault();

    const formData = new FormData(addExerciseForm);
    const exercise = {
      id: Date.now(),
      name: formData.get('name'),
      sets: parseInt(formData.get('sets')) || 0,
      reps: parseInt(formData.get('reps')) || 0,
      weight: parseFloat(formData.get('weight')) || 0,
      notes: formData.get('notes'),
    };

    sessionLog.push(exercise);
    renderSessionLog();
    addExerciseForm.reset();
  };

  const removeExercise = (id) => {
    sessionLog = sessionLog.filter((exercise) => exercise.id !== id);
    renderSessionLog();
  };

  const renderSessionLog = () => {
    sessionLogContainer.innerHTML = '';
    sessionLog.forEach((exercise) => {
      const exerciseElement = document.createElement('div');
      exerciseElement.className = 'exercise-item';
      exerciseElement.innerHTML = `
        <div>
          <strong>${exercise.name}</strong> - ${exercise.sets} sets x ${exercise.reps} reps @ ${exercise.weight}kg
          <p>${exercise.notes}</p>
        </div>
        <button class="remove-exercise" data-id="${exercise.id}">Remove</button>
      `;
      exerciseElement.querySelector('.remove-exercise').addEventListener('click', () => removeExercise(exercise.id));
      sessionLogContainer.appendChild(exerciseElement);
    });
  };

  const saveWorkout = () => {
    fetch('/log-workout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ workoutType, sessionLog }),
    })
      .then((response) => response.json())
      .then((data) => alert(data.message))
      .catch((error) => console.error('Error:', error));
  };

  document.getElementById('toggle-timer').addEventListener('click', toggleTimer);
  workoutTypeSelect.addEventListener('change', (event) => (workoutType = event.target.value));
  addExerciseForm.addEventListener('submit', addExercise);
  saveWorkoutButton.addEventListener('click', saveWorkout);
});
