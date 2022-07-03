/*=============== SHOW ===============*/
const showModal = (openButton, modalContent) =>{
    const openBtn = document.getElementById(openButton),
    modalContainer = document.getElementById(modalContent)
    
    if(openBtn && modalContainer){
        openBtn.addEventListener('click', ()=>{
            modalContainer.classList.add('show-modal')
        })
    }
}
showModal('open-modal','modal-container')

/*=============== CLOSE ===============*/
const closeBtn = document.querySelectorAll('.close-modal')

function closeModal(){
    const modalContainer = document.getElementById('modal-container')
    modalContainer.classList.remove('show-modal')
}
closeBtn.forEach(c => c.addEventListener('click', closeModal))

// POPUP AJOUT PAR L'ADMINISTRATEUR DU SITE
const Fermer = document.getElementById('fermer')
const Ajouter = document.getElementById('ajouter')
const Add_user = document.querySelector('.add_user')
const Update = document.querySelector('.add_users')
const Modif = document.querySelectorAll('.modif')
const Archive = document.querySelectorAll('.archive')
const li = document.querySelectorAll('li')
const note = document.querySelector('.notification')
const rechercheImg = document.getElementById('rechercheImg')
const formSearch = document.getElementById('formSearch')
const rechercherInput =  document.querySelector('.rechercherInput')
const ImgProfile =  document.querySelector('.img1')


Modif.forEach(modif=>modif.addEventListener('click',(e)=>{
    e.preventDefault()
    Update.style.display='flex'
}))
Ajouter.addEventListener('click',()=>{Add_user.style.display='flex'})
Fermer.addEventListener('click',()=>{Add_user.style.display='none'})

// Display de la barre de recherche
rechercheImg.addEventListener('click',()=>{rechercherInput.style.display='flex'})
rechercheImg.addEventListener('dblclick',()=>{rechercherInput.style.display='none'})

// Voir les profile
ImgProfile.addEventListener('click',()=>{Update.style.display='flex'})
Fermer.addEventListener('click',()=>{Update.style.display='none'})

// ARBRE
// var root;

// var boxWidth = 150,
//     boxHeight = 40,
//     duration = 750; // duration of transitions in ms


// var zoom = d3.behavior.zoom()
//   .scaleExtent([.1,1])
//   .on('zoom', function(){
//     svg.attr("transform", "translate(" + d3.event.translate + ") scale(" + d3.event.scale + ")");
//   })
//   .translate([150, 200]);

// var svg = d3.select("div#arbre").append("svg")
//   .attr('width', 1000)
//   .attr('height', 500)
//   .call(zoom)
//   .append('g')
  
//   .attr("transform", "translate(150,200)");

// var tree = d3.layout.tree()
  
//   .nodeSize([100, 200])
  
//   .separation(function(){
//     return .5;
//   })
  
//   .children(function(person){
    
//     if(person.collapsed){
//       return;
//     } else {
//       return person._parents;
//     }
//   });

// d3.json("../img/8gens.json", function(error, json){
  
//   if(error) {
//     return console.error(error);
//   }
  
//   json._parents.forEach(function(gen2){
//     gen2._parents.forEach(function(gen3){
//       collapse(gen3);
//     });
//   });
  
//   root = json;
  
//   root.x0 = 0;
//   root.y0 = 0;
  
//   draw(root);
      
// });

// function draw(source){
  
//   var nodes = tree.nodes(root),
//       links = tree.links(nodes);

//   // Update links
//   var link = svg.selectAll("path.link")
  
//       .data(links, function(d){ return d.target.id; });
  
//   link.enter().append("path")
//       .attr("class", "link")
//       .attr("d", function(d) {
//         var o = {x: source.x0, y: (source.y0 + boxWidth/2)};
//         return transitionElbow({source: o, target: o});
//       });
    
//   link.transition()
//       .duration(duration)
//       .attr("d", elbow);
  
//   link.exit()
//       .transition()
//       .duration(duration)
//       .attr("d", function(d) {
//         var o = {x: source.x, y: (source.y + boxWidth/2)};
//         return transitionElbow({source: o, target: o});
//       })
//       .remove();

//   // Update nodes    
//   var node = svg.selectAll("g.person")
      
