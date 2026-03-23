// Fetch years from the backend and populate the dropdown
async function loadYears() {
    try {
        const response = await fetch('/years');
        if (!response.ok) {
            throw new Error('Failed to fetch years');
        }
        const data = await response.json();
        const years = data.years;

        // Get the select element
        const yearSelect = document.getElementById('year-select');
        
        // Clear existing options (except the first placeholder)
        yearSelect.innerHTML = '<option value="">-- Select a Year --</option>';

        // Add years to the dropdown
        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        });

    } catch (error) {
        console.error('Error loading years:', error);
        const yearSelect = document.getElementById('year-select');
        yearSelect.innerHTML = '<option value="">Error loading years</option>';
    }
}

// Fetch teams for a selected year
async function loadTeams(year) {
    try {
        console.log('Fetching teams for year:', year);
        const response = await fetch(`/teams?year=${year}`);
        if (!response.ok) {
            throw new Error('Failed to fetch teams');
        }
        const data = await response.json();
        console.log('Received data:', data);
        const teams = data.teams;
        console.log('Teams array:', teams);

        const teamsContainer = document.getElementById('teams-container');
        
        if (!teams || teams.length === 0) {
            teamsContainer.innerHTML = '<p>No teams found for this year.</p>';
            return;
        }

        // Check if league and division data exists
        const hasLeagueAndDivision = teams.some(team => team.league && team.division);

        let teamsHTML = '';

        if (hasLeagueAndDivision) {
            // Organize teams by league and division
            const organizedTeams = {};
            teams.forEach(team => {
                const league = team.league || 'Unknown League';
                const division = team.division || 'Unknown Division';
                
                if (!organizedTeams[league]) {
                    organizedTeams[league] = {};
                }
                if (!organizedTeams[league][division]) {
                    organizedTeams[league][division] = [];
                }
                organizedTeams[league][division].push(team);
            });

            // Build HTML with league and division structure
            teamsHTML = '<div class="leagues-container">';
            for (const league in organizedTeams) {
                teamsHTML += `<div class="league"><h4>${league}</h4>`;
                for (const division in organizedTeams[league]) {
                    teamsHTML += `<div class="division"><h5>${division}</h5><ul class="teams-list">`;
                    organizedTeams[league][division].forEach(team => {
                        teamsHTML += `<li class="team-item" data-team-id="${team.id}" data-team-name="${team.name}">${team.name}</li>`;
                    });
                    teamsHTML += '</ul></div>';
                }
                teamsHTML += '</div>';
            }
            teamsHTML += '</div>';
        } else {
            // Fallback: just list the team names
            teamsHTML = '<ul class="teams-list">';
            teams.forEach(team => {
                teamsHTML += `<li class="team-item" data-team-id="${team.id}" data-team-name="${team.name}">${team.name}</li>`;
            });
            teamsHTML += '</ul>';
        }

        console.log('Setting teams HTML:', teamsHTML);
        teamsContainer.innerHTML = teamsHTML;

        // Add click event listeners to team items using event delegation
        teamsContainer.addEventListener('click', async (event) => {
            const teamItem = event.target.closest('.team-item');
            if (!teamItem) return;
            
            event.preventDefault();
            const teamId = teamItem.getAttribute('data-team-id');
            const teamName = teamItem.getAttribute('data-team-name');
            const year = document.getElementById('year-select').value;
            
            console.log('Team clicked:', teamId, teamName);
            
            // Highlight selected team
            document.querySelectorAll('.team-item').forEach(item => item.classList.remove('active'));
            teamItem.classList.add('active');
            
            // Load and display roster
            await loadRoster(year, teamId, teamName);
        });

    } catch (error) {
        console.error('Error loading teams:', error);
        const teamsContainer = document.getElementById('teams-container');
        teamsContainer.innerHTML = '<p>Error loading teams.</p>';
    }
}

// Fetch players for a selected team
async function loadRoster(year, teamId, teamName) {
    try {
        const rosterColumn = document.getElementById('roster-column');
        const rosterContainer = document.getElementById('roster-container');
        const rosterTitle = document.getElementById('roster-title');

        // Show roster section and set title
        rosterColumn.style.display = 'block';
        rosterTitle.textContent = `${teamName} Roster`;
        rosterContainer.innerHTML = '<p class="loading">Loading roster...</p>';

        const response = await fetch(`/players?year=${year}&team=${teamId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch players');
        }
        const data = await response.json();
        const players = data.players;

        if (!players || players.length === 0) {
            rosterContainer.innerHTML = '<p>No players found for this team.</p>';
            return;
        }

        // Create roster HTML
        let rosterHTML = '<div class="players-grid">';
        players.forEach(player => {
            const fullName = `${player.first_name || 'Unknown'} ${player.last_name || 'Unknown'}`.trim();
            rosterHTML += `<div class="player-card"><span class="player-name">${fullName}</span></div>`;
        });
        rosterHTML += '</div>';

        rosterContainer.innerHTML = rosterHTML;

    } catch (error) {
        console.error('Error loading roster:', error);
        const rosterContainer = document.getElementById('roster-container');
        rosterContainer.innerHTML = '<p>Error loading roster.</p>';
    }
}

// Handle year selection
document.addEventListener('DOMContentLoaded', () => {
    loadYears();

    const yearSelect = document.getElementById('year-select');
    yearSelect.addEventListener('change', (event) => {
        const selectedYear = event.target.value;
        if (selectedYear) {
            console.log('Year selected:', selectedYear);
            const dataSection = document.getElementById('data-section');
            dataSection.style.display = 'block';
            dataSection.querySelector('h3').textContent = `Teams for ${selectedYear}`;
            loadTeams(selectedYear);
        }
    });
});