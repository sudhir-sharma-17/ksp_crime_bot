let chartInstance = null;

// ==================================================
// DOM ELEMENTS
// ==================================================
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatHistory = document.getElementById("chat-history");
const tableContainer = document.getElementById("table-container");
const rowCountLabel = document.getElementById("row-count");
const chartCanvas = document.getElementById("visualChart");
const contentArea = document.getElementById("content-area");
const chartEmptyState = document.getElementById("chart-empty");
const debugToggle = document.getElementById("debug-toggle");
const debugLog = document.getElementById("debug-log");
const debugEmpty = document.getElementById("debug-empty");

// ==================================================
// EVENT LISTENERS
// ==================================================
chatForm.addEventListener("submit", handleChatSubmit);

debugToggle.addEventListener("click", () => {
    debugToggle.classList.toggle("open");
    debugLog.classList.toggle("open");
});

// ==================================================
// CHAT LOGIC
// ==================================================
async function handleChatSubmit(event) {
    event.preventDefault();
    
    const query = userInput.value.trim();
    if (!query) return;
    
    // Clear input
    userInput.value = "";
    
    // Append user message
    appendMessage(query, "user");
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: query
            })
        });
        
        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeElement(typingId);
        
        // Render the English analytical summary
        // Fallback to error message or final output if not available
        let agentResponse = "I could not process that request.";
        if (data.debug && data.debug.analytical_summary) {
            agentResponse = data.debug.analytical_summary;
        } else if (data.message) {
            agentResponse = data.message;
        }
        
        appendMessage(agentResponse, "agent");
        
        if (data.debug) {
            updateDashboard(data.debug);
        }
        
    } catch (error) {
        console.error("API Error:", error);
        removeElement(typingId);
        appendMessage("An error occurred while connecting to the server.", "agent");
    }
}

