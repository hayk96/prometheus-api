document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    fetchAndDisplayPolicies();
});

function setupEventListeners() {
    document.getElementById('createPolicyBtn').addEventListener('click', openCreatePolicyModal);
    document.getElementById('submitNewPolicy').addEventListener('click', createPolicy);
    document.getElementById('cancelCreatePolicyBtn').addEventListener('click', closeCreatePolicyModal);
    document.getElementById('cancelEditPolicyBtn').addEventListener('click', closeEditPolicyModal);
    document.getElementById('submitEditPolicy').addEventListener('click', savePolicy);
    document.getElementById('confirmDeletePolicyBtn').addEventListener('click', confirmDeletePolicy);
    document.getElementById('cancelDeletePolicyBtn').addEventListener('click', closeDeletePolicyModal);
    document.getElementById('searchInput').addEventListener('input', handleSearchInput);
    document.getElementById('homeBtn').addEventListener('click', () => window.location.href = '/'); 
    document.getElementById('prometheusBtn').addEventListener('click', () => window.location.href = '/graph'); 
}

let allPolicies = [];
let policyToDelete = null;

/**
 * This function is responsible for retrieving the
 * current set of metrics lifecycle policies from
 * the server and displaying them on the user interface
 */
function fetchAndDisplayPolicies() {
    fetch('/api/v1/metrics-lifecycle-policies')
        .then(response => response.json())
        .then(data => {
            allPolicies = data; 
            displayPolicies(data);
        })
        .catch(error => console.error('Error fetching policies:', error));
}

/**
 * This function is responsible for
 * rendering the metrics lifecycle
 * policies onto the user interface
 */
function displayPolicies(policies) {
    const policiesListElement = document.getElementById('policiesList');
    policiesListElement.innerHTML = '';

    if (Object.keys(policies).length === 0) {
        const noPoliciesMessage = document.createElement('div');
        noPoliciesMessage.className = 'no-policies-message';
        noPoliciesMessage.textContent = 'No metrics lifecycle policies are defined';
        policiesListElement.appendChild(noPoliciesMessage);
        return;
    }

    for (const [name, policy] of Object.entries(policies)) {
        const policyItem = document.createElement('div');
        policyItem.className = 'policy-item';

        const nameDiv = document.createElement('div');
        nameDiv.textContent = name;
        nameDiv.className = 'filename';
        policyItem.appendChild(nameDiv);

        const detailsDiv = document.createElement('div');
        detailsDiv.className = 'details';

        
        for (const [key, value] of Object.entries(policy)) {
            const fieldDiv = document.createElement('div');
            fieldDiv.className = `field-${key}`;
            fieldDiv.innerHTML = `<span class="field-name">${capitalizeFirstLetter(key)}:</span> <span title="${value}">${value}</span>`;
            detailsDiv.appendChild(fieldDiv);
        }

        policyItem.appendChild(detailsDiv);

        const buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'button-container';

        const editButton = document.createElement('button');
        editButton.className = 'edit-policy-btn';
        editButton.textContent = 'Edit';
        editButton.addEventListener('click', () => openEditPolicyModal(name, policy));
        buttonsContainer.appendChild(editButton);

        const deleteButton = document.createElement('button');
        deleteButton.className = 'remove-policy-btn';
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => openDeletePolicyModal(name));
        buttonsContainer.appendChild(deleteButton);

        policyItem.appendChild(buttonsContainer);
        policiesListElement.appendChild(policyItem);
    }
}

/**
 * This function is designed to take a string
 * as input and return a new string with the
 * first letter capitalized and the rest of
 * the string unchanged
 */
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).replace(/_/g, ' ');
}

/**
 * This function is an event handler designed
 * to filter and display policies based on
 * user input in the search bar
 */
function handleSearchInput(event) {
    const searchTerm = event.target.value.toLowerCase();
    const filteredPolicies = {};

    for (const [name, policy] of Object.entries(allPolicies)) {
        if (policy.match.toLowerCase().includes(searchTerm)) {
            filteredPolicies[name] = policy;
        }
    }

    displayPolicies(filteredPolicies);
}

/**
 * This function is designed to handle
 * the user interaction for opening the
 * modal dialog used to create a new policy
 */
function openCreatePolicyModal() {
    document.getElementById('createPolicyModal').style.display = 'block';
}

/**
 * This function is responsible for handling
 * the user interaction to close the create
 * policy modal dialog
 */
function closeCreatePolicyModal() {
    document.getElementById('createPolicyModal').style.display = 'none';
    clearCreatePolicyForm();
}

/**
 * This function is designed to reset and clear
 * all input fields and error messages within
 * the "Create New Policy" modal dialog
 */
function clearCreatePolicyForm() {
    document.getElementById('newPolicyName').value = '';
    document.getElementById('newPolicyMatch').value = '';
    document.getElementById('newPolicyKeepFor').value = '';
    document.getElementById('newPolicyDescription').value = '';
    document.getElementById('createPolicyError').textContent = '';
}

/**
 * This function is responsible for creating a new
 * metrics lifecycle policy based on the input
 * provided by the user in the "Create New Policy"
 * modal dialog
 */
function createPolicy() {
    const name = document.getElementById('newPolicyName').value.trim();
    const match = document.getElementById('newPolicyMatch').value.trim();
    const keepFor = document.getElementById('newPolicyKeepFor').value.trim();
    const description = document.getElementById('newPolicyDescription').value.trim();

    
    if (!name || !match || !keepFor) {
        document.getElementById('createPolicyError').textContent = 'Policy name, match pattern, and retention period are required.';
        return;
    }

    const policy = { name, match, keep_for: keepFor, description };

    fetch('/api/v1/metrics-lifecycle-policies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(policy)
    })
    .then(response => response.json().then(data => ({ ok: response.ok, data }))) 
    .then(({ ok, data }) => {
        if (ok) {
            closeCreatePolicyModal();
            fetchAndDisplayPolicies();
        } else {
            throw new Error(data.message || 'An error occurred'); 
        }
    })
    .catch(error => {
        document.getElementById('createPolicyError').textContent = `Error creating policy: ${error.message}`;
    });
}

/**
 * This function is responsible for opening
 * the modal dialog to edit an existing
 * metrics lifecycle policy
 */
function openEditPolicyModal(name, policy) {
    document.getElementById('editPolicyName').value = name;
    document.getElementById('editPolicyMatch').value = policy.match;
    document.getElementById('editPolicyKeepFor').value = policy.keep_for;
    document.getElementById('editPolicyDescription').value = policy.description;
    document.getElementById('editPolicyModal').style.display = 'block';
}

/**
 * This function is responsible for closing
 * the edit policy modal dialog and clearing
 * any input fields within the modal
 */
function closeEditPolicyModal() {
    document.getElementById('editPolicyModal').style.display = 'none';
    clearEditPolicyForm();
}

/**
 * This function is designed to reset the
 * input fields and clear any error messages
 * in the edit policy modal.
 */
function clearEditPolicyForm() {
    document.getElementById('editPolicyName').value = '';
    document.getElementById('editPolicyMatch').value = '';
    document.getElementById('editPolicyKeepFor').value = '';
    document.getElementById('editPolicyDescription').value = '';
    document.getElementById('editPolicyError').textContent = '';
}

/**
 * This function is responsible for saving
 * the changes made to an existing policy
 */
function savePolicy() {
    const name = document.getElementById('editPolicyName').value.trim();
    const match = document.getElementById('editPolicyMatch').value.trim();
    const keepFor = document.getElementById('editPolicyKeepFor').value.trim();
    const description = document.getElementById('editPolicyDescription').value.trim();

    const policy = { match, keep_for: keepFor, description };

    fetch(`/api/v1/metrics-lifecycle-policies/${name}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(policy)
    })
    .then(response => {
        if (response.ok) {
            closeEditPolicyModal();
            fetchAndDisplayPolicies();
        } else {
            return response.json().then(data => {
                throw new Error(data.message);
            });
        }
    })
    .catch(error => {
        document.getElementById('editPolicyError').textContent = `Error saving policy: ${error.message}`;
    });
}

/**
 * This function is responsible for opening the delete
 * policy modal and setting up the necessary information
 * to confirm the deletion of a specified policy
 */
function openDeletePolicyModal(name) {
    policyToDelete = name;
    document.getElementById('deletePolicyModal').style.display = 'block';
}

/**
 * This function is responsible for closing
 * the delete policy modal and resetting
 * any relevant state or information.
 */
function closeDeletePolicyModal() {
    document.getElementById('deletePolicyModal').style.display = 'none';
    policyToDelete = null;
}

/**
 * This function is responsible for deleting a policy
 * when the user confirms the deletion action
 */
function confirmDeletePolicy() {
    if (policyToDelete) {
        fetch(`/api/v1/metrics-lifecycle-policies/${policyToDelete}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                closeDeletePolicyModal();
                fetchAndDisplayPolicies();
            } else {
                return response.json().then(data => {
                    throw new Error(data.message);
                });
            }
        })
        .catch(error => console.error('Error deleting policy:', error));
    }
}
