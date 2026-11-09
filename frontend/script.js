const isLocalhost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || !window.location.hostname;
const API_URL = (!isLocalhost || window.location.port === "8000")
    ? window.location.origin
    : "http://127.0.0.1:8000";

const form = document.getElementById("complaintForm");
const result = document.getElementById("result");

const departmentText = document.getElementById("department");
const priorityText = document.getElementById("priority");
const probabilityText = document.getElementById("probability");
const messageText = document.getElementById("message");

const confirmButton = document.getElementById("confirmButton");
const cancelButton = document.getElementById("cancelButton");

let currentComplaint = null;

form.addEventListener("submit", async (event) => {
    confirmButton.hidden = false;
    confirmButton.disabled = false;
    cancelButton.disabled = false;
    event.preventDefault();

    const citizenId = Number(
        document.getElementById("citizenId").value
    );

    const complaint = document.getElementById("complaint").value.trim();

    currentComplaint = null;
    result.hidden = true;

    try {
        const response = await fetch(`${API_URL}/complaints`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                citizen_id: citizenId,
                complaint: complaint,
                confirm: false
            })
        });

        const data =await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to analyze complaint.");
        }

        departmentText.textContent = `Suggested department: ${data.predicted_department}`;

        priorityText.textContent = `Suggested priority: ${data.suggested_priority}`;

        probabilityText.textContent = `Estimated probability: ${data.probability_percent}%`;

        messageText.textContent = "Review the suggestions before submitting.";

        currentComplaint = { citizenId, complaint };
        result.hidden = false;
        
    } catch (error) {
        messageText.textContent = error.message;
        result.hidden = false;
        confirmButton.hidden = true;
    }
});

confirmButton.addEventListener("click", async () => {
    if (!currentComplaint) return;

    confirmButton.disabled = true;
    messageText.textContent = "Submitting complaint...";

    try {
        const response = await fetch(`${API_URL}/complaints`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                citizen_id: currentComplaint.citizenId,
                complaint: currentComplaint.complaint,
                confirm: true
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Submission failed.");
        }

        departmentText.textContent = `Department: ${data.department}`;
        priorityText.textContent = `Priority: ${data.priority}`;
        probabilityText.textContent =  `Estimated probability: ${data.probability_percent}%`;

        messageText.textContent = `Complaint submitted successfully! ID: ${data.complaint_id}. Status: ${data.status}`;

        confirmButton.hidden = true;
        cancelButton.hidden = true;
        currentComplaint = null;
        form.reset();
    } catch (error) {
        messageText.textContent = error.message;
    } finally {
        confirmButton.disabled = false;
    }
});

cancelButton.addEventListener("click", () => {
    currentComplaint = null;
    result.hidden = true;
    confirmButton.hidden = false;
});