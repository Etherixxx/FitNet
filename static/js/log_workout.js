let timerInterval;
let elapsedSeconds = 0;
const exercises = [];

document.getElementById('start-timer').addEventListener('click', () => {
  const workoutType = document.getElementById('workout-type').value;
  if (!workoutType) {
    alert('Please select a workout type.');
    return;
  }
  document.getElementById('start-timer').disabled = true;
  document.getElementById('stop-timer').disabled = false;

  timerInterval = setInterval(() => {
    elapsedSeconds++;
    const minutes = Math.floor(elapsedSeconds / 60);
    const seconds = elapsedSeconds % 60;
    document.getElementById('timer-display').textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }, 1000);
});

document.getElementById('stop-timer').addEventListener('click', () => {
  clearInterval(timerInterval);
  document.getElementById('start-timer').disabled = false;
  document.getElementById('stop-timer').disabled = true;

  const workoutType = document.getElementById('workout-type').value;
  const workoutData = {
    workoutType,
    duration: elapsedSeconds,
    exercises,
  };

  fetch('/log-workout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(workoutData),
  })
    .then(response => response.json())
    .then(data => {
      alert('Workout logged successfully!');
      location.reload();
    })
    .catch(error => {
      console.error('Error logging workout:', error);
    });
});

document.getElementById('add-exercise').addEventListener('click', () => {
  const exerciseName = document.getElementById('exercise-name').value;
  const sets = parseInt(document.getElementById('sets').value, 10);
  const reps = parseInt(document.getElementById('reps').value, 10);
  const weight = parseFloat(document.getElementById('weight').value);
  const notes = document.getElementById('notes').value;

  if (!exerciseName || sets <= 0 || reps <= 0 || weight < 0) {
    alert('Please fill out all fields correctly.');
    return;
  }

  const exercise = { exerciseName, sets, reps, weight, notes };
  exercises.push(exercise);

  const exerciseLog = document.getElementById('exercise-log');
  const exerciseEntry = document.createElement('div');
  exerciseEntry.textContent = `${exerciseName} - ${sets} sets, ${reps} reps, ${weight} kg`;
  exerciseLog.appendChild(exerciseEntry);
});
