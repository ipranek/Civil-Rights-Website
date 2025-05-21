document.getElementById('countryForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const selectedCountry = document.getElementById('countrySelect').value;
  loadChartForCountry(selectedCountry);


  scrollToGraph();
});

function scrollToGraph() {
  const graphSection = document.getElementById('lineChart');
  graphSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

let chartInstance = null;

function loadChartForCountry(name) {
  console.log("Loading chart for:", name);
  fetch(`/api/country/${name}`)
    .then(res => res.json())
    .then(data => {
      console.log("API response:", data);
      const ctx = document.getElementById('lineChart').getContext('2d');
      const scores = data.scores.map(d => d.Score);
      const labels = data.scores.map(d => d.Year);

      if (chartInstance) {
        chartInstance.destroy();  
      }

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Civil Rights Score',
            data: scores,
            borderColor: 'blue',
            fill: false
          }]
        },
        options: {
          responsive: true,
          
          scales: {
            y: {
              min: 1,   // Minimum value for the y-axis
              max: 7,  // Maximum value for the y-axis
              ticks: {
                stepSize: 1, // Ensures that the ticks go from 1 to 10 with a step of 1
                }
              }
            },
          plugins: {
            tooltip: {
              callbacks: {
                afterLabel: function (ctx) {
                  const year = parseInt(ctx.label);

                  const incidents = data.incidents.filter(i => {
                    const incidentDate = new Date(i["Date of incident"]);
                    return incidentDate.getFullYear() === year;
                  });

                  if (incidents.length > 0) {
                    return incidents.flatMap(incident => [
                      `Incident: ${incident["Incident name"]}`,
                      incident["Brief description of the incident"] || ''
                    ]);
                  }

                  return ''; // no incidents for this year
                }
              }
            }
          }
        }
      });
    });
}
