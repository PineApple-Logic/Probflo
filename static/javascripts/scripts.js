let currentNodeType = 'bar'; // Default chart type
var contextmenus = [] ; 

const stateColorMapping = {};

function getColorForState(stateName) {
  if (!stateColorMapping[stateName]) {
    // Generate a random color for new states
    stateColorMapping[stateName] = getRandomColor();
  }
  return stateColorMapping[stateName];
}

function getRandomColor() {
  const randomChannel = () => Math.floor(Math.random() * 155 + 100); // Generate a value between 100 and 255
  const red = randomChannel();
  const green = randomChannel();
  const blue = randomChannel();
  return `rgb(${red}, ${green}, ${blue})`;
  }

function showChart(chartType) {
  currentNodeType = chartType;
  updateNodeCharts();
}

function updateNodeCharts() {
  const nodeGraphsContainer = document.getElementById('nodeGraphsContainer');
  const nodeListBtns = document.getElementById("nodeListBtns");
  nodeGraphsContainer.innerHTML = ''; // Clear previous content
  var nodeListBtnsHtml = "";
   
  nodeData.forEach(node => {
    const nodeGraph = document.createElement('div');
    nodeGraph.style.left = node.left; 
    nodeGraph.style.top = node.top; 
    nodeGraph.setAttribute("id", node.name);
    nodeGraph.setAttribute("data-children", node.children.join(" "));
    nodeGraph.setAttribute("data-contextmenu",node.name)
    nodeGraph.classList.add('node-graph');
    nodeListBtnsHtml += `<a href="#">${node.name}</a>`; 
    const nodeChartContainer = document.createElement('div');
    nodeChartContainer.classList.add('node-chart-container');
    nodeChartContainer.innerHTML = `<h3>${node.name}</h3>`;
    if (!node.values.length && node.parents.length){
      nodeChartContainer.innerHTML += `<span style="color:red;position:absolute; left:30%; bottom:-30px;font-size:18px ">Not Specified CPD Parent</span>`;
    }
    
    nodeGraph.appendChild(nodeChartContainer);
    nodeGraphsContainer.appendChild(nodeGraph);
    const ctx = document.createElement('canvas');
    ctx.classList.add('node-chart');
    nodeChartContainer.appendChild(ctx);
    const chartConfig = {
      type: currentNodeType,
      data: {
        labels: node.states.map(state => state.name),
        datasets: [{
          label: node.name,
          data: node.states.map(state => state.probability),
          backgroundColor: node.states.map(state => getColorForState(state.name)),
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        title: {
          display: false
        }
      }
    };
    new Chart(ctx, chartConfig);
    dragElement(nodeGraph);
    const circles = [
      { className: "circle top" },
      { className: "circle right" },
      { className: "circle bottom" },
      { className: "circle left" }
    ]
    for (const circle of circles) {
      let elem = document.createElement("div")
      elem.setAttribute("class", circle.className);
      nodeGraph.appendChild(elem);
    }        
    let delButton = document.createElement("button")
    delButton.appendChild(document.createTextNode("X"));
    delButton.setAttribute("class", "delete-node-btn visible");
    delButton.setAttribute("onclick", `deleteNode('${node.name}')`);
    nodeGraph.appendChild(delButton);
  });

  nodeListBtnsHtml += `<a href="#" onclick="addNode()">Add Node</a>`;
  nodeListBtns.innerHTML = nodeListBtnsHtml;


  if (init){
    socket.emit('update_node_data', { data: nodeData });
  }
  drawArrows();
 
    
   
  for (let node of nodeData) {
    const options = [
      { label: 'Edit Node', handler: (index) => console.log(`Option 1 clicked for ${node.name}`), shortcut: 'Ctrl+1' },
      { label: 'Delete Node', handler: (index) => deleteNode(node.name), shortcut: 'Ctrl+2' },
      { label: 'Add Parent Node', handler: (index) => console.log('Option 3 clicked for element 1'), shortcut: 'Ctrl+3' },
      { label: 'Add Child Node', handler: (index) =>{

        let child = prompt("Mention the child node") ; 
        let parent_node = nodeData.find(({name}) =>{ return name  == node.name} )
        parent_node.children.push(child) ;
        let child_node = nodeData.find(({name}) =>{ return name  == child})
        child_node.parents.push(node.name);  
        updateNodeCharts()

        drawArrows(); 
      }, shortcut: 'Ctrl+1' },
      { label: 'View Probabilities', handler: (index) => console.log('Option 2 clicked for element 1'), shortcut: 'Ctrl+2' },
      { label: 'Run Inferences', handler: (index) => console.log('Option 3 clicked for element 1'), shortcut: 'Ctrl+3' },
      { label: 'Visualise CPT', handler: (index) => console.log('Option 1 clicked for element 1'), shortcut: 'Ctrl+1' },
      { label: 'Export Node', handler: (index) => console.log('Option 2 clicked for element 1'), shortcut: 'Ctrl+2' },
      // { label: 'Option 3', handler: (index) => console.log('Option 3 clicked for element 1'), shortcut: 'Ctrl+3' }
    ];
  new ContextMenu(node.name, [ ...options]);
    
    
  }
  
}





function drawArrows() {
  const svgElements = document.body.querySelectorAll("svg");
  svgElements.forEach(function(svgElement) {
    svgElement.remove();
  });
  nodeData.forEach(node => {
    const sourceElement = document.getElementById(node.name);
    try{
      node.children.forEach(childName => {
        const destinationElement = document.getElementById(childName);
          const line = new LeaderLine(sourceElement, destinationElement, {
            startPlug: 'disc',
            endPlug: 'arrow3',
            color: 'rgba(250, 250, 250, 0.7)',
            startPlugColor: 'rgb(241, 76, 129)',
            endPlugColor: 'rgba(241, 76, 129, 0.5)',
            startPlugSize: 5,
            endPlugSize: 8,
            endPlugOutline: true,
            middleLabel: LeaderLine.captionLabel({
              text: `P( ${childName} | ${node.name} )`,
              color: 'whitesmoke',
              outlineColor: '',
              fontWeight: "500",
              fontSize:"20px"
            }),
          });
          line.size = 0.5; 
      });
    }catch{}
    
  });
}

function deleteNode(id) {
  let indexToDelete = nodeData.findIndex(({ name }) => name === id);

  if (indexToDelete !== -1) {
    nodeData.splice(indexToDelete, 1);
    updateNodeCharts();
  } else {
    console.log("Node not found");
  }
}
// Initial chart display
updateNodeCharts();


// Dropdown toggle functionality
$(document).ready(function() {
  $('.dropdown-toggle').click(function() {
    $(this).siblings('.dropdown-content').toggleClass('show');
  });
});

