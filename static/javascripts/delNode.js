function isbin(elem){
    
    // document.getElementsByTagName("body")[0].style.backgroundColor = "red" ; 
 const bin = document.getElementById("delNode"); 
 let pos = bin.getBoundingClientRect()
//  console.log(pos)
 let x1 = pos.left , x2 = pos.right ;
 let y1 = pos.bottom , y2 = pos.top ;

 // elem coords
 let x = elem.style.left.replace("px","") ;
 let y = elem.style.top.replace("px","")


}

