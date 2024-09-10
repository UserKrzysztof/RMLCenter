/*setInterval(function() {
   var logElement = document.getElementById("log");
  var text = logElement.textContent;
  logElement.textContent = text + '\n' + new Date().toISOString();
}, 60 * 1000)*/

class Indexer {
  constructor(){
    this.index = 0;
  }

  next(){
    this.index ++;
  }

  get(){
    return this.index;
  }

}

let indexer = new Indexer();

window.addEventListener('load', function(ev){
  indexer = new Indexer();
})

function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function allowDrop(ev) {
ev.preventDefault(); 
}

function drag(ev) {
ev.dataTransfer.setData("text", ev.target.id); 
}

function drop(ev) {
  ev.preventDefault(); 
  var data = ev.dataTransfer.getData("text"); 
  var nodeCopy = document.getElementById(data).cloneNode(true);
  var dropOutput = document.getElementsByClassName('network-drop-output')[0];

  indexer.next()
  var idx = indexer.get();

  nodeCopy.id = "{'type':'network-layer','index':"+ idx + "}";
  nodeCopy.className = "network-layer";
  nodeCopy.style.display = "flex";
  nodeCopy.style.justifyContent = "space-between";
  nodeCopy.style.alignItems = "center";
  nodeCopy.style.height = '5vh'

  var clearBtn = document.createElement('I');
  clearBtn.id = "{'type':'network-delete-layer-btn','index':"+ idx + "}";
  clearBtn.className = "network-delete-layer-btn fa-solid fa-xmark";

  var showOptionsBtn = document.createElement('I');
  showOptionsBtn.id = '{"index":'+idx+',"type":"network-show-layrs-opt-btn"}';
  showOptionsBtn.className = "network-show-layrs-opt-btn fa-solid fa-chevron-down"

  var mobileMenu = document.createElement('div');
  mobileMenu.id = '{"index":'+ idx +',"type":"network-mobile-menu"}'
  mobileMenu.className = "network-mobile-menu";

  var btnsContainer = document.createElement('div')
  btnsContainer.className = "network-lyrs-btns-cont"

  showOptionsBtn.addEventListener("click", function () {
      if (mobileMenu.style.display === "inline-block") {
          mobileMenu.style.display = "none";
          showOptionsBtn.className = "network-show-layrs-opt-btn fa-solid fa-chevron-down";
      } else {
          mobileMenu.style.display = "inline-block";
          showOptionsBtn.className = "network-show-layrs-opt-btn fa-solid fa-chevron-up"
      }
  });

  clearBtn.addEventListener("click", function(){
    //mobileMenu.removeChild(mobileMenu.firstChild);
    var placeholder = document.getElementById("network-layrs-params-placeholder");
    mobileMenu.firstChild.style.display = 'none';
    placeholder.appendChild(mobileMenu.firstChild);
    /*for (var i = 1; i <= dropOutput.children.length; i= i+2) {
      var outputChild = dropOutput.children[i];

      if (outputChild && outputChild.firstChild) {
          var placeholder = document.getElementById("network-layrs-params-placeholder");
          outputChild.firstChild.style.display = 'none';
          placeholder.appendChild(outputChild.firstChild);
      }
    }*/
    nodeCopy.parentNode.removeChild(nodeCopy)
    mobileMenu.parentNode.removeChild(mobileMenu);
  });

  btnsContainer.appendChild(showOptionsBtn);
  btnsContainer.appendChild(clearBtn);
  nodeCopy.appendChild(btnsContainer);

  if (ev.target.id.length > 9 && ev.target.id[9] === "0") {
      for (var i = 1; i <= dropOutput.children.length; i= i+2) {
          var outputChild = dropOutput.children[i];

          if (outputChild && outputChild.firstChild) {
              var placeholder = document.getElementById("network-layrs-params-placeholder");
              outputChild.firstChild.style.display = 'none';
              placeholder.appendChild(outputChild.firstChild);
          }
      }
      dropOutput.insertBefore(nodeCopy, dropOutput.firstChild);
  } else {
      for (var i = 1; i <= dropOutput.children.length; i= i+2) {
        var outputChild = dropOutput.children[i];

        if (outputChild && outputChild.firstChild) {
            var placeholder = document.getElementById("network-layrs-params-placeholder");
            outputChild.firstChild.style.display = 'none';
            placeholder.appendChild(outputChild.firstChild);
        }
      }
      dropOutput.appendChild(nodeCopy); 
  }

  insertAfter(nodeCopy, mobileMenu)
}


window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    drag_and_drop_handler: function(children) {
        var elementsWithDrop = document.getElementsByClassName('network-drop');
        for (var i = 0; i < elementsWithDrop.length; i++) {
          elementsWithDrop[i].addEventListener('dragover', allowDrop);
          elementsWithDrop[i].addEventListener('drop', drop);
        }

        var elementsWithDraggable = document.getElementsByClassName('network-draggable');
        for (var i = 0; i < elementsWithDraggable.length; i++) {
          elementsWithDraggable[i].addEventListener('dragstart', drag);
        }

        var output = document.getElementById('network-drop-output')
        return  {
        'layers_count': indexer.get(),
        'layers': []
        };
    },

    layers_catcher: function(output_hovered){
      var output = document.getElementById('network-drop-output');
      var layers = [];

      for (var i = 0; i < output.children.length; i = i+2) {
          var layer = output.children[i];
          var layerData = {
              id: layer.id,
              mobile_menu_id: output.children[i+1].id,
              name: layer.children[0].innerHTML
          };

          layers.push(layerData);
      }

      return {
          'layers_count': indexer.get(),
          'layers': layers
      };
    },

    layers_rewriter: function(children){
      var outputChildren = document.getElementById('network-drop-output').children;

      for (var i = 1; i < outputChildren.length; i= i+2) {
          var outputChild = outputChildren[i];

          if (outputChild && !outputChild.firstChild) {
              var newInput = document.getElementById("network-layrs-params-placeholder").children[0];
              if(!newInput){
                  continue;
              }
              newInput.style.display = 'block';
              outputChild.appendChild(newInput);
          }
      }
    }
  }
});