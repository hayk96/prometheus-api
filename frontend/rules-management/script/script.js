let filesData = [];
let currentFilename = '';
let codeMirrorInstance;

document.addEventListener('DOMContentLoaded', () => {
    setupEditor();
    setupEventListeners();
    fetchAndDisplayAllRules();
});

function fetchAndDisplayRules() {
    fetch(`http://localhost:5000/api/v1/rules`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(json => {
            if (!json.data) {
                throw new Error('No data found in the response');
            }
            filesData = json.data.groups; 
            displayRulesList(filesData); 
        })
        .catch(error => {
            console.error('Error fetching rules:', error);
        });
}

function populateFileSelector(groups) {
    const fileSelector = document.getElementById('fileSelector');
    fileSelector.innerHTML = '';
    groups.forEach((group, index) => {
        const option = new Option(group.file, index);
        option.textContent = group.file;
        fileSelector.add(option);
    });
    fileSelector.style.display = 'block';
    fileSelector.selectedIndex = -1;
}

function handleFileSelection(event) {
    const selectedIndex = event.target.value;
    const selectedGroup = filesData[selectedIndex];
    currentFilename = selectedGroup.file;
    const preprocessedData = preprocessDataForYaml(selectedGroup);
    codeMirrorInstance.setValue(jsyaml.dump(preprocessedData));
    document.getElementById('editorContainer').style.display = 'block';
}

function preprocessDataForYaml(selectedGroup) {
    let groupType = selectedGroup.rules[0]?.type;

    if (!groupType) {
        console.error('Rule type is undefined.');
        return null;
    }

    let processedRules = selectedGroup.rules.map(rule => {
        if (rule.type === 'alerting') {
            return {
                alert: rule.name,
                expr: rule.query,
                for: convertDurationToHumanReadable(rule.duration),
                labels: rule.labels,
                annotations: rule.annotations
            };
        } else if (rule.type === 'recording') {
            return {
                record: rule.name,
                expr: rule.query,
                labels: rule.labels,
                annotations: rule.annotations
            };
        }
    });

    let processedGroup = {
        name: selectedGroup.name,
        rules: processedRules.filter(Boolean)
    };

    return { groups: [processedGroup] };
}

function convertDurationToHumanReadable(duration) {
    const second = 1;
    const minute = 60 * second;
    const hour = 60 * minute;
    const day = 24 * hour;
    const week = 7 * day;
    const year = 365.25 * day;

    let result = '';

    if (duration >= year) {
        result += Math.floor(duration / year) + 'y';
        duration %= year;
    } else if (duration >= week) {
        result += Math.floor(duration / week) + 'w';
        duration %= week;
    } else if (duration >= day) {
        result += Math.floor(duration / day) + 'd';
        duration %= day;
    } else if (duration >= hour) {
        result += Math.floor(duration / hour) + 'h';
        duration %= hour;
    } else if (duration >= minute) {
        result += Math.floor(duration / minute) + 'm';
        duration %= minute;
    } else if (duration >= second) {
        result += Math.floor(duration / second) + 's';
        duration %= second;
    } else if (duration > 0) {
        result += duration + 'ms';
    }

    return result;
}

function createRule() {
    const filename = prompt("Please enter the filename for the new rule:", "");
    if (filename) {
        currentFilename = filename;
        codeMirrorInstance.setValue('');
        document.getElementById('editorContainer').style.display = 'block';
    }
    setTimeout(() => {
        codeMirrorInstance.refresh();
    }, 0);
}

async function saveRule() {
    const editedYaml = codeMirrorInstance.getValue();
    try {
        const modifiedData = jsyaml.load(editedYaml);
        if (!modifiedData) {
            throw new Error('The YAML is empty or not structured correctly.');
        }
        const payload = JSON.stringify({ data: modifiedData });
        const filename = currentFilename ? encodeURIComponent(currentFilename.split('/').pop()) : '';
        const method = currentFilename ? 'PUT' : 'POST';
        const url = currentFilename ?
            `http://localhost:5000/api/v1/rules/${filename}?recreate=true` :
            `http://localhost:5000/api/v1/rules`;

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.message || `HTTP error! status: ${response.status}`);
        }

        await response.json(); 
        displayModal('Rule saved successfully.');
        document.getElementById('editorContainer').style.display = 'none';

        
        fetchAndDisplayAllRules();
    } catch (error) {
        displayModal(`Error saving rule: ${error.message}`);
        console.error('Error:', error);
    }
}




function displayModal(message) {
    var modal = document.getElementById("myModal");
    var text = document.getElementById("modal-text");
    var span = document.getElementsByClassName("close")[0];

    text.textContent = message;
    modal.style.display = "block";

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
}


function displayRulesList(groups) {
    const rulesListElement = document.getElementById('rulesList');
    rulesListElement.innerHTML = ''; 

    groups.forEach((group, groupIndex) => {
        group.rules.forEach((rule, ruleIndex) => {
            const ruleItem = document.createElement('div');
            ruleItem.className = 'rule-item';

            
            const filenameOnly = group.file.split('/').pop();

            
            const filenameDiv = document.createElement('div');
            filenameDiv.textContent = filenameOnly;
            filenameDiv.className = 'filename'; 
            ruleItem.appendChild(filenameDiv);

            
            const typeLabel = document.createElement('span');
            typeLabel.textContent = rule.type.charAt(0).toUpperCase() + rule.type.slice(1);
            typeLabel.className = `rule-type ${rule.type.toLowerCase()}`; 
            ruleItem.appendChild(typeLabel);

            
            const buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'buttons-container';

            
            const editButton = document.createElement('button');
            editButton.textContent = 'Edit';
            editButton.className = 'edit-rule-btn';
            editButton.addEventListener('click', () => editRule(group.file));
            buttonsContainer.appendChild(editButton);

            
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Remove';
            deleteButton.className = 'remove-rule-btn';
            deleteButton.addEventListener('click', () => {
                
                removeRule(group.file, groupIndex, ruleIndex);
            });
            buttonsContainer.appendChild(deleteButton);

            
            ruleItem.appendChild(buttonsContainer);

            
            rulesListElement.appendChild(ruleItem);
        });
    });
}

