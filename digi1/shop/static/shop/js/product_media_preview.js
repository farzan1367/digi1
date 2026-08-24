document.addEventListener('change', function (event) {

    if (!event.target.matches('input[type="file"]')){
        return;
    }
    const input = event.target;
    const file = input.files[0];

    if(!file){
        return;
    }
    const row = input.closest('tr');

    if (!row){
        return;
    }

    const preview = row.querySelector('.field-media_preview');

    if (!preview){
        return;
    }

    const oldMedia = preview.querySelector('img,video');
    if (oldMedia){
        oldMedia.remove();
    }
    const url = URL.createObjectURL(file);

    if (file.type.startsWith('image/')){
        const img = document.createElement('img');
        img.src = url;
        img.width = 100;
        img.height = 100;
        img.style.objectFit = 'cover';
        preview.appendChild(img);
    }
    else if (file.type.startsWith('video/')){
        const video = document.createElement('video');
        video.src = url;
        video.width = 100;
        video.height = 100;
        video.controls = true;
        preview.appendChild(video);

    }
});
