/**
 * PRIME OPTICAL VISION - Advanced Virtual Try-On Module
 * Engineering Principle: Real-time Geometric Alignment
 * 
 * Logic Separation:
 * 1. FaceTracker: Wraps MediaPipe, handles smoothing, emits 'onFaceProto'.
 * 2. VisualEngine: Wraps Three.js, manages occlusion, lighting, and frame rendering.
 * 3. GeometrySolver: Pure math for PnP, scaling, and alignment.
 * 4. TryOnApp: Orchestrates camera, state, and UI binding.
 */

// import * as THREE from 'three'; // REMOVED: Using Global
// import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'; // REMOVED: Using Global

// Access Globals
const THREE = window.THREE;

// --- CONSTANTS ---
const IPD_REFERENCE_MM = 63.0; // Standard Inter-pupillary distance
const FRAME_REFERENCE_WIDTH_MM = 140.0; // Standard frame width
const SMOOTHING_FACTOR = 0.5; // EMA Alpha (0.1 = very smooth/slow, 0.9 = responsive/jittery)

// --- UTILITIES: GEOMETRY SOLVER ---
class GeometrySolver {
    static getCentroid(points) {
        const center = new THREE.Vector3();
        points.forEach(p => center.add(p));
        center.divideScalar(points.length);
        return center;
    }

    /**
     * Constructs a rotation matrix from Facial Normal logic.
     * We define:
     * - Forward (Z): Face Normal (approx)
     * - Up (Y): Vector from Mouth to Mid-Eyes
     * - Right (X): Cross product
     */
    static computeHeadPose(landmarks, videoAspect) {
        // Landmarks: 33 (L Eye), 263 (R Eye), 1 (Nose Tip), 152 (Chin), 61 (Mouth L), 291 (Mouth R)
        // MediaPipe coords are normalized [0,1]. We convert to aspect-corrected space.

        const toVector = (idx) => new THREE.Vector3(
            (landmarks[idx].x - 0.5),
            -(landmarks[idx].y - 0.5), // Flip Y for 3D space
            -landmarks[idx].z // MP Z is rough
        );

        const leftEye = toVector(33);
        const rightEye = toVector(263);
        const nose = toVector(1);
        const chin = toVector(152);

        // Midpoints
        const midEyes = new THREE.Vector3().addVectors(leftEye, rightEye).multiplyScalar(0.5);

        // Construct Basis Vectors
        // UP: Chin -> Mid-Eyes
        const up = new THREE.Vector3().subVectors(midEyes, chin).normalize();

        // RIGHT: LeftEye -> RightEye (Strictly horizontal relative to head)
        const right = new THREE.Vector3().subVectors(rightEye, leftEye).normalize();

        // FORWARD: Cross(Right, Up) - pointing out of face
        const forward = new THREE.Vector3().crossVectors(right, up).normalize();

        // Re-orthogonalize Up to ensure 90 degrees
        const correctedUp = new THREE.Vector3().crossVectors(forward, right).normalize();

        const rotationMatrix = new THREE.Matrix4().makeBasis(right, correctedUp, forward);
        const quaternion = new THREE.Quaternion().setFromRotationMatrix(rotationMatrix);

        return {
            quaternion: quaternion,
            center: midEyes, // Normalized screen space center
            noseTip: nose,
            eyeDistance: leftEye.distanceTo(rightEye)
        };
    }
}

// --- UTILITIES: SMOOTHING ---
class LandmarkSmoother {
    constructor() {
        this.buffer = null;
    }

    update(newValue, alpha = SMOOTHING_FACTOR) {
        if (!this.buffer) {
            this.buffer = newValue.clone();
            return newValue;
        }
        this.buffer.lerp(newValue, alpha);
        return this.buffer.clone();
    }
}

// --- CORE: VISUAL ENGINE ---
class VisualEngine {
    constructor(canvas, videoElement) {
        this.canvas = canvas;
        this.video = videoElement;
        this.scene = new THREE.Scene();
        this.camera = null;
        this.renderer = null;
        this.currentFrame = null;
        this.occluderMesh = null;

        this.frameGroup = new THREE.Group(); // Holds the glasses
        this.scene.add(this.frameGroup);

        this.poseSmoother = {
            position: new LandmarkSmoother(),
            quaternion: new LandmarkSmoother(),
            scale: new LandmarkSmoother()
        };

        this.initThree();
        this.initLights();
        // this.initOccluder(); // Placeholder for phase 2
    }

