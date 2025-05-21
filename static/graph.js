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

      
      const scores = data.scores.map(d => d.Score);
      const labels = data.scores.map(d => d.Year);
      console.log("Processed Scores:", scores); 
      console.log("Processed Labels:", labels); 

      const incidentsByYear = data.incidents.reduce((acc, incident) => {
        const year = new Date(incident["Date of incident"]).getFullYear();
        if (!acc[year]) {
          acc[year] = [];
        }
        acc[year].push({
          name: incident["Incident name"],
          description: incident["Brief description of the incident"]
        });
        return acc;
      }, {});
      console.log("Incidents grouped by year:", incidentsByYear); 
      // ====== START: EXTRA INCIDENT DISPLAY ======
      const simpleIncidentList = document.getElementById('simpleIncidentList');
      simpleIncidentList.innerHTML = ''; 
      
      if (data.incidents && data.incidents.length > 0) {
        let html = `<h3>🗒️ Incidents Summary for ${name}</h3><div class="incident-grid">`;
      
        data.incidents.forEach(incident => {
          const year = incident["Date of incident"] ?? "N/A";
          const incidentName = incident["Incident name"] || "Unnamed incident";
          const description = incident["Brief description of the incident"] || "No description provided.";
          
      
          html += `
            <div class="incident-card">
              <div class="incident-header">
                <span class="incident-year">${year}</span>
                <span class="incident-title">${incidentName}</span>
                <span class="tooltip">
                  <span class="tooltip-icon">❓</span>
                  <span class="tooltip-text">
                    <strong>Description:</strong><br />
                    ${description}<br /><br />
                    
                  </span>
                </span>
              </div>
            </div>`;
        });
      
        html += `</div>`;
        simpleIncidentList.innerHTML = html;
      } else {
        simpleIncidentList.innerHTML = `<p>No incidents found for ${name}.</p>`;
      }
      
      
      // ====== END: EXTRA INCIDENT DISPLAY ======


      
      const ctx = document.getElementById('lineChart').getContext('2d');

      if (chartInstance) {
        chartInstance.destroy();  
      }

      chartInstance = new Chart(ctx, {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{
      label: 'Civil Liberties Score',
      data: scores,
      borderColor: 'blue',
      fill: false
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        min: 1,
        max: 7,
        ticks: {
          stepSize: 1,
          color: '#ffffff',
          font: {
            size: 16
          }
        },
        grid: {
          color: 'rgba(255,255,255,0.1)'
        }
      },
      x: {
        ticks: {
          color: '#ffffff',
          font: {
            size: 16
          }
        },
        grid: {
          color: 'rgba(255,255,255,0.1)'
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          color: '#ffffff',   
          font: {
            size: 18,         
            weight: 'bold'
          }
        }
        },
      tooltip: {
        callbacks: {
          afterLabel: function (ctx) {
            const year = parseInt(ctx.label);
            const incidents = incidentsByYear[year] || [];
            if (incidents.length > 0) {
              return incidents.flatMap(incident => [
                `Incident: ${incident.name}`,
                incident.description || ''
              ]);
            }
            return '';
          }
        }
      }
    }
  }
});

});
}