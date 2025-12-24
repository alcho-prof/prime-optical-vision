/**
 * Virtual Try-On AR Feature
 * Uses TensorFlow.js and Face Landmarks Detection for real-time frame overlay
 */

// Global variables
let video, canvas, ctx;
let detector;
let currentStream;
let selectedVariant = null;
let frameImage = null;
let isDetecting = false;
let facingMode = 'user'; // 'user' or 'environment'

/**
 * Initialize the Virtual Try-On application
 * @param {string} sessionId - Unique session identifier
 */
function initVirtualTryOn(sessionId) {
    window.sessionId = sessionId;

    // Initialize on page load
    document.addEventListener('DOMContentLoaded', async () => {
        video = document.getElementById('webcam');
        canvas = document.getElementById('canvas');
        ctx = canvas.getContext('2d');

        // Setup event listeners
        document.getElementById('startBtn').addEventListener('click', startCamera);
        document.getElementById('stopBtn').addEventListener('click', stopCamera);
        document.getElementById('captureBtn').addEventListener('click', capturePhoto);
        document.getElementById('switchBtn').addEventListener('click', switchCamera);

        // Variant selection
        document.querySelectorAll('.variant-item').forEach(item => {
            item.addEventListener('click', () => selectVariant(item));
        });

        // Load face detection model
        await loadModel();
    });
}

/**
 * Load TensorFlow.js Face Detection Model
 */
async function loadModel() {
    try {
        const model = faceLandmarksDetection.SupportedModels.MediaPipeFaceMesh;
        const detectorConfig = {
            runtime: 'tfjs',
            refineLandmarks: true,
        };
        detector = await faceLandmarksDetection.createDetector(model, detectorConfig);
        document.getElementById('loading').style.display = 'none';
        console.log('Face detection model loaded successfully');
    } catch (error) {
        console.error('Error loading model:', error);
        document.getElementById('loading').innerHTML = '<div>Error loading AR models. Please refresh the page.</div>';
    }
}

/**
 * Start camera and begin AR session
 */
async function startCamera() {
    try {
        const constraints = {
            video: {
                facingMode: facingMode,
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        };

        currentStream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = currentStream;

        video.addEventListener('loadeddata', () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            // Update button states
            updateButtonStates(true);

            // Start detection loop
            isDetecting = true;
            detectFaces();
        });
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Unable to access camera. Please check permissions and ensure you are using HTTPS.');
    }
}

/**
 * Stop camera and end AR session
 */
function stopCamera() {
    isDetecting = false;
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
    }

    // Update button states
    updateButtonStates(false);

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

/**
 * Switch between front and rear cameras (mobile)
 */
async function switchCamera() {
    facingMode = facingMode === 'user' ? 'environment' : 'user';
    stopCamera();
    await startCamera();
}

/**
 * Update button states based on camera status
 * @param {boolean} cameraActive - Whether camera is currently active
 */
function updateButtonStates(cameraActive) {
    document.getElementById('startBtn').disabled = cameraActive;
    document.getElementById('stopBtn').disabled = !cameraActive;
    document.getElementById('captureBtn').disabled = !cameraActive;
    document.getElementById('switchBtn').disabled = !cameraActive;

    if (cameraActive) {
        document.getElementById('startBtn').classList.remove('active');
        document.getElementById('stopBtn').classList.add('active');
    } else {
        document.getElementById('startBtn').classList.add('active');
        document.getElementById('stopBtn').classList.remove('active');
    }
}

/**
 * Main face detection loop
 */
async function detectFaces() {
    if (!isDetecting || !detector) return;

    try {
        const faces = await detector.estimateFaces(video, {
            flipHorizontal: false
        });

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (faces.length > 0) {
            const face = faces[0];

            // Draw frame overlay if selected
            if (selectedVariant && frameImage) {
                drawFrameOverlay(face);
            }
        }
    } catch (error) {
        console.error('Detection error:', error);
    }

    // Continue detection loop
    requestAnimationFrame(detectFaces);
}

/**
 * Draw eyeglass frame overlay on detected face
 * @param {Object} face - Detected face object with keypoints
 */
function drawFrameOverlay(face) {
    // Get key facial landmarks
    const keypoints = face.keypoints;

    // Find eye positions (approximate)
    const leftEye = keypoints[33]; // Left eye outer corner
    const rightEye = keypoints[263]; // Right eye outer corner

    if (!leftEye || !rightEye) return;

    // Calculate frame position and size
    const eyeDistance = Math.sqrt(
        Math.pow(rightEye.x - leftEye.x, 2) +
        Math.pow(rightEye.y - leftEye.y, 2)
    );

    const frameWidth = eyeDistance * 2.2; // Adjust multiplier for frame size
    const frameHeight = frameWidth * 0.4; // Aspect ratio for glasses

    // Center position between eyes
    const centerX = (leftEye.x + rightEye.x) / 2;
    const centerY = (leftEye.y + rightEye.y) / 2;

    // Calculate rotation angle
    const angle = Math.atan2(rightEye.y - leftEye.y, rightEye.x - leftEye.x);

    // Draw the frame
    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(angle);
    ctx.globalAlpha = 0.9;
    ctx.drawImage(
        frameImage,
        -frameWidth / 2,
        -frameHeight / 2,
        frameWidth,
        frameHeight
    );
    ctx.restore();
}

/**
 * Select a variant to try on
 * @param {HTMLElement} item - Clicked variant item element
 */
function selectVariant(item) {
    // Remove active class from all items
    document.querySelectorAll('.variant-item').forEach(el => {
        el.classList.remove('active');
    });

    // Add active class to selected item
    item.classList.add('active');

    // Load frame image
    const variantId = item.dataset.variantId;
    const imageUrl = item.dataset.imageUrl;

    selectedVariant = variantId;

    // Load image
    frameImage = new Image();
    frameImage.crossOrigin = 'anonymous';
    frameImage.src = imageUrl;
    frameImage.onload = () => {
        console.log('Frame image loaded successfully');
    };
    frameImage.onerror = () => {
        console.error('Error loading frame image');
        alert('Error loading frame image. Please try another frame.');
    };
}

/**
 * Capture photo with AR overlay
 */
async function capturePhoto() {
    if (!selectedVariant) {
        alert('Please select a frame first');
        return;
    }

    // Create a temporary canvas for capture
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');

    // Draw video frame
    tempCtx.save();
    tempCtx.scale(-1, 1); // Mirror
    tempCtx.drawImage(video, -tempCanvas.width, 0, tempCanvas.width, tempCanvas.height);
    tempCtx.restore();

    // Draw overlay
    tempCtx.drawImage(canvas, 0, 0);

    // Convert to base64
    const photoData = tempCanvas.toDataURL('image/jpeg', 0.9);

    // Save to server
    try {
        const response = await fetch('/virtual-tryon/api/save-photo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: window.sessionId,
                variant_id: selectedVariant,
                photo: photoData
            })
        });

        const result = await response.json();
        if (result.success) {
            alert('Photo saved successfully!');
        } else {
            alert('Error saving photo: ' + result.error);
        }
    } catch (error) {
        console.error('Error saving photo:', error);
        alert('Error saving photo. Please try again.');
    }
}