    initThree() {
        const width = this.video.videoWidth || 640;
        const height = this.video.videoHeight || 480;
        const aspect = width / height;

        // Use Perspective Camera matching generic webcam FOV (~60 deg)
        // We place camera at (0,0,50) to give working room.
        this.camera = new THREE.PerspectiveCamera(50, aspect, 0.1, 1000);
        this.camera.position.set(0, 0, 50);
        this.camera.lookAt(0, 0, 0);

        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            alpha: true,
            antialias: true,
            preserveDrawingBuffer: true
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(window.devicePixelRatio);
    }

    initLights() {
        // High quality lighting for realistic frame reflection
        const startLight = new THREE.DirectionalLight(0xffffff, 1.2);
        startLight.position.set(10, 10, 20);
        this.scene.add(startLight);

        const fillLight = new THREE.DirectionalLight(0xffeedd, 0.8);
        fillLight.position.set(-10, 0, 20);
        this.scene.add(fillLight);

        const ambient = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambient);
    }

    async loadFrame(url) {
        return new Promise((resolve, reject) => {
            // Robust Global Loader Access
            const LoaderClass = THREE.GLTFLoader || window.GLTFLoader;
            if (!LoaderClass) {
                console.error("GLTFLoader not found!");
                return reject("GLTFLoader missing");
            }
            const loader = new LoaderClass();
            loader.load(url, (gltf) => {
                const model = gltf.scene;

                // Cleanup old
                if (this.currentFrame) this.frameGroup.remove(this.currentFrame);

                // Normalize Model Center
                const box = new THREE.Box3().setFromObject(model);
                const center = box.getCenter(new THREE.Vector3());
                const size = box.getSize(new THREE.Vector3());

                // Shift so (0,0,0) is at the bridge (top center relatively)
                // Bridge logic: X=0, Y=Top - 10-20%, Z=Front
                const bridgeY = center.y + size.y * 0.35;

                const wrapper = new THREE.Object3D();
                model.position.set(-center.x, -bridgeY, -center.z);
                wrapper.add(model);

                this.currentFrame = wrapper;
                this.frameGroup.add(wrapper);
                this.frameGroup.visible = true;
                resolve(wrapper);
            }, undefined, reject);
        });
    }

    update(poseData) {
        if (!this.currentFrame) return;

        // 1. Z-Projection Logic
        // We map the normalized 2D center to the Camera Frustum plane at Z=0
        const vPlaneHalfH = Math.tan(THREE.Math.degToRad(this.camera.fov / 2)) * this.camera.position.z;
        const vPlaneW = vPlaneHalfH * 2 * this.camera.aspect;
        const vPlaneH = vPlaneHalfH * 2;

        // Position on the Z=0 plane
        const targetPos = new THREE.Vector3(
            poseData.center.x * vPlaneW,
            poseData.center.y * vPlaneH,
            0 // Locked to Z=0 for stability, depth handled by scale
        );

        // 2. Scale Logic
        // Calculate physical scale ratio.
        // We want the eyeDistance in model space to match eyeDistance in world space.
        // But we don't know the exact model dimensions without metadata.
        // Robust Heuristic: The model width should be approx 2.2x the IPD.
        const modelScale = (poseData.eyeDistance * vPlaneW * 2.2) * 6.5; // Tuned multiplier

        // 3. Smoothing
        const smoothPos = this.poseSmoother.position.update(targetPos);
        const smoothRot = this.poseSmoother.quaternion.update(poseData.quaternion);
        // Scale smoothing is critical to prevent "breathing" effect
        // We manually smooth the scalar
        if (!this.scaleBuffer) this.scaleBuffer = modelScale;
        this.scaleBuffer = this.scaleBuffer * 0.7 + modelScale * 0.3;

        // 4. Apply Transforms
        this.frameGroup.position.copy(smoothPos);
        this.frameGroup.quaternion.copy(smoothRot);
        this.frameGroup.scale.setScalar(this.scaleBuffer);

        // Render
        this.renderer.render(this.scene, this.camera);
    }

    clear() {
        this.renderer.clear();
        this.frameGroup.visible = false;
    }

    resize(w, h) {
        this.camera.aspect = w / h;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(w, h);
    }
}

