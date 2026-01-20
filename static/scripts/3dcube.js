// Three.js 3D Rotating GLB Model with Drop Shadow and Backlight

// Import GLTFLoader from CDN
import('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/jsm/loaders/GLTFLoader.js')
  .then(module => {
    const GLTFLoader = module.GLTFLoader;
    initScene(GLTFLoader);
  })
  .catch(err => {
    console.error('Failed to load GLTFLoader:', err);
  });

function initScene(GLTFLoader) {
// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);

// Camera setup
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.z = 5;

// Renderer setup
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// Variable to hold the loaded model
let loadedModel = null;

// Add a temporary cube to verify rendering works
const tempGeometry = new THREE.BoxGeometry(1, 1, 1);
const tempMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const tempCube = new THREE.Mesh(tempGeometry, tempMaterial);
tempCube.castShadow = true;
scene.add(tempCube);
console.log('Temporary red cube added - if you see this, rendering works!');

// Load GLB model
const loader = new GLTFLoader();
const modelPath = 'static/models/orb.glb'; // Replace with your GLB file path

console.log('Starting to load model from:', modelPath);

loader.load(
  modelPath,
  (gltf) => {
    console.log('Model loaded! Contents:', gltf);
    loadedModel = gltf.scene;

    // Remove temporary cube
    scene.remove(tempCube);

    // Enable shadows for all meshes in the model
    loadedModel.traverse((node) => {
      if (node.isMesh) {
        node.castShadow = true;
        node.receiveShadow = true;
        console.log('Found mesh:', node.name);
      }
    });

    // Center and scale the model
    const box = new THREE.Box3().setFromObject(loadedModel);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());

    console.log('Model size:', size);
    console.log('Model center:', center);

    // Center the model
    loadedModel.position.sub(center);

    // Scale model to fit in view (target size of ~2 units)
    const maxDim = Math.max(size.x, size.y, size.z);
    const scale = 2 / maxDim;
    loadedModel.scale.setScalar(scale);

    console.log('Applied scale:', scale);

    // Position camera based on model size
    const distance = maxDim * 2;
    camera.position.set(distance, distance * 0.5, distance);
    camera.lookAt(0, 0, 0);

    console.log('Camera position:', camera.position);

    // Adjust ground plane position
    plane.position.y = -size.y * scale / 2 - 0.5;

    scene.add(loadedModel);

    console.log('Model loaded successfully!');
  },
  (progress) => {
    console.log('Loading: ' + (progress.loaded / progress.total * 100) + '%');
  },
  (error) => {
    console.error('Error loading model:', error);
  }
);

// Create ground plane for shadow
const planeGeometry = new THREE.PlaneGeometry(10, 10);
const planeMaterial = new THREE.ShadowMaterial({ opacity: 0.3 });
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.position.y = -2;
plane.receiveShadow = true;
scene.add(plane);

// Backlight (behind the cube)
const backLight = new THREE.PointLight(0x00ffff, 2, 100);
backLight.position.set(0, 0, -3);
scene.add(backLight);

// Main light (front/top)
const mainLight = new THREE.DirectionalLight(0xffffff, 1);
mainLight.position.set(5, 5, 5);
mainLight.castShadow = true;
mainLight.shadow.mapSize.width = 2048;
mainLight.shadow.mapSize.height = 2048;
mainLight.shadow.camera.near = 0.5;
mainLight.shadow.camera.far = 50;
scene.add(mainLight);

// Ambient light
const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
scene.add(ambientLight);

// Rim light (side lighting)
const rimLight = new THREE.PointLight(0xff00ff, 1, 100);
rimLight.position.set(-3, 2, 2);
scene.add(rimLight);

// Animation loop
function animate() {
  requestAnimationFrame(animate);

  // Rotate temporary cube
  if (tempCube && tempCube.parent) {
    tempCube.rotation.x += 0.01;
    tempCube.rotation.y += 0.01;
  }

  // Rotate model if loaded
  if (loadedModel) {
    loadedModel.rotation.x += 0.01;
    loadedModel.rotation.y += 0.01;
  }

  // Animate backlight intensity
  backLight.intensity = 2 + Math.sin(Date.now() * 0.001) * 0.5;

  renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Start animation
animate();
} // End of initScene function