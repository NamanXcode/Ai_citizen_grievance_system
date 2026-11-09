const isLocalhost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || !window.location.hostname;
const AUTH_API = (!isLocalhost || window.location.port === "8000")
    ? window.location.origin
    : "http://127.0.0.1:8002";
const OFFICER_API = (!isLocalhost || window.location.port === "8000")
    ? window.location.origin
    : "http://127.0.0.1:8001";

let accessToken = null;
let complaints = [];

// HTML elements
const loginSection = document.getElementById("loginSection");
const dashboardSection = document.getElementById("dashboardSection");

const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");
const dashboardMessage = document.getElementById("dashboardMessage");

const complaintsContainer = document.getElementById("complaintsContainer");
const statusFilterElement = document.getElementById("statusFilter");
const priorityFilterElement = document.getElementById("priorityFilter");

const totalCountElement = document.getElementById("totalCount");
const pendingCountElement = document.getElementById("pendingCount");
const progressCountElement = document.getElementById("progressCount");
const resolvedCountElement = document.getElementById("resolvedCount");

// Check required HTML elements
if (
    !loginSection ||
    !dashboardSection ||
    !loginForm ||
    !loginMessage ||
    !dashboardMessage ||
    !complaintsContainer ||
    !statusFilterElement ||
    !priorityFilterElement ||
    !totalCountElement ||
    !pendingCountElement ||
    !progressCountElement ||
    !resolvedCountElement
) {
    throw new Error("Some required HTML elements are missing. Check officer.html IDs.");
}

// Helper: safely read JSON responses
async function readResponse(response) {
    const text = await response.text();

    try {
        return text ? JSON.parse(text) : {};
    } catch {
        throw new Error("Server returned an invalid response.");
    }
}

// Helper: normalize text so "In Progress", "in_progress", "InProgress" all match
function normalize(value) {
    return String(value ?? "")
        .toLowerCase()
        .replace(/[^a-z0-9]/g, "");
}

// Helper: true when the "All ..." option is selected
function isAll(value) {
    return value === "" || value.startsWith("all");
}

// Handle expired or invalid officer session
function handleUnauthorized() {
    logout();
    loginMessage.textContent = "Session expired. Please log in again.";
}

// Officer Login
loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    loginMessage.textContent = "Logging in...";

    try {
        const response = await fetch(`${AUTH_API}/officer/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await readResponse(response);

        if (!response.ok) {
            throw new Error(data.detail || "Login failed.");
        }

        accessToken = data.access_token;

        if (!accessToken || !data.officer) {
            throw new Error("Invalid login response from server.");
        }

        document.getElementById("officerName").textContent =
            data.officer.username;

        document.getElementById("departmentName").textContent =
            `Department: ${data.officer.department}`;

        loginSection.hidden = true;
        dashboardSection.hidden = false;

        loginForm.reset();
        loginMessage.textContent = "";

        // Reset filters on every new login
        statusFilterElement.value = "All";
        priorityFilterElement.value = "All";

        await loadComplaints();

    } catch (error) {
        loginMessage.textContent = error.message;
    }
});

// Load Department Complaints
async function loadComplaints() {
    dashboardMessage.textContent = "Loading complaints...";
    complaintsContainer.innerHTML = "";

    try {
        const response = await fetch(`${OFFICER_API}/officer/complaints`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`
            }
        });

        const data = await readResponse(response);

        if (response.status === 401) {
            handleUnauthorized();
            return false;
        }

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load complaints.");
        }

        if (!Array.isArray(data.complaints)) {
            throw new Error("Invalid complaints data received from server.");
        }

        complaints = data.complaints;

        console.table(complaints.map(c => ({
            id: c.id,
            status: c.status,
            priority: c.priority,
            department: c.department
        })));

        renderComplaints();
        return true;

    } catch (error) {
        dashboardMessage.textContent = error.message;
        return false;
    }
}

