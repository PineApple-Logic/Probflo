var data = []; // Array to store dictionary objects
  
  document.getElementById("doneNodeBtn").addEventListener("click", ()=>{
  

$("#modal").hide(); 
  
let newNode = {
    name: document.getElementById("nodeName").value,
    left:"300px",
  top:"300px",
    states: [...data ],
    children:[],
    values: [],
    parents:[],
  }; 
  
  data = [];
  nodeData.push(newNode);
  updateNodeCharts()  
})


function addNode(){
   
  const tableBody = document.getElementById("tableBody");
  const dataForm = document.getElementById("dataForm");
  const stateNameInput = document.getElementById("stateName");
  const stateValueInput = document.getElementById("stateValue");
  const addRowButton = document.getElementById("addRowButton");
  const errorMessage = document.getElementById("errorMessage");

$("#modal").show();
  dataForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const newStateName = stateNameInput.value;
    const newStateValue = parseFloat(stateValueInput.value);

    if (newStateName && !isNaN(newStateValue)) {
      const newRow = document.createElement("tr");
      const newNodeCell = document.createElement("td");
      const newValueCell = document.createElement("td");
      const actionsCell = document.createElement("td");

      const rowCount = tableBody.childElementCount + 1;
      data.push({ name: newStateName, probability: newStateValue });

      newNodeCell.textContent = newStateName;
      newValueCell.textContent = newStateValue.toFixed(2);
      const removeButton = document.createElement("button");
      removeButton.textContent = "Remove Row";
      removeButton.className = "remove-button";
      removeButton.addEventListener("click", () => {
        tableBody.removeChild(newRow);
        data = data.filter(entry => entry.name !== newStateName); // Remove corresponding data entry
        updateSum();
      });
      actionsCell.appendChild(removeButton);

      newRow.appendChild(newNodeCell);
      newRow.appendChild(newValueCell);
      newRow.appendChild(actionsCell);
      tableBody.appendChild(newRow);
      // Clear form inputs
      stateNameInput.value = "";
      stateValueInput.value = "";
      updateSum();
    }

  }
  );

  function updateSum() {
    const sum = data.reduce((total, entry) => total + entry.probability, 0);
    if (sum >= 1) {
      addRowButton.disabled = true;
      errorMessage.textContent = "Sum of values is equal to or greater than 1.";
    } else {
      addRowButton.disabled = false;
      errorMessage.textContent = "";
    }
  }
$("#modal").show();
 }
function hideModal(){
  $("#modal").hide();
  document.getElementById("doneNodeBtn").removeEventListener('click',()=>{}); 
}

function showModal(){
  $("#modal").hide();
}