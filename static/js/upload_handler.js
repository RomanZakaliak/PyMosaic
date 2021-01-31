let input = document.querySelector(".custom-file #file");
let imageWrapper = document.querySelector(".row .col-6");

const doUpload = () => {
    let data = new FormData();
    data.append('file', input.files[0]);

    fetch('/upload_file', {
        method: 'POST',
        body: data
    });

    const fileReader = new FileReader();
    fileReader.readAsDataURL(input.files[0]);
    fileReader.addEventListener('load', ()=>{
        const image = new Image();

        if(imageWrapper.childElementCount > 0){
            imageWrapper.childNodes[0].remove();
        }
        else{
            imageWrapper.appendChild(image);
        }

        image.src = fileReader.result;
        image.classList.add('img-fluid', 'ml-auto');
    });
}

input.addEventListener('change', doUpload, false);