// Tab functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const chartContents = document.querySelectorAll('.chart-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            chartContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(tabName + 'Chart').classList.add('active');
        });
    });

    // Initialize charts
    initializeCharts();
});

function initializeCharts() {
    // Get data from template (you'll need to pass this from Flask)
    const weeklyData = {{ weekly_data | tojsonfilter | safe }};
    const strengthData = {{ strength_data | tojsonfilter | safe }};
    const monthlyData = {{ monthly_data | tojsonfilter | safe }};

    // Weekly Workout Chart with real data
    const weeklyCtx = document.getElementById('weeklyChart').getContext('2d');
    const weeklyLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const weeklyValues = weeklyLabels.map(day => {
        const found = weeklyData.find(d => d.day_name === day);
        return found ? found.total_minutes : 0;
    });

    new Chart(weeklyCtx, {
        type: 'bar',
        data: {
            labels: weeklyLabels,
            datasets: [{
                data: weeklyValues,
                backgroundColor: '#758BFD',
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { color: '#F1F2F6' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#F1F2F6' }
                }
            }
        }
    });

    // Strength Progress Chart with real data
    if (strengthData.length > 0) {
        const strengthCtx = document.getElementById('strengthProgressChart').getContext('2d');
        new Chart(strengthCtx, {
            type: 'line',
            data: {
                labels: strengthData.map(d => d.workout_date),
                datasets: [{
                    label: 'Bench Press (kg)',
                    data: strengthData.map(d => d.max_weight),
                    borderColor: '#758BFD',
                    backgroundColor: 'rgba(117, 139, 253, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { 
                        display: true,
                        labels: { color: '#F1F2F6' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#F1F2F6' }
                    },
                    x: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#F1F2F6' }
                    }
                }
            }
        });
    }

    // Monthly Overview Chart with real data
    if (monthlyData.length > 0) {
        const monthlyCtx = document.getElementById('monthlyOverviewChart').getContext('2d');
        new Chart(monthlyCtx, {
            type: 'line',
            data: {
                labels: monthlyData.map(d => d.month),
                datasets: [{
                    label: 'Workouts',
                    data: monthlyData.map(d => d.workouts),
                    borderColor: '#758BFD',
                    backgroundColor: 'rgba(117, 139, 253, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y'
                }, {
                    label: 'Hours',
                    data: monthlyData.map(d => d.hours),
                    borderColor: '#AEB8FE',
                    backgroundColor: 'rgba(174, 184, 254, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { 
                        display: true,
                        labels: { color: '#F1F2F6' }
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#F1F2F6' }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        ticks: { color: '#F1F2F6' }
                    },
                    x: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#F1F2F6' }
                    }
                }
            }
        });
    }
}