//       .data(nodes, function(person){ return person.id; });
      
//   // Add any new nodes
//   var nodeEnter = node.enter().append("g")
//       .attr("class", "person")
      
//       // Add new nodes at the right side of their child's box.
//       // They will be transitioned into their proper position.
//       .attr('transform', function(person){
//         return 'translate(' + (source.y0 + boxWidth/2) + ',' + source.x0 + ')';
//       })
//       .on('click', togglePerson);

//   nodeEnter.append("rect")
//       .attr({
//         x: 0,
//         y: 0,
//         width: 0,
//         height: 0
//       });

//   // Draw the person's name and position it inside the box
//   nodeEnter.append("text")
//       .attr("dx", 0)
//       .attr("dy", 0)
//       .attr("text-anchor", "start")
//       .attr('class', 'name')
//       .text(function(d) { 
//         return d.name; 
//       })
//       .style('fill-opacity', 0);
  
//   // Update the position of both old and new nodes
//   var nodeUpdate = node.transition()
//       .duration(duration)
//       .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });
      
//   // Grow boxes to their proper size    
//   nodeUpdate.select('rect')
//       .attr({
//         x: -(boxWidth/2),
//         y: -(boxHeight/2),
//         width: boxWidth,
//         height: boxHeight
//       });
  
//   // Move text to it's proper position
//   nodeUpdate.select('text')
//       .attr("dx", -(boxWidth/2) + 10)
//       .style('fill-opacity', 1);
  
//   // Remove nodes we aren't showing anymore
//   var nodeExit = node.exit()
//       .transition()
//       .duration(duration)
      
//       // Transition exit nodes to the source's position
//       .attr("transform", function(d) { return "translate(" + (source.y + boxWidth/2) + "," + source.x + ")"; })
//       .remove();
  
//   // Shrink boxes as we remove them    
//   nodeExit.select('rect')
//       .attr({
//         x: 0,
//         y: 0,
//         width: 0,
//         height: 0
//       });
      
//   // Fade out the text as we remove it
//   nodeExit.select('text')
//       .style('fill-opacity', 0)
//       .attr('dx', 0);
  
//   // Stash the old positions for transition.
//   nodes.forEach(function(person) {
//     person.x0 = person.x;
//     person.y0 = person.y;
//   });
// }

// /**
//  * Update a person's state when they are clicked.
//  */
// function togglePerson(person){
//   if(person.collapsed){
//     person.collapsed = false;
//   } else {
//     collapse(person);
//   }
//   draw(person);
// }

// /**
//  * Collapse person (hide their ancestors). We recursively
//  * collapse the ancestors so that when the person is
//  * expanded it will only reveal one generation. If we don't
//  * recursively collapse the ancestors then when
//  * the person is clicked on again to expand, all ancestors
//  * that were previously showing will be shown again.
//  * If you want that behavior then just remove the recursion
//  * by removing the if block.
//  */
// function collapse(person){
//   person.collapsed = true;
//   if(person._parents){
//     person._parents.forEach(collapse);
//   }
// }
    
// /**
//  * Custom path function that creates straight connecting
//  * lines. Calculate start and end position of links.
//  * Instead of drawing to the center of the node,
//  * draw to the border of the person profile box.
//  * That way drawing order doesn't matter. In other
//  * words, if we draw to the center of the node
//  * then we have to draw the links first and the
//  * draw the boxes on top of them.
//  */
// function elbow(d) {
//   var sourceX = d.source.x,
//       sourceY = d.source.y + (boxWidth / 2),
//       targetX = d.target.x,
//       targetY = d.target.y - (boxWidth / 2);
      
//   return "M" + sourceY + "," + sourceX
//     + "H" + (sourceY + (targetY-sourceY)/2)
//     + "V" + targetX 
//     + "H" + targetY;
// }

// /**
//  * Use a different elbow function for enter
//  * and exit nodes. This is necessary because
//  * the function above assumes that the nodes
//  * are stationary along the x axis.
//  */
// function transitionElbow(d){
//   return "M" + d.source.y + "," + d.source.x
//     + "H" + d.source.y
//     + "V" + d.source.x 
//     + "H" + d.source.y;
// }