// --- CORE: MAIN APPLICATION ---
class TryOnApp {
    constructor() {
        this.video = document.getElementById('webcam');
        this.canvas = document.getElementById('canvas');
        this.captureUi = {
            startBtn: document.getElementById('startBtn'),
            captureBtn: document.getElementById('captureBtn'),
            retakeBtn: document.getElementById('retakeBtn'),
            capturedFace: document.getElementById('captured-face'),
            error: document.getElementById('camera-error')
        };

        this.engine = null;
        this.faceMesh = null;
        this.isCameraRunning = false;
        this.mode = 'LIVE'; // LIVE | CAPTURED
        this.framesMetadata = {};

        this.init();
    }

    async init() {
        console.log("TryOnApp Initializing...");

        // Load metadata
        try {
            const resp = await fetch(window.tryonConfig?.framesUrl || '/virtual-tryon/api/models/');
            const data = await resp.json();
            if (data.success) {
                data.frames.forEach(f => this.framesMetadata[f.id] = f);
            }
        } catch (e) { console.warn("Metadata load failed", e); }

        // Bind UI
        this.captureUi.startBtn.onclick = () => this.startSystem();
        this.captureUi.captureBtn.onclick = () => this.capture();
        this.captureUi.retakeBtn.onclick = () => this.retake();

        // Bind Cards
        document.querySelectorAll('.tryon-card').forEach(c => {
            c.onclick = () => this.handleCardClick(c);
        });

        // Init Engine
        this.engine = new VisualEngine(this.canvas, this.video);

        // Handle Resize
        window.onresize = () => {
            if (this.video) this.engine.resize(this.video.clientWidth, this.video.clientHeight);
        };
    }

    async startSystem() {
        console.log("Requesting camera access...");
        this.captureUi.error.style.display = 'none';

        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert("Camera API not supported in this browser. Please use Chrome/Safari/Firefox/Edge.");
            return;
        }

