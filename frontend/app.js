const API_URL = "http://localhost:8000";


async function analyzeLog() {

    const fileInput = document.getElementById("logFile");
    const status = document.getElementById("status");

    if (!fileInput.files.length) {
        status.textContent = "Please select a log file.";
        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    status.textContent = "Analyzing...";

    try {

        const response = await fetch(
            `${API_URL}/analyze`,
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Analysis failed");
        }

        const data = await response.json();

        displayResults(data);

        status.textContent = "Analysis complete.";

    } catch (error) {

        console.error(error);

        status.textContent =
            "Could not connect to the analysis server.";

    }
}


function displayResults(data) {

    document
        .getElementById("summary")
        .classList.remove("hidden");

    document.getElementById("totalLines")
        .textContent = data.total_lines;

    document.getElementById("totalAlerts")
        .textContent = data.alerts.length;

    const highAlerts = data.alerts.filter(
        alert => alert.severity === "high"
    );

    document.getElementById("highAlerts")
        .textContent = highAlerts.length;


    const container =
        document.getElementById("alerts");

    container.innerHTML = "";


    if (data.alerts.length === 0) {

        container.innerHTML =
            "<p>No suspicious activity detected.</p>";

        return;
    }


    data.alerts.forEach(alert => {

        const div = document.createElement("div");

        div.className =
            `alert ${alert.severity}`;

        div.innerHTML = `
            <strong>${alert.type}</strong>
            <br>
            Severity: ${alert.severity}
            <br>
            IP: ${alert.ip || "N/A"}
            <br>
            ${alert.message || ""}
        `;

        container.appendChild(div);

    });
}
