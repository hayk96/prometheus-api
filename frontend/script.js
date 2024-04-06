let currentFilename = '';
let codeMirrorInstance;
let filesData = [];

function preprocessDataForYaml(selectedGroup) {
    let cleanGroupData = JSON.parse(JSON.stringify(selectedGroup));

    delete cleanGroupData.file;
    delete cleanGroupData.interval;
    delete cleanGroupData.limit;
    delete cleanGroupData.evaluationTime;
    delete cleanGroupData.lastEvaluation;

    cleanGroupData.rules = cleanGroupData.rules.map(rule => {
        return {
            alert: rule.name,
            expr: rule.query,
            for: convertDurationToHumanReadable(rule.duration),
            labels: rule.labels,
            annotations: rule.annotations
        };
    });

        if (selectedGroup.type === 'alerting') {
        cleanGroupData.rules = cleanGroupData.rules.map(rule => {
            return {
                alert: rule.name,
                expr: rule.query,
                for: convertDurationToHumanReadable(rule.duration),
                labels: rule.labels,
                annotations: rule.annotations
            };
        });
    } else if (selectedGroup.type === 'recording') {
        cleanGroupData.rules = cleanGroupData.rules.map(rule => {
            return {
                alert: rule.name,
                expr: rule.query,
                labels: rule.labels,
                annotations: rule.annotations
            };
        });
    }

    return { groups: [cleanGroupData] };
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
        const selectedGroup = filesData[selectedIndex];
        currentFilename = selectedGroup.file;
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
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                alert('Rule saved successfully.');
            })
            .catch(error => {
                alert('Error saving rule.');
                console.error('Error:', error);
            });
        } catch (error) {
            alert('Error processing YAML.');
            console.error('Error parsing YAML:', error);
        }
    });
});

function fetchAndDisplayRules(ruleType) {
    fetch(`http://localhost:5000/api/v1/rules?type=${ruleType}`)
        .then(response => response.json())
        .then(json => {
            filesData = json.data.groups;
            const fileSelector = document.getElementById('fileSelector');
            fileSelector.innerHTML = '';
            json.data.groups.forEach((group, index) => {
                const option = new Option(group.file, index);
                option.value = index;
                fileSelector.add(option);
            });
            fileSelector.style.display = 'block';
            fileSelector.selectedIndex = -1;
        })
        .catch(error => {
            console.error(`Error fetching ${ruleType} rules:`, error);
        });
}