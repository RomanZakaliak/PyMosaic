let input = document.querySelector('.custom-file #file');
let imageWrapper = document.querySelector('.d-flex.justify-content-center .col-6');
let chunkSize = document.querySelector('#chunk-sizes');
let uploadBtn = document.querySelector('#upload');
let loader = document.querySelector('#loader');

const displayPreview = () => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(input.files[0]);
    fileReader.addEventListener('load', ()=>{
        const image = document.createElement('img');

        image.src = fileReader.result;
        image.classList.add('img-fluid');

        if(imageWrapper.firstChild){
            imageWrapper.replaceChild(image, imageWrapper.firstChild);
        }else{
            imageWrapper.appendChild(image);
        }
    });
}



const sendOnServer = async objToSend => {
    try{
        let response = await fetch('/upload_file', objToSend);
        let data = null;
        if(response.ok){
            data = await response.json();
        } else{
            throw new Error('Request complete with errors!');
        }
        loader.classList.toggle('animation-placeholder');
        const image = new Image();
        image.src = `/download/${data.filename}`;
        image.classList.add('img-fluid');

        let a = document.createElement('a');
        a.href = image.src;
        a.download = data.filename;
        a.appendChild(image);
        imageWrapper.replaceChild(a, imageWrapper.firstChild);

    } catch(error){
        console.log(error);
        loader.classList.toggle('animation-placeholder');
    }
}

const upload = ()=> {
    if(input.files.length == 0) return;

    let data = new FormData();
    data.append('file', input.files[0]);
    data.append('chunk_size', chunkSize.value);
    loader.classList.toggle('animation-placeholder');

    let objToSend = {
        method: 'POST',
        body: data
    };
    sendOnServer(objToSend);
}

input.addEventListener('change', displayPreview, false);
uploadBtn.addEventListener('click', upload, false);