
function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(elmnt.id )) {
      /* if present, the header is where you move the DIV from:*/
      document.getElementById(elmnt.id).onmousedown = dragMouseDown;
    } else {
      /* otherwise, move the DIV from anywhere inside the DIV:*/
      elmnt.onmousedown = dragMouseDown;
    }
  
    function dragMouseDown(e) {
      e = e || window.event;
      e.preventDefault();
      // get the mouse cursor position at startup:
      pos3 = e.clientX;
      pos4 = e.clientY;
      document.onmouseup = closeDragElement;
      // call a function whenever the cursor moves:
      document.onmousemove = elementDrag;
      for(const circle of Array.from(elmnt.children).slice(1,4)){
        circle.classList.add('visible');  
      }
      
    }
  
    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      // calculate the new cursor position:
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
      // set the element's new position:
      elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
      elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
      elmnt.classList.add('dragging');
      drawArrows();
    }
  
    function closeDragElement() {
      /* stop moving when mouse button is released:*/
      document.onmouseup = null;
      document.onmousemove = null;
      let node = elmnt.children[0].children[0].innerText ; 
      elem = nodeData.find(({name})=> name == node )
      elem.left = elmnt.style.left; 
      elem.top = elmnt.style.top;
      elmnt.classList.remove('dragging');
      socket.emit('update_node_data', { data: nodeData });
      
      // updateNodeCharts()
      for(const circle of Array.from(elmnt.children).slice(1,4)){
        circle.classList.remove('visible');
        
        let parentsNode = document.getElementById(elem.name).getAttribute('data-children') ; 
        if(parentsNode){
            let parent = document.getElementById(parentsNode);
          
            let parentCircles = document.getElementById(parentsNode).children
            let rectx = document.getElementById(parentsNode).children[2].getBoundingClientRect().x ; 
            let recty = document.getElementById(parentsNode).children[2].getBoundingClientRect().y ; 

          //  arrow1.update({source: {x: rectx, y: recty}, destination: {x:document.getElementById(elem.name).children[4].getBoundingClientRect().x , y: document.getElementById(elem.name).children[4].getBoundingClientRect().y}});
          
        }
      }
    }
   
  }