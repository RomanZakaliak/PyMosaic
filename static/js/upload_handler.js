let input = document.querySelector(".custom-file #file");
let formGroup = document.querySelector(".form-group");

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
        formGroup.appendChild(image);
        image.src = fileReader.result;
    });
}

input.addEventListener('change', doUpload, false);