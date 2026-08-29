function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (const cookie of cookies) {
            const trimmedCookie = cookie.trim();

            if (trimmedCookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(
                    trimmedCookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}


document.addEventListener('DOMContentLoaded', function () {

    const uploadInput = document.querySelector('#product-media-upload');
    const previewContainer = document.querySelector('#product-media-preview');
    const uploadButton = document.querySelector('#upload-product-media');


    // ==============================
    // Group Preview
    // ==============================

    if (uploadInput && previewContainer) {

        uploadInput.addEventListener('change', function () {

            previewContainer.innerHTML = '';

            const files = uploadInput.files;

            for (const file of files) {

                const item = document.createElement('div');

                item.style.width = '120px';
                item.style.textAlign = 'center';

                const url = URL.createObjectURL(file);


                if (file.type.startsWith('image/')) {

                    const img = document.createElement('img');

                    img.src = url;
                    img.width = 100;
                    img.height = 100;
                    img.style.objectFit = 'cover';

                    item.appendChild(img);

                } else if (file.type.startsWith('video/')) {

                    const video = document.createElement('video');

                    video.src = url;
                    video.width = 100;
                    video.height = 100;
                    video.controls = true;

                    item.appendChild(video);
                }


                const name = document.createElement('div');

                name.textContent = file.name;
                name.style.marginTop = '5px';

                item.appendChild(name);

                previewContainer.appendChild(item);
            }
        });
    }


    // ==============================
    // Group Upload
    // ==============================

    if (uploadButton && uploadInput) {

        uploadButton.addEventListener('click', function () {

            const files = uploadInput.files;

            if (!files.length) {
                alert('لطفاً حداقل یک فایل انتخاب کنید.');
                return;
            }


            const pathParts = window.location.pathname.split('/');

            const productIndex = pathParts.indexOf('product');

            if (productIndex === -1 || !pathParts[productIndex + 1]) {
                alert('شناسه محصول از URL پیدا نشد.');
                return;
            }

            const productId = pathParts[productIndex + 1];

            const formData = new FormData();


            for (const file of files) {
                formData.append('files', file);
            }


            fetch(`/product/${productId}/upload_media/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(function (response) {

                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }

                return response.json();
            })
            .then(function (data) {

                if (data.success) {

                    alert(
                        `${data.count} فایل با موفقیت آپلود شد.`
                    );

                    location.reload();

                } else {

                    alert(
                        data.message || 'خطا در آپلود فایل‌ها.'
                    );
                }
            })
            .catch(function (error) {

                console.error(error);

                alert('خطایی هنگام آپلود رخ داد.');
            });
        });
    }


    // ==============================
    // Inline Preview
    // ==============================

    document.addEventListener('change', function (event) {

        if (!event.target.matches('input[type="file"]')) {
            return;
        }


        const input = event.target;

        if (input === uploadInput) {
            return;
        }


        const file = input.files[0];

        if (!file) {
            return;
        }


        const row = input.closest('tr');

        if (!row) {
            return;
        }


        const preview = row.querySelector('.field-media_preview');

        if (!preview) {
            return;
        }


        const oldMedia = preview.querySelector('img, video');

        if (oldMedia) {
            oldMedia.remove();
        }


        const url = URL.createObjectURL(file);


        if (file.type.startsWith('image/')) {

            const img = document.createElement('img');

            img.src = url;
            img.width = 100;
            img.height = 100;
            img.style.objectFit = 'cover';

            preview.appendChild(img);

        } else if (file.type.startsWith('video/')) {

            const video = document.createElement('video');

            video.src = url;
            video.width = 100;
            video.height = 100;
            video.controls = true;

            preview.appendChild(video);
        }
    });

});