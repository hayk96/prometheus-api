const PROMETHEUS_API_ADDR = window.location.origin;
let filesData = [];
let currentFilename = '';
let codeMirrorInstance;

document.addEventListener('DOMContentLoaded', () => {
   setupEditor();
   setupEventListeners();
   fetchAndDisplayAllRules();
   initializeTheme();
});

function fetchAndDisplayRules() {
   fetch(`${PROMETHEUS_API_ADDR}/api/v1/rules`)
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

function handleFileSelection(event) {
   const selectedIndex = event.target.value;
   const selectedGroup = filesData[selectedIndex];
   currentFilename = selectedGroup.file;
   const preprocessedData = preprocessDataForYaml(selectedGroup);
   document.getElementById('editorContainer').style.display = 'block';
   codeMirrorInstance.setValue(jsyaml.dump(preprocessedData));
   setTimeout(function () {
      codeMirrorInstance.refresh();
   }, 0);
}


function openEditorWithNewFilename(filename) {
   document.getElementById('editorContainer').style.display = 'block';
   codeMirrorInstance.setValue('');
   setTimeout(function () {
      codeMirrorInstance.refresh();
   }, 0);
   currentFilename = filename;
}

/**
 * This function processes the data before it's sent
 * to the YAML editor. The function filters rules
 * based on their type and formats them accordingly.
 */
function preprocessDataForYaml(group) {
   let processedRules = group.rules.map(rule => {

      let baseRule = {
         alert: rule.name,
         expr: rule.query,
         labels: rule.labels,
         annotations: rule.annotations
      };

      if (rule.type === 'alerting') {

         baseRule.for = convertDurationToHumanReadable(rule.duration);
      } else if (rule.type === 'recording') {

         baseRule.record = baseRule.alert;
         delete baseRule.alert;
      }

      return baseRule;
   });

   return {
      name: group.name,
      rules: processedRules
   };
}


/**
 * This function is used to convert durations
 * from seconds into a more readable format.
 */
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
   } else if (duration >= 0) {
      result += duration + 'ms';
   }

   return result;
}