        try {
            // Simplify constraints to just "true" to maximize compatibility
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            console.log("Stream acquired:", stream);

            this.video.srcObject = stream;

            // Robust play handling
            this.video.onloadedmetadata = async () => {
                console.log("Video metadata loaded");
                try {
                    await this.video.play();
                    console.log("Video playing");
                    // UI Updates
                    this.isCameraRunning = true;
                    this.captureUi.startBtn.disabled = true;
                    this.captureUi.captureBtn.disabled = false;
                    this.captureUi.retakeBtn.style.display = 'none';
                    this.video.style.display = 'block';
                    this.captureUi.capturedFace.style.display = 'none';

                    this.initMediaPipe();
                } catch (playErr) {
                    console.error("Play error:", playErr);
                    alert("Camera started but video failed to play: " + playErr.message);
                }
            };

        } catch (e) {
            console.error("Camera Access Error:", e);
            alert("Camera Access Denied or Error: " + e.name + " - " + e.message + "\nPlease check browser permissions.");
            this.captureUi.error.textContent = "Error: " + e.message;
            this.captureUi.error.style.display = 'block';
        }
    }

    initMediaPipe() {
        if (!window.FaceMesh || !window.Camera) {
            console.error("MediaPipe not loaded");
            return;
        }

        this.faceMesh = new window.FaceMesh({ locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}` });
        this.faceMesh.setOptions({
            maxNumFaces: 1,
            refineLandmarks: true,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        this.faceMesh.onResults((res) => this.onFaceResults(res));

        // Start Loop
        const loop = async () => {
            if (this.isCameraRunning && this.video.readyState >= 2) {
                await this.faceMesh.send({ image: this.video });
            }
            requestAnimationFrame(loop);
        };
        loop();
    }

    onFaceResults(results) {
        if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
            const landmarks = results.multiFaceLandmarks[0];
            const pose = GeometrySolver.computeHeadPose(landmarks);
            this.engine.update(pose);
        } else {
            this.engine.clear();
        }
    }

    async handleCardClick(card) {
        if (this.mode === 'CAPTURED') return; // In gallery mode, these are static

        const variantId = card.dataset.variantId;
        const meta = this.framesMetadata[variantId];
        if (meta?.model_url) {
            card.classList.add('loading');
            await this.engine.loadFrame(meta.model_url);
            card.classList.remove('loading');
        }
    }

    // --- CAPTURE MODE (SMART GALLERY) ---
    async capture() {
        if (!this.isCameraRunning) return;

        // 1. Capture Image
        const capCanvas = document.createElement('canvas');
        capCanvas.width = this.video.videoWidth;
        capCanvas.height = this.video.videoHeight;
        capCanvas.getContext('2d').drawImage(this.video, 0, 0);

        this.captureUi.capturedFace.src = capCanvas.toDataURL('image/jpeg');
        this.captureUi.capturedFace.style.display = 'block';
        this.video.style.display = 'none';

        // 2. Stop Camera Flow
        this.isCameraRunning = false;
        this.video.pause();
        this.mode = 'CAPTURED';

        // 3. UI Update
        this.captureUi.captureBtn.style.display = 'none';
        this.captureUi.retakeBtn.style.display = 'inline-block';
        this.captureUi.retakeBtn.disabled = false;

        // 4. Trigger Batch Processing
        await this.runSmartGallery(capCanvas);
    }

    async retake() {
        this.mode = 'LIVE';
        this.isCameraRunning = true;
        this.video.play();
        this.video.style.display = 'block';
        this.captureUi.capturedFace.style.display = 'none';

        this.captureUi.captureBtn.style.display = 'inline-block';
        this.captureUi.retakeBtn.style.display = 'none';

        this.engine.clear();
    }

    async runSmartGallery(sourceCanvas) {
        // Re-use the existing visual engine but offscreen?
        // Actually, we need to run face detection ONE LAST TIME on the static image
        // to get the perfect static landmarks.

        this.faceMesh.reset(); // clear history

        // We need a way to get landmarks ONE time.
        // We'll hook the next result.
        const originalOnResults = this.faceMesh.onResults;

        return new Promise((resolve) => {
            // One-time listener for the static image
            const processStaticImage = async (results) => {
                if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
                    const landmarks = results.multiFaceLandmarks[0];
                    const pose = GeometrySolver.computeHeadPose(landmarks);

                    // Now render every card
                    const cards = document.querySelectorAll('.tryon-card');
                    let count = 0;
                    for (const card of cards) {
                        try {
                            await this.renderCard(card, pose, sourceCanvas);
                            count++;
                            // Small delay to yield to UI/main thread to prevent freezing
                            if (count % 2 === 0) await new Promise(r => setTimeout(r, 50));
                        } catch (err) {
                            console.error("Failed to render card", card, err);
                            card.classList.remove('loading');
                        }
                    }
                } else {
                    console.warn("No face detected in capture!");
                    alert("No face detected. Please retake.");
                }

                // Restore original listener
                this.faceMesh.onResults((res) => this.onFaceResults(res));
                resolve();
            };

            this.faceMesh.onResults(processStaticImage);
            this.faceMesh.send({ image: sourceCanvas });
        });
    }

    async renderCard(card, pose, bgCanvas) {
        const variantId = card.dataset.variantId;
        const meta = this.framesMetadata[variantId];
        if (!meta?.model_url) return;

        card.classList.add('loading');

        // Load model into engine
        await this.engine.loadFrame(meta.model_url);

        // Force update engine to this static pose
        this.engine.update(pose);

        // Composite
        const destW = 500;
        const destH = destW * (bgCanvas.height / bgCanvas.width);

        const comp = document.createElement('canvas');
        comp.width = destW;
        comp.height = destH;
        const ctx = comp.getContext('2d');

        // Draw Face (Mirrored to match webcam feel?)
        // The sourceCanvas is raw video. 
        // engine render is also matching that geometry.
        // We flip both for the user.
        ctx.save();
        ctx.scale(-1, 1);
        ctx.translate(-destW, 0);
        ctx.drawImage(bgCanvas, 0, 0, destW, destH);

        // Draw 3D
        ctx.drawImage(this.engine.renderer.domElement, 0, 0, destW, destH);
        ctx.restore();

        // Apply
        const img = card.querySelector('.tryon-view');
        img.src = comp.toDataURL('image/jpeg', 0.85);
        img.onload = () => {
            img.style.display = 'block';
            card.querySelector('.default-view').style.display = 'none';
            card.classList.remove('loading');
        };
    }
}

// --- BOOTSTRAP ---
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TryOnApp();
});