// Display and Filter Complaints
function renderComplaints() {
    complaintsContainer.innerHTML = "";
    updateStatistics();

    const selectedStatus = normalize(statusFilterElement.value);
    const selectedPriority = normalize(priorityFilterElement.value);

    const filteredComplaints = complaints.filter(complaint => {
        const complaintStatus = normalize(complaint.status);
        const complaintPriority = normalize(complaint.priority);

        return (
            (isAll(selectedStatus) || complaintStatus === selectedStatus) &&
            (isAll(selectedPriority) || complaintPriority === selectedPriority)
        );
    });

    console.log("Selected status:", selectedStatus);
    console.log("Selected priority:", selectedPriority);
    console.log("Filtered complaints:", filteredComplaints.length);

    dashboardMessage.textContent =
        `Showing ${filteredComplaints.length} of ${complaints.length} complaints`;

    if (filteredComplaints.length === 0) {
        complaintsContainer.textContent = "No complaints found.";
        return;
    }

    filteredComplaints.forEach(complaint => {
        const card = document.createElement("div");
        card.className = "complaint-card";

        const heading = document.createElement("h3");
        heading.textContent = `Complaint #${complaint.id}`;

        const description = document.createElement("p");
        description.textContent = `Description: ${complaint.description}`;

        const citizen = document.createElement("p");
        citizen.textContent = `Citizen ID: ${complaint.citizen_id}`;

        const priority = document.createElement("p");
        priority.textContent = `Priority: ${complaint.priority}`;

        const status = document.createElement("p");
        status.textContent = `Current status: ${complaint.status}`;

        const statusSelect = document.createElement("select");

        ["Pending", "In Progress", "Resolved"].forEach(value => {
            const option = document.createElement("option");

            option.value = value;
            option.textContent = value;

            if (normalize(complaint.status) === normalize(value)) {
                option.selected = true;
            }

            statusSelect.appendChild(option);
        });

        const updateButton = document.createElement("button");
        updateButton.className = "update-button";
        updateButton.textContent = "Update Status";

        updateButton.addEventListener("click", async () => {
            updateButton.disabled = true;

            await updateComplaintStatus(
                complaint.id,
                statusSelect.value
            );

            updateButton.disabled = false;
        });

        card.append(
            heading,
            description,
            citizen,
            priority,
            status,
            statusSelect,
            updateButton
        );

        complaintsContainer.appendChild(card);
    });
}

// Update Dashboard Statistics
function updateStatistics() {

    const total = complaints.length;
    
    const pending = complaints.filter(
        c => normalize(c.status) === "pending"
    ).length;

    const inProgress = complaints.filter(
        c => normalize(c.status) === "inprogress"
    ).length;

    const resolved = complaints.filter(
        c => normalize(c.status) === "resolved"
    ).length;

    totalCountElement.textContent = total;
    pendingCountElement.textContent = pending;
    progressCountElement.textContent = inProgress;
    resolvedCountElement.textContent = resolved;
}

// Update Complaint Status
async function updateComplaintStatus(complaintId, newStatus) {
    dashboardMessage.textContent = "Updating complaint...";

    try {
        const response = await fetch(
            `${OFFICER_API}/officer/complaints/${complaintId}/status`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    status: newStatus
                })
            }
        );

        const data = await readResponse(response);

        if (response.status === 401) {
            handleUnauthorized();
            return;
        }

        if (!response.ok) {
            throw new Error(data.detail || "Status update failed.");
        }


        // Reload from the server; current filters stay applied
        const reloadSuccess = await loadComplaints();

        if (!reloadSuccess) {
            return;
        }

        dashboardMessage.textContent =
            data.message || "Complaint status updated successfully.";

    } catch (error) {
        dashboardMessage.textContent = error.message;
    }
}

// Status and Priority Filters
statusFilterElement.addEventListener("change", renderComplaints);
priorityFilterElement.addEventListener("change", renderComplaints);

// Refresh Complaints
document.getElementById("refreshButton")
    .addEventListener("click", loadComplaints);

// Logout
function logout() {
    accessToken = null;
    complaints = [];

    dashboardSection.hidden = true;
    loginSection.hidden = false;

    loginMessage.textContent = "";
    dashboardMessage.textContent = "";

    complaintsContainer.innerHTML = "";

    loginForm.reset();
}

document.getElementById("logoutButton")
    .addEventListener("click", logout);