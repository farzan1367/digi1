// =========================================================
// CSRF Cookie
// =========================================================

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


// =========================================================
// Product ID
// =========================================================

function getProductId() {

    const pathParts = window.location.pathname
        .split('/')
        .filter(Boolean);

    const productIndex = pathParts.indexOf('product');

    if (
        productIndex === -1 ||
        !pathParts[productIndex + 1]
    ) {
        return null;
    }

    return pathParts[productIndex + 1];
}


// =========================================================
// DOM Loaded
// =========================================================

document.addEventListener('DOMContentLoaded', function () {

    const uploadInput = document.querySelector(
        '#product-media-upload'
    );

    const previewContainer = document.querySelector(
        '#product-media-preview'
    );

    const uploadButton = document.querySelector(
        '#upload-product-media'
    );


    // =====================================================
    // Group Preview
    // =====================================================

    if (uploadInput && previewContainer) {

        uploadInput.addEventListener(
            'change',
            function () {

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

                    }

                    else if (file.type.startsWith('video/')) {

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
            }
        );
    }


    // =====================================================
    // Group Upload
    // =====================================================

    if (uploadButton && uploadInput) {

        uploadButton.addEventListener(
            'click',
            function () {

                const files = uploadInput.files;

                if (!files.length) {

                    alert(
                        'لطفاً حداقل یک فایل انتخاب کنید.'
                    );

                    return;
                }


                const productId = getProductId();

                if (!productId) {

                    alert(
                        'شناسه محصول از URL پیدا نشد.'
                    );

                    return;
                }


                const formData = new FormData();


                for (const file of files) {

                    formData.append(
                        'files',
                        file
                    );
                }


                fetch(
                    `/product/${productId}/upload_media/`,
                    {
                        method: 'POST',

                        body: formData,

                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    }
                )

                .then(function (response) {

                    if (!response.ok) {

                        throw new Error(
                            `HTTP error: ${response.status}`
                        );
                    }

                    return response.json();
                })

                .then(function (data) {

                    if (data.success) {

                        alert(
                            `${data.count} فایل با موفقیت آپلود شد.`
                        );

                        location.reload();

                    }

                    else {

                        alert(
                            data.message ||
                            'خطا در آپلود فایل‌ها.'
                        );
                    }
                })

                .catch(function (error) {

                    console.error(error);

                    alert(
                        'خطایی هنگام آپلود رخ داد.'
                    );
                });
            }
        );
    }


    // =====================================================
    // Inline Preview
    // =====================================================

    document.addEventListener(
        'change',
        function (event) {

            if (
                !event.target.matches(
                    'input[type="file"]'
                )
            ) {
                return;
            }


            const input = event.target;


            // ورودی آپلود گروهی را نادیده بگیر
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


            const preview = row.querySelector(
                '.field-media_preview'
            );

            if (!preview) {
                return;
            }


            const oldMedia = preview.querySelector(
                'img, video'
            );

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
            }

            else if (file.type.startsWith('video/')) {

                const video = document.createElement('video');

                video.src = url;
                video.width = 100;
                video.height = 100;
                video.controls = true;

                preview.appendChild(video);
            }
        }
    );


    // =====================================================
    // Get Existing Media Rows
    // =====================================================

    function getMediaRows() {

        const rows = document.querySelectorAll(
            '.inline-group tbody tr.form-row'
        );

        return Array.from(rows).filter(function (row) {

            const idInput = row.querySelector(
                'input[name$="-id"]'
            );

            return idInput && idInput.value;
        });
    }


    // =====================================================
    // Get Media ID
    // =====================================================

    function getMediaId(row) {

        const idInput = row.querySelector(
            'input[name$="-id"]'
        );

        if (!idInput) {
            return null;
        }

        return idInput.value;
    }


    // =====================================================
    // Save New Order
    // =====================================================

    function saveMediaOrder() {

        const productId = getProductId();

        if (!productId) {
            return;
        }


        const rows = getMediaRows();

        const order = rows
            .map(getMediaId)
            .filter(Boolean);


        fetch(
            `/product/${productId}/reorder_media/`,
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },

                body: JSON.stringify({
                    order: order
                })
            }
        )

        .then(function (response) {

            if (!response.ok) {

                throw new Error(
                    `HTTP error: ${response.status}`
                );
            }

            return response.json();
        })

        .then(function (data) {

            if (!data.success) {

                throw new Error(
                    data.message ||
                    'خطا در ذخیره ترتیب'
                );
            }
        })

        .catch(function (error) {

            console.error(
                'Reorder error:',
                error
            );

            alert(
                'ترتیب جدید ذخیره نشد.'
            );
        });
    }


    // =====================================================
    // Delete Media
    // =====================================================

    function deleteMedia(row, mediaId) {

    const deleteInput = row.querySelector(
        'input[name$="-DELETE"]'
    );

    if (!deleteInput) {
        console.error(
            'Django DELETE input not found.'
        );
        return;
    }

    const confirmed = confirm(
        'آیا مطمئن هستید که می‌خواهید این مدیا حذف شود؟'
    );

    if (!confirmed) {
        return;
    }

    // به Django Admin می‌گوییم این Inline باید حذف شود
    deleteInput.checked = true;

    // ردیف را فقط از ظاهر صفحه مخفی می‌کنیم
    row.style.display = 'none';
}


    // =====================================================
    // Drag & Drop
    // =====================================================

    function enableDragAndDrop() {

        const rows = getMediaRows();

        rows.forEach(function (row) {

            row.draggable = true;

            row.style.cursor = 'move';


            row.addEventListener(
                'dragstart',
                function (event) {

                    row.classList.add(
                        'media-dragging'
                    );

                    event.dataTransfer.effectAllowed =
                        'move';

                    event.dataTransfer.setData(
                        'text/plain',
                        ''
                    );
                }
            );


            row.addEventListener(
                'dragend',
                function () {

                    row.classList.remove(
                        'media-dragging'
                    );
                }
            );


            row.addEventListener(
                'dragover',
                function (event) {

                    event.preventDefault();

                    const draggingRow =
                        document.querySelector(
                            '.media-dragging'
                        );

                    if (
                        !draggingRow ||
                        draggingRow === row
                    ) {
                        return;
                    }


                    const tbody = row.parentNode;

                    const rect =
                        row.getBoundingClientRect();

                    const middle =
                        rect.top +
                        rect.height / 2;


                    if (event.clientY < middle) {

                        tbody.insertBefore(
                            draggingRow,
                            row
                        );

                    }

                    else {

                        tbody.insertBefore(
                            draggingRow,
                            row.nextSibling
                        );
                    }
                }
            );


            row.addEventListener(
                'drop',
                function (event) {

                    event.preventDefault();

                    saveMediaOrder();
                }
            );
        });
    }


    // =====================================================
    // Delete Buttons
    // =====================================================

    function enableDeleteButtons() {

        const buttons = document.querySelectorAll(
            '.media-delete-button'
        );


        buttons.forEach(function (button) {

            button.addEventListener(
                'click',
                function (event) {

                    event.preventDefault();
                    event.stopPropagation();


                    const mediaId =
                        button.dataset.mediaId;

                    const row =
                        button.closest('tr');

                    if (!row || !mediaId) {
                        return;
                    }


                    deleteMedia(
                        row,
                        mediaId
                    );
                }
            );
        });
    }


    // =====================================================
    // Initialize
    // =====================================================

    enableDragAndDrop();
    enableDeleteButtons();

});