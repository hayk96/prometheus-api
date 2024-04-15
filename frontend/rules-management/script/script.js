let filesData = [];
let currentFilename = '';
let codeMirrorInstance;

document.addEventListener('DOMContentLoaded', () => {
    codeMirrorInstance = CodeMirror.fromTextArea(document.getElementById('yamlEditor'), {
        mode: 'yaml',
        lineNumbers: true,
        theme: 'monokai',
        lineWrapping: true
    });

    document.getElementById('editAlertingRulesBtn').addEventListener('click', () => {
        fetchAndDisplayRules('alert');
    });

    document.getElementById('editRecordingRulesBtn').addEventListener('click', () => {
        fetchAndDisplayRules('record');
    });

    document.getElementById('fileSelector').addEventListener('change', (event) => {
        const selectedIndex = event.target.value;
        currentFilename = filesData[selectedIndex].file;
        const selectedGroup = filesData[selectedIndex];
        const preprocessedData = preprocessDataForYaml(selectedGroup);
        codeMirrorInstance.setValue(jsyaml.dump(preprocessedData));
        document.getElementById('editorContainer').style.display = 'block';
        setTimeout(() => {
            codeMirrorInstance.refresh();
        }, 1);
    });

    document.getElementById('cancelBtn').addEventListener('click', () => {
        codeMirrorInstance.setValue('');
        document.getElementById('editorContainer').style.display = 'none';
    });

    document.getElementById('saveBtn').addEventListener('click', saveRule);
});

document.addEventListener('keydown', function(event) {
    var modal = document.getElementById("myModal");
    if (event.key === "Escape") {
        modal.style.display = "none";
    }
});


function fetchAndDisplayRules(ruleType) {
    fetch(`http://localhost:5000/api/v1/rules?type=${ruleType}`)
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
            populateFileSelector(filesData);
        })
        .catch(error => {
            console.error(`Error fetching ${ruleType} rules:`, error);
        });
}

function populateFileSelector(groups) {
    const fileSelector = document.getElementById('fileSelector');
    fileSelector.innerHTML = '';
    groups.forEach((group, index) => {
        const option = new Option(group.file, index);
        fileSelector.add(option);
    });
    fileSelector.style.display = 'block';
    fileSelector.selectedIndex = -1;
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
}

function saveRule() {
    const editedYaml = codeMirrorInstance.getValue();
    try {
        const modifiedData = jsyaml.load(editedYaml);
        const payload = JSON.stringify({ data: modifiedData });
        const url = `http://localhost:5000/api/v1/rules/${encodeURIComponent(currentFilename)}`;

        fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            displayModal('Rule saved successfully.');
            document.getElementById('editorContainer').style.display = 'none';
        })
        .catch(error => {
            displayModal('Error saving rule: ' + error.message);
            console.error('Error:', error);
        });
    } catch (error) {
        displayModal('Error processing YAML: ' + error.message);
        console.error('Error parsing YAML:', error);
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