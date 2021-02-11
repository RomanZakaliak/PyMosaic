const fileInput = document.querySelector('.custom-file #file');
const imageWrapper = document.querySelector('.d-flex.justify-content-center .col-6');
const chunkSize = document.querySelector('.form-control.form-control-sm');
const uploadForm = document.querySelector('#form-upload');
const loader = document.querySelector('#loader');
const contantWrapper = document.querySelector('.content-wrapper');


const elementCreator = (tagName, ...classList) =>{
    let element = document.createElement(tagName);
    element.classList.add(...classList);
    return element;
}

const displayPreview = () => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(fileInput.files[0]);
    fileReader.addEventListener('load', ()=>{
        const image = document.createElement('img');

        image.src = fileReader.result;
        image.width = window.innerWidth/4;
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
        const image = elementCreator('img', 'img-fluid');
        image.width = window.innerWidth/4;
        image.src = `/thumbnails/thum_${data.filename}`;

        let downloadLink = elementCreator('a');
        downloadLink.href = `/download/${data.filename}`;
        downloadLink.download = data.filename;
        downloadLink.appendChild(image);
        imageWrapper.replaceChild(downloadLink, imageWrapper.firstChild);

    } catch(error){
        console.log(error);
        loader.classList.toggle('animation-placeholder');
    }
}

const upload = event => {
    event.preventDefault();
    try{
        [fileInput, chunkSize].forEach(item => {
            if(!item.validity.valid ){
                if(item.parentNode.lastElementChild.classList.contains('invalid-feedback')){
                    throw new Error('Form invalid');
                }
                var errorText = elementCreator('p','invalid-feedback');
                if(item.type == 'file'){
                    errorText.innerText = "Please, select file for process!";
                } else{
                    errorText.innerText = "Chunk size must be in range of 2 to 1000!";
                }
                item.parentElement.appendChild(errorText);
                throw new Error('Form ivalid!');
            }
        });
    } catch(error){
        console.error(error);
        return;
    }

    let data = new FormData();
    data.append('file', fileInput.files[0]);
    data.append('chunk_size', chunkSize.value);
    loader.classList.toggle('animation-placeholder');

    let objToSend = {
        method: 'POST',
        body: data
    };
    sendOnServer(objToSend);
}

fileInput.addEventListener('change', displayPreview, false);
uploadForm.addEventListener('submit', upload, false);
[fileInput, chunkSize].forEach(item => {
    item.addEventListener('focus', ()=>{
        let errorArea = item.parentNode.lastElementChild;
        if(errorArea.classList.contains('invalid-feedback')){
            errorArea.remove();
        }
    });
}); 