async function saveRule() {
   const editedYaml = codeMirrorInstance.getValue();
   try {
      const modifiedData = jsyaml.load(editedYaml);

      if (!modifiedData) {
         throw new Error('The YAML is empty or not structured correctly.');
      }
      const payload = JSON.stringify({
         data: modifiedData
      });
      const filename = currentFilename ? encodeURIComponent(currentFilename.split('/').pop()) : '';
      const url = `${PROMETHEUS_API_ADDR}/api/v1/rules/${filename}${currentFilename ? '?recreate=true' : ''}`;

      const response = await fetch(url, {
         method: 'PUT',
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

      fetchAndDisplayAllRules();

      document.getElementById('rulesList').style.display = 'block';
   } catch (error) {
      displayModal(`Error saving rule: ${error.message}`);
      console.error('Error:', error);
   } finally {
      document.getElementById('editorContainer').style.display = 'none';
      codeMirrorInstance.setValue('');
      currentFilename = '';
   }
}


function displayModal(message) {
   var modal = document.getElementById("myModal");
   var text = document.getElementById("modal-text");
   var span = document.getElementsByClassName("close")[0];

   text.textContent = message;
   modal.style.display = "block";

   span.onclick = function () {
      modal.style.display = "none";
   }

   window.onclick = function (event) {
      if (event.target === modal) {
         modal.style.display = "none";
      }
   }
}

function displayRulesList(groups) {
   const rulesListElement = document.getElementById('rulesList');
   rulesListElement.innerHTML = '';

   const rulesByFilename = groups.reduce((acc, group) => {
      const filename = group.file.split('/').pop();
      if (!acc[filename]) {
         acc[filename] = {
            filename: filename,
            types: [],
            path: group.file,
            groupIndex: groups.indexOf(group)
         };
      }

      group.rules.forEach(rule => {
         if (!acc[filename].types.includes(rule.type)) {
            acc[filename].types.push(rule.type);
         }
      });
      return acc;
   }, {});

   Object.values(rulesByFilename).forEach(({
      filename,
      types,
      path,
      groupIndex
   }) => {
      const ruleItem = document.createElement('div');
      ruleItem.className = 'rule-item';

      const filenameDiv = document.createElement('div');
      filenameDiv.textContent = filename;
      filenameDiv.className = 'filename';
      ruleItem.appendChild(filenameDiv);

      types.forEach(type => {
         const typeLabel = document.createElement('span');
         typeLabel.textContent = type.charAt(0).toUpperCase() + type.slice(1);
         typeLabel.className = `rule-type ${type.toLowerCase()}`;
         ruleItem.appendChild(typeLabel);
      });

      const buttonsContainer = document.createElement('div');
      buttonsContainer.className = 'buttons-container';

      const editIcon = document.createElement('img');
      editIcon.className = 'edit-rule-icon';

      const editButton = document.createElement('button');
      editButton.className = 'edit-rule-btn';
      editButton.appendChild(editIcon);
      editButton.addEventListener('click', () => editRule(path));
      buttonsContainer.appendChild(editButton);

      const removeIcon = document.createElement('img');
      removeIcon.className = 'remove-rule-icon';

      const deleteButton = document.createElement('button');
      deleteButton.className = 'remove-rule-btn';
      deleteButton.appendChild(removeIcon);
      deleteButton.addEventListener('click', () => removeRule(path, groupIndex));
      buttonsContainer.appendChild(deleteButton);

      ruleItem.appendChild(buttonsContainer);
      rulesListElement.appendChild(ruleItem);
   });
}

/**
 * This function fetches specific rule data when
 * a file is selected for editing. The function
 * should ensure that all groups within the selected
 * file are processed and displayed in the editor.
 */
function editRule(filePath) {
   currentFilename = filePath;
   fetch(`${PROMETHEUS_API_ADDR}/api/v1/rules?file[]=${encodeURIComponent(currentFilename)}`)
      .then(response => response.json())
      .then(data => {
         if (!data || !data.data || !data.data.groups) {
            console.error('Invalid structure in response:', data);
            alert('No rules data found for the file.');
            return;
         }

         let groupsContent = data.data.groups
            .filter(group => group.file === currentFilename)
            .map(preprocessDataForYaml);

         let yamlContent = jsyaml.dump({
            groups: groupsContent
         }, {
            indent: 2
         });

         if (yamlContent) {
            codeMirrorInstance.setValue(yamlContent);
            document.getElementById('editorContainer').style.display = 'block';
            document.getElementById('rulesList').style.display = 'none';
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
   const cancelBtn = document.getElementById('cancelBtn');
   if (cancelBtn) {
      cancelBtn.classList.remove('gray-btn');
   }
   document.getElementById('editorContainer').style.display = 'none';
   document.getElementById('rulesList').style.display = 'block';
   codeMirrorInstance.setValue('');
   currentFilename = '';
}

function fetchRuleDetails(filePath) {
   fetch(`${PROMETHEUS_API_ADDR}/api/v1/rules?file[]=${encodeURIComponent(filePath)}`)
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

   const searchInput = document.getElementById('searchInput');
   if (searchInput) {
      searchInput.addEventListener('input', handleSearchInput);
   } else {
      console.error('Search input not found');
   }

   const createRuleBtn = document.getElementById('createRuleBtn');
   if (createRuleBtn) {
      createRuleBtn.addEventListener('click', openCreateRuleModal);
   } else {
      console.error('Create rule button not found');
   }

   const submitNewRuleBtn = document.getElementById('submitNewRule');
   if (submitNewRuleBtn) {
      submitNewRuleBtn.addEventListener('click', submitNewRule);
   } else {
      console.error('Submit new rule button not found');
   }

   const cancelCreateRuleBtn = document.getElementById('cancelCreateRuleBtn');
   if (cancelCreateRuleBtn) {
      cancelCreateRuleBtn.addEventListener('click', function () {
         document.getElementById('editorContainer').style.display = 'none';
         document.getElementById('createRuleModal').style.display = 'none';
         codeMirrorInstance.setValue('');
         document.getElementById('rulesList').style.display = 'block';
         currentFilename = '';
      });
   } else {
      console.error('Cancel Create Rule Button not found');
   }

   document.getElementById('editAlertingRulesBtn')?.addEventListener('click', () => fetchAndDisplayRules('alert'));
   document.getElementById('editRecordingRulesBtn')?.addEventListener('click', () => fetchAndDisplayRules('record'));
   document.getElementById('fileSelector')?.addEventListener('change', handleFileSelection);
   document.getElementById('saveBtn')?.addEventListener('click', saveRule);
   document.getElementById('cancelBtn')?.addEventListener('click', cancelEdit);
   document.getElementById('applyBtn')?.addEventListener('click', applyChanges);
   document.getElementById('homeBtn').addEventListener('click', function () {
      window.location.href = PROMETHEUS_API_ADDR;
   });
   document.getElementById('prometheusBtn').addEventListener('click', function () {
      window.location.href = PROMETHEUS_API_ADDR + "/graph";
   });
}

/**
 * This function fetches all rules and
 * displays them using displayRulesList
 */
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
      fetch(`${PROMETHEUS_API_ADDR}/api/v1/rules/${encodeURIComponent(filenameOnly)}`, {
            method: 'DELETE',
            headers: {
               'Content-Type': 'application/json'
            }
         })
         .then(response => {
            if (response.ok && response.status === 204) {

               return null;
            } else if (!response.ok) {

               return response.json().then(err => {
                  throw new Error(err.message || `HTTP error! status: ${response.status}`);
               });
            }
            return response.json();
         })
         .then(data => {
            if (data) {

               displayModal(data.message || 'Rule deleted successfully.');
            } else {

               displayModal('Rule deleted successfully.');
            }

            fetchAndDisplayRules();
         })
         .catch(error => {
            displayModal(`Error deleting rule: ${error.message}`);
            console.error('Error:', error);
         })
         .finally(() => {

            deleteModal.style.display = 'none';
            confirmDeleteBtn.removeEventListener('click', confirmDeletion);
            cancelDeleteBtn.removeEventListener('click', cancelDeletion);
         });
   }

   function cancelDeletion() {
      deleteModal.style.display = 'none';
      confirmDeleteBtn.removeEventListener('click', confirmDeletion);
      cancelDeleteBtn.removeEventListener('click', cancelDeletion);
   }

   confirmDeleteBtn.addEventListener('click', confirmDeletion);
   cancelDeleteBtn.addEventListener('click', cancelDeletion);
}


function handleSearchInput(event) {
   const searchTerm = event.target.value.toLowerCase();

   const filteredGroups = filesData.filter(group =>
      group.file.toLowerCase().includes(searchTerm)
   );

   displayRulesList(filteredGroups);
}

function applyChanges() {
   const editedYaml = codeMirrorInstance.getValue();
   try {
      const modifiedData = jsyaml.load(editedYaml);
      if (!modifiedData) {
         throw new Error('The YAML is empty or not structured correctly.');
      }
      const payload = JSON.stringify({
         data: modifiedData
      });
      const filename = currentFilename ? encodeURIComponent(currentFilename.split('/').pop()) : '';
      const url = `${PROMETHEUS_API_ADDR}/api/v1/rules/${filename}${currentFilename ? '?recreate=true' : ''}`;

      fetch(url, {
            method: 'PUT',
            headers: {
               'Content-Type': 'application/json'
            },
            body: payload
         })
         .then(response => {
            if (!response.ok) {
               return response.json().then(err => {
                  throw new Error(err.message || `HTTP error! status: ${response.status}`);
               });
            }
            return response.json();
         })
         .then(() => {
            displayModal('Changes applied successfully.');
            fetchAndDisplayRules();
         })
         .catch(error => {
            displayModal(`Error applying changes: ${error.message}`);
            console.error('Error:', error);
         });
   } catch (error) {
      displayModal(`Error processing YAML: ${error.message}`);
      console.error('Error parsing YAML:', error);
   }
}

function openCreateRuleModal() {
   const modal = document.getElementById('createRuleModal');
   const newRuleNameInput = document.getElementById('newRuleName');
   newRuleNameInput.value = '';
   newRuleNameInput.focus();
   modal.style.display = 'block';

   document.getElementById('rulesList').style.display = 'none';
   document.getElementById('editorContainer').style.display = 'block';
   codeMirrorInstance.setValue('');
   currentFilename = '';

   setTimeout(function () {
      codeMirrorInstance.refresh();
   }, 0);

   const cancelBtn = document.getElementById('cancelBtn');
   if (cancelBtn) {
      cancelBtn.classList.add('gray-btn');
   }
}

function closeCreateRuleModal() {
   const modal = document.getElementById('createRuleModal');
   modal.style.display = 'none';
}

function submitNewRule() {
   const newRuleNameInput = document.getElementById('newRuleName');
   const newRuleName = newRuleNameInput.value.trim();
   const createRuleError = document.getElementById('createRuleError');
   createRuleError.textContent = '';

   if (newRuleName === '') {
      createRuleError.textContent = 'Please enter a filename for the new rule.';
      return;
   }

   if (filesData.some(group => group.file.split('/').pop() === newRuleName)) {
      createRuleError.textContent = 'A rule with this filename already exists. Please enter another name.';
      return;
   }

   document.getElementById('createRuleModal').style.display = 'none';
   currentFilename = newRuleName;
   document.getElementById('editorContainer').style.display = 'block';
   codeMirrorInstance.setValue('');
   codeMirrorInstance.focus();
   openEditorWithNewFilename(newRuleName);
}

/**
 * This function is responsible for initializing
 * and managing the theme switching functionality
 * of a Rules Management page.
 */
function initializeTheme() {
    const themeSwitcher = document.getElementById('themeSwitcher');
    const themeIcon = document.getElementById('themeIcon');
    const lightIcon = themeSwitcher.getAttribute('data-to-dark-icon');
    const darkIcon = themeSwitcher.getAttribute('data-to-light-icon');
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        themeIcon.src = darkIcon;
    }

    themeSwitcher.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        themeIcon.src = isDarkMode ? darkIcon : lightIcon;
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    });
}