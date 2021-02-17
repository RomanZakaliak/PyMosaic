"use strict"

let selectedArea = {
    x1:0,
    y1:0,
    x2:0,
    y2:0
}

function addSelectionArea(window){
    const selection_wrapper = window.document.querySelector('.selection_wrapper');
    let selection_area = window.document.querySelector('.selection_area');
    let overlay = window.document.querySelector('.overlay');

    (()=>{
        if(overlay == null){
            overlay = window.document.createElement('div');
            overlay.classList.add('overlay');
            selection_wrapper.appendChild(overlay);
        }
        if(selection_area == null){
            selection_area = window.document.createElement('canvas');
            selection_area.classList.add('selection_area');
            selection_area.hidden = 1;
            overlay.appendChild(selection_area);
        }
    })();

    const ctx = selection_area.getContext('2d');
    let image = window.document.querySelector('img.selection_target');
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    image.ondragstart = ()=>{return false};

    let coords = {
        x1: 0,
        x2: 0,
        y1: 0,
        y2: 0,
        selected: false
    }

    let docOffset = {
        left: window.document.documentElement.scrollLeft,
        top: window.document.documentElement.scrollTop
    }

    const getPageOffset = (element) => {
        const rect = element.getBoundingClientRect();
        return {
            x: rect.x,
            y: rect.y
        }
    }

    let imgWidthIndex = 0; 
    let imgHeightIndex = 0;
    image.addEventListener('load', ()=>{
        imgWidthIndex = image.naturalWidth/image.clientWidth;
        imgHeightIndex = image.naturalHeight/image.clientHeight;
    });

    const reassign = () =>{
        addSelectionArea(window);
    }

    window.addEventListener('resize', ()=>{
        image = window.document.querySelector('img.selection_target');
        imgWidthIndex = image.naturalWidth/image.clientWidth;
        imgHeightIndex = image.naturalHeight/image.clientHeight;
    });

    const redraw = () =>{
        let {x, y} = getPageOffset(image);
        let selection_left_min = Math.min(coords.x1, coords.x2);
        let selection_left_max = Math.max(coords.x1, coords.x2);
        let selection_top_min = Math.min(coords.y1, coords.y2);
        let selection_top_max = Math.max(coords.y1, coords.y2);

        selection_area.style.left = selection_left_min - x + 'px';
        selection_area.style.top =  selection_top_min - y + 'px';
        selection_area.style.width = (selection_left_max - selection_left_min)+ 'px';
        selection_area.style.height = (selection_top_max - selection_top_min) + 'px';

        let image_x1 = (selection_left_min - x) * imgWidthIndex;
        let image_y1 = (selection_top_min - y) * imgHeightIndex;
        let image_x2 = (selection_left_max - selection_left_min) * imgWidthIndex;
        let image_y2 = (selection_top_max - selection_top_min) * imgHeightIndex; 
        ctx.clearRect(0, 0, selection_area.width, selection_area.height);
        ctx.drawImage(image, image_x1, image_y1, image_x2, 
            image_y2, 0, 0, selection_area.width, selection_area.height);
    }

    image.onmousedown = (event)=>{
        overlay.style.width = `${image.width}px`;
        overlay.style.height = `${image.height}px`;
        selection_area.hidden = 0;
        coords.selected = true;
        coords.x1 = coords.x2 = event.clientX + docOffset.left;
        coords.y1 = coords.y2 = event.clientY + docOffset.top;
        redraw();
        image.style.filter = 'blur(2px)';
        selectedArea.x1 = (coords.x1 - getPageOffset(image).x)*imgWidthIndex;
        selectedArea.y1 = (coords.y1 - getPageOffset(image).y)*imgHeightIndex; 
    }

    window.document.onmousemove = (event)=>{
        if(!coords.selected) {return false;}
        let {x, y} = getPageOffset(image);
        let pointerX = event.clientX + docOffset.left; 
        let pointerY = event.clientY + docOffset.top;
        coords.x2 = (pointerX < image.width+x)?(pointerX>x)?pointerX:x:image.width+x;
        coords.y2 = (pointerY < image.height+y)?(pointerY>y)?pointerY:y:image.height+y;
        redraw();
    }

    window.document.onmouseup = (event)=>{
        if(!coords.selected) {return false;}
        coords.selected = false;
        selectedArea.x2 = (coords.x2 - getPageOffset(image).x)*imgWidthIndex;
        selectedArea.y2 = (coords.y2 - getPageOffset(image).y)*imgHeightIndex; 
        console.log(selectedArea);
    }

}