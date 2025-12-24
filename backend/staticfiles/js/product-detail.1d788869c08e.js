// Product Detail Page JavaScript

// Variant Selection Logic
function selectVariant(id, name, imageUrl, element) {
    // Update Form Action
    const form = document.getElementById('addToCartForm');
    if (!form) return;

    // Replace the ID in the URL
    const currentAction = form.action;
    form.action = currentAction.replace(/\/cart\/add\/\d+\/?/, '/cart/add/' + id + '/');

    // Update UI Text
    const selectedColorName = document.getElementById('selectedColorName');
    if (selectedColorName) {
        selectedColorName.innerText = name;
    }

    // Update Main Image
    if (imageUrl) {
        updateMainImage(imageUrl);
    }

    // Update Visual Selection State
    document.querySelectorAll('.variant-option').forEach(el => {
        el.classList.remove('variant-selected');
    });
    element.classList.add('variant-selected');
}

// Image Switcher
function updateMainImage(url) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage && url) {
        mainImage.src = url;
    }
}

// Virtual Try-On Modal Logic
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById("tryOnModal");
    const btn = document.getElementById("tryOnBtn");
    const span = document.getElementById("closeModal");
    const video = document.getElementById("webcam");

    if (btn && modal) {
        btn.onclick = function () {
            modal.style.display = "block";
            startWebcam();
        }
    }

    if (span && modal) {
        span.onclick = function () {
            modal.style.display = "none";
            stopWebcam();
        }
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
            stopWebcam();
        }
    }

    function startWebcam() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia && video) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                    video.srcObject = stream;
                })
                .catch(function (err) {
                    console.log("Webcam error:", err);
                    alert("Could not access webcam. Please allow camera permissions.");
                });
        }
    }

    function stopWebcam() {
        if (video && video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
            video.srcObject = null;
        }
    }
});