function removeRule(filePath, groupIndex, ruleIndex) {
    if (!confirm("Are you sure you want to delete this rule?")) {
        return;
    }

    
    const filenameOnly = filePath.split('/').pop();

    fetch(`http://localhost:5000/api/v1/rules/${encodeURIComponent(filenameOnly)}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            
            if(response.status !== 204) {
                return response.json().then(err => {
                    throw new Error(err.message || `HTTP error! status: ${response.status}`);
                });
            }
        }
        
        if (filesData[groupIndex] && filesData[groupIndex].rules[ruleIndex]) {
            filesData[groupIndex].rules.splice(ruleIndex, 1);
            if (filesData[groupIndex].rules.length === 0) {
                
                filesData.splice(groupIndex, 1);
            }
            displayRulesList(filesData); 
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function editRule(filePath) {
    currentFilename = filePath; 
    fetchRuleDetails(filePath);
    fetch(`http://localhost:5000/api/v1/rules?file[]=${encodeURIComponent(currentFilename)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data || !data.data || !data.data.groups || data.data.groups.length === 0) {
                console.error('No rules data found for:', currentFilename);
                alert('No rules data found for the file.');
                return;
            }
            
            const preprocessedData = preprocessDataForYaml(data.data.groups[0]);
            if (preprocessedData) {
                codeMirrorInstance.setValue(jsyaml.dump(preprocessedData));
                document.getElementById('editorContainer').style.display = 'block';
                
                setTimeout(() => codeMirrorInstance.refresh(), 1);
            } else {
                alert('Failed to process rules data.');
            }
        })
        .catch(error => {
            console.error('Error fetching rule details:', error);
            alert(`Error fetching rule details: ${error.message}`);
        });
}

function cancelEdit() {
    
    document.getElementById('editorContainer').style.display = 'none';
    codeMirrorInstance.setValue('');
    currentFilename = ''; 
}

function fetchRuleDetails(filePath) {
    fetch(`http://localhost:5000/api/v1/rules?file[]=${encodeURIComponent(filePath)}`)
        .then(response => response.json())
        .then(data => {
            
            
        })
        .catch(error => {
            console.error('Error fetching rule details:', error);
        });
}

function setupEditor() {
    const yamlEditor = document.getElementById('yamlEditor');
    if (yamlEditor) {
        codeMirrorInstance = CodeMirror.fromTextArea(yamlEditor, {
            mode: 'yaml',
            lineNumbers: true,
            theme: 'monokai',
            lineWrapping: true
        });
    }
}

function setupEventListeners() {
    
    document.getElementById('createRuleBtn')?.addEventListener('click', createRule);
    document.getElementById('editAlertingRulesBtn')?.addEventListener('click', () => fetchAndDisplayRules('alert'));
    document.getElementById('editRecordingRulesBtn')?.addEventListener('click', () => fetchAndDisplayRules('record'));
    document.getElementById('fileSelector')?.addEventListener('change', handleFileSelection);
    document.getElementById('saveBtn')?.addEventListener('click', saveRule);
    document.getElementById('cancelBtn')?.addEventListener('click', cancelEdit);
}

function fetchAndDisplayAllRules() {
    
    fetchAndDisplayRules('alert');
    fetchAndDisplayRules('record');
}

function removeRule(filePath) {
    
    const filenameOnly = filePath.split('/').pop();

    const deleteModal = document.getElementById('deleteModal');
    const deleteMessage = document.getElementById('deleteMessage');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');

    
    deleteMessage.textContent = `Are you sure you want to delete the file: ${filenameOnly}?`;
    deleteModal.style.display = 'block';

    
    function confirmDeletion() {
        
        fetch(`http://localhost:5000/api/v1/rules/${encodeURIComponent(filenameOnly)}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok && response.status !== 204) {
                return response.json().then(err => {
                    throw new Error(err.message || `HTTP error! status: ${response.status}`);
                });
            }
            displayModal('Rule deleted successfully.');
            fetchAndDisplayRules(); 
        })
        .catch(error => {
            displayModal(`Error deleting rule: ${error.message}`);
            console.error('Error:', error);
        });

        
        deleteModal.style.display = 'none';
        confirmDeleteBtn.removeEventListener('click', confirmDeletion);
        cancelDeleteBtn.removeEventListener('click', cancelDeletion);
    }

    
    function cancelDeletion() {
        deleteModal.style.display = 'none';
        confirmDeleteBtn.removeEventListener('click', confirmDeletion);
        cancelDeleteBtn.removeEventListener('click', cancelDeletion);
    }

    
    confirmDeleteBtn.addEventListener('click', confirmDeletion);
    cancelDeleteBtn.addEventListener('click', cancelDeletion);
}