function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}`;
    msgDiv.textContent = text;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function showTypingIndicator() {
    const indicatorDiv = document.createElement("div");
    const id = "typing-" + Date.now();
    indicatorDiv.id = id;
    indicatorDiv.className = "message agent typing";
    indicatorDiv.innerHTML = "<span></span><span></span><span></span>";
    chatHistory.appendChild(indicatorDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return id;
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ==================================================
// DASHBOARD UPDATE LOGIC
// ==================================================
function updateDashboard(debugData) {
    // Semantic Routing Display Logic
    const hasData = debugData.sql_results && debugData.sql_results.length > 0 && debugData.generated_sql !== "CHITCHAT";
    if (hasData) {
        contentArea.classList.add("has-data");
    } else {
        contentArea.classList.remove("has-data");
    }
    
    updateDebugLog(debugData);
    updateTable(debugData.sql_results, debugData.generated_sql);
    renderChart(debugData.sql_results, debugData.generated_sql);
}

function updateDebugLog(debugData) {
    if (debugEmpty) debugEmpty.style.display = "none";
    
    let logHtml = `<span class="terminal-prompt">Status: ${debugData.status || 'SUCCESS'}</span>\n`;
    logHtml += `<span class="terminal-prompt">Retries: ${debugData.retry_count || 0}</span>\n\n`;
    
    if (debugData.translated_query) {
        logHtml += `<span class="terminal-prompt">Translated Query:</span>\n${debugData.translated_query}\n\n`;
    }
    
    logHtml += `<span class="terminal-prompt">Generated SQL:</span>\n<span class="sql-highlight">${debugData.generated_sql || 'N/A'}</span>\n`;
    
    if (debugData.sql_error) {
        logHtml += `\n<span class="terminal-prompt">SQL Error:</span>\n<span class="error-highlight">${debugData.sql_error}</span>`;
    }
    
    debugLog.innerHTML = logHtml;
    
    // Auto-open debug log if there was an error
    if (debugData.sql_error && !debugToggle.classList.contains("open")) {
        debugToggle.classList.add("open");
        debugLog.classList.add("open");
    }
}

function updateTable(results, generatedSql) {
    const tableCard = tableContainer.closest('.card');
    
    if (!results || results.length === 0 || generatedSql === "CHITCHAT") {
        return;
    }
    
    rowCountLabel.textContent = `${results.length} row${results.length !== 1 ? 's' : ''}`;
    
    const headers = Object.keys(results[0]);
    let tableHtml = `<table><thead><tr>`;
    
    headers.forEach(h => {
        tableHtml += `<th>${h}</th>`;
    });
    tableHtml += `</tr></thead><tbody>`;
    
    results.forEach(row => {
        tableHtml += `<tr>`;
        headers.forEach(h => {
            const val = row[h] !== null ? row[h] : "NULL";
            tableHtml += `<td>${val}</td>`;
        });
        tableHtml += `</tr>`;
    });
    tableHtml += `</tbody></table>`;
    
    tableContainer.innerHTML = tableHtml;
}

// ==================================================
// CHART RENDERING
// ==================================================
function renderChart(results, generatedSql) {
    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
    
    const chartCard = chartCanvas.closest('.card');
    
    if (!results || results.length === 0 || generatedSql === "CHITCHAT") {
        return;
    }
    
    chartEmptyState.style.display = "none";
    chartCanvas.style.display = "block";
    
    const keys = Object.keys(results[0]);
    let labelKey = null;
    let valueKey = null;
    
    // Auto-detect columns for charting
    for (let key of keys) {
        const val = results[0][key];
        if (typeof val === "number") {
            valueKey = key;
        } else if (typeof val === "string" && !labelKey && !key.toLowerCase().includes("id")) {
            labelKey = key;
        }
    }
    
    let labels = [];
    let dataPoints = [];
    
    if (labelKey && valueKey) {
        labels = results.map(r => r[labelKey]);
        dataPoints = results.map(r => r[valueKey]);
    } else {
        // Fallback: frequency count of the first non-ID categorical column
        const targetKey = labelKey || keys.find(k => !k.toLowerCase().includes("id")) || keys[0];
        const freqMap = {};
        
        results.forEach(r => {
            const val = r[targetKey] || "Unknown";
            freqMap[val] = (freqMap[val] || 0) + 1;
        });
        
        labels = Object.keys(freqMap);
        dataPoints = Object.values(freqMap);
        valueKey = "Count";
    }
    
    // Limit to 10 items for visual clarity
    if (labels.length > 10) {
        labels = labels.slice(0, 10);
        dataPoints = dataPoints.slice(0, 10);
    }
    
    // Enterprise color palette
    const bgColors = [
        'rgba(30, 64, 175, 0.7)',   // Deep Blue
        'rgba(15, 118, 110, 0.7)',  // Teal
        'rgba(71, 85, 105, 0.7)',   // Slate Gray
        'rgba(37, 99, 235, 0.7)',   // Royal Blue
        'rgba(51, 65, 85, 0.7)',    // Dark Slate
        'rgba(13, 148, 136, 0.7)',  // Light Teal
        'rgba(100, 116, 139, 0.7)'  // Light Gray
    ];
    
    const borderColors = bgColors.map(color => color.replace('0.7', '1'));
    
    const isPieChart = labels.length <= 5;
    
    const ctx = chartCanvas.getContext("2d");
    chartInstance = new Chart(ctx, {
        type: isPieChart ? 'pie' : 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: valueKey,
                data: dataPoints,
                backgroundColor: bgColors,
                borderColor: borderColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: isPieChart ? 'right' : 'top',
                    labels: {
                        color: '#212529',
                        font: { family: 'Inter', size: 12 }
                    }
                }
            },
            scales: isPieChart ? { x: { display: false }, y: { display: false } } : {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#6c757d' },
                    grid: { color: '#dee2e6' }
                },
                x: {
                    ticks: { color: '#6c757d' },
                    grid: { display: false }
                }
            }
        }
    });
}

// ==================================================
// THREE.JS 3D SCENE SETUP
// ==================================================
function init3D() {
    const canvas = document.getElementById('canvas3d');
    if (!canvas) return;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
    camera.position.z = 5;

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const dirLight = new THREE.DirectionalLight(0x00d2ff, 1);
    dirLight.position.set(2, 3, 4);
    scene.add(dirLight);
    
    const dirLight2 = new THREE.DirectionalLight(0x00ff88, 0.5);
    dirLight2.position.set(-2, -3, -4);
    scene.add(dirLight2);

    // HACKATHON NOTE: Replace this mesh with the official KSP double-headed lion .gltf / .obj model asset here
    const geometry = new THREE.IcosahedronGeometry(1.5, 1); // stylized placeholder
    const material = new THREE.MeshPhysicalMaterial({
        color: 0x001133,
        metalness: 0.9,
        roughness: 0.1,
        emissive: 0x00d2ff,
        emissiveIntensity: 0.2,
        wireframe: true
    });
    
    const emblem = new THREE.Mesh(geometry, material);
    scene.add(emblem);

    function resize() {
        const parent = canvas.parentElement;
        if (parent && parent.clientWidth > 0) {
            const width = parent.clientWidth;
            const height = parent.clientHeight;
            if (canvas.width !== width || canvas.height !== height) {
                renderer.setSize(width, height, false);
                camera.aspect = width / height;
                camera.updateProjectionMatrix();
            }
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        resize();
        emblem.rotation.y += 0.005;
        emblem.rotation.x += 0.002;
        renderer.render(scene, camera);
    }
    
    animate();
}

document.addEventListener('DOMContentLoaded', init3D);
