let filesData = [];
let currentFilename = '';
let codeMirrorInstance;

document.addEventListener('DOMContentLoaded', () => {
    const saveButton = document.getElementById('saveBtn'); // Adjust if your button has a different identifier
    saveButton.addEventListener('click', saveRule);
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
    });

    document.getElementById('cancelBtn').addEventListener('click', () => {
        codeMirrorInstance.setValue('');
        document.getElementById('editorContainer').style.display = 'none';
    });

    document.getElementById('saveBtn').addEventListener('click', () => {
        const editedYaml = codeMirrorInstance.getValue();
        try {
            const modifiedData = jsyaml.load(editedYaml);
            const payload = JSON.stringify({ data: modifiedData });
            const filename = encodeURIComponent(currentFilename.split('/').pop());

            fetch(`http://localhost:5000/api/v1/rules/${filename}?recreate=true`, {
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
                alert('Rule saved successfully.');
                document.getElementById('editorContainer').style.display = 'none';
            })
            .catch(error => {
                alert('Error saving rule: ' + error.message);
                console.error('Error:', error);
            });
        } catch (error) {
            alert('Error processing YAML: ' + error.message);
            console.error('Error parsing YAML:', error);
        }
    });
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

function saveRule() {
    const editedYaml = codeMirrorInstance.getValue();
    try {
        const modifiedData = jsyaml.load(editedYaml);
        const payload = JSON.stringify({ data: modifiedData });
        const filename = encodeURIComponent(currentFilename.split('/').pop());

        fetch(`http://localhost:5000/api/v1/rules/${filename}?recreate=true`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: payload
        })
        .then(response => {
            if (!response.ok) {
                // Parse the response as JSON only if the response is not ok
                return response.json().then(err => {
                    // If the JSON has a 'message' field, throw it as an error
                    throw new Error(err.message || `HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            alert('Rule saved successfully.');
            document.getElementById('editorContainer').style.display = 'none';
        })
        .catch(error => {
            // The error thrown from above is caught here and its message is displayed
            alert('Error saving rule: ' + error.message);
            console.error('Error:', error);
        });
    } catch (error) {
        // If jsyaml.load throws an error, catch it here
        alert('Error processing YAML: ' + error.message);
        console.error('Error parsing YAML:', error);
    }
}



