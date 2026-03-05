import * as THREE from "three";

/**
 * World 1: Brunelleschi's Dome
 *
 * An octagonal Renaissance dome inspired by the Florence Cathedral.
 * Golden light, ornate ribs, marble floor, floating particles.
 * The feeling: awe, warmth, being sheltered, the promise of
 * government protecting individuals.
 */

interface RenaissanceObjects {
  particles: THREE.Points;
  ribs: THREE.Mesh[];
  figure: THREE.Group;
  pointLights: THREE.PointLight[];
}

function createMarbleFloor(scene: THREE.Scene): THREE.Mesh {
  const floorGeo = new THREE.CircleGeometry(12, 64);
  const floorMat = new THREE.MeshStandardMaterial({
    color: 0xf5e6d3,
    roughness: 0.3,
    metalness: 0.1,
  });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.01;
  floor.receiveShadow = true;
  scene.add(floor);

  // Floor inlay pattern — concentric rings
  for (let i = 1; i <= 4; i++) {
    const ringGeo = new THREE.RingGeometry(i * 2.5 - 0.05, i * 2.5 + 0.05, 64);
    const ringMat = new THREE.MeshStandardMaterial({
      color: 0xc4a265,
      roughness: 0.4,
      metalness: 0.2,
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.005;
    scene.add(ring);
  }

  return floor;
}

function createOctagonalDome(scene: THREE.Scene): THREE.Group {
  const domeGroup = new THREE.Group();

  // Main dome shell — upper hemisphere with octagonal flavor
  const domeGeo = new THREE.SphereGeometry(14, 8, 32, 0, Math.PI * 2, 0, Math.PI / 2);
  const domeMat = new THREE.MeshStandardMaterial({
    color: 0xd4a574,
    roughness: 0.6,
    metalness: 0.1,
    side: THREE.BackSide,
  });
  const dome = new THREE.Mesh(domeGeo, domeMat);
  dome.position.y = 0;
  domeGroup.add(dome);

  // Inner dome surface — slightly smaller, warmer color
  const innerGeo = new THREE.SphereGeometry(13.8, 8, 32, 0, Math.PI * 2, 0, Math.PI / 2);
  const innerMat = new THREE.MeshStandardMaterial({
    color: 0xe8cfa0,
    roughness: 0.7,
    metalness: 0.05,
    side: THREE.BackSide,
  });
  const innerDome = new THREE.Mesh(innerGeo, innerMat);
  innerDome.position.y = 0;
  domeGroup.add(innerDome);

  // Drum / base wall (cylindrical lower portion)
  const drumGeo = new THREE.CylinderGeometry(14, 14, 4, 8, 1, true);
  const drumMat = new THREE.MeshStandardMaterial({
    color: 0xd4a574,
    roughness: 0.6,
    metalness: 0.1,
    side: THREE.BackSide,
  });
  const drum = new THREE.Mesh(drumGeo, drumMat);
  drum.position.y = -2;
  domeGroup.add(drum);

  // Oculus at the top — a glowing ring
  const oculusGeo = new THREE.RingGeometry(0.8, 1.2, 32);
  const oculusMat = new THREE.MeshStandardMaterial({
    color: 0xffd700,
    emissive: 0xffd700,
    emissiveIntensity: 0.6,
    roughness: 0.2,
    metalness: 0.8,
    side: THREE.DoubleSide,
  });
  const oculus = new THREE.Mesh(oculusGeo, oculusMat);
  oculus.rotation.x = -Math.PI / 2;
  oculus.position.y = 13.95;
  domeGroup.add(oculus);

  scene.add(domeGroup);
  return domeGroup;
}

function createRibs(scene: THREE.Scene): THREE.Mesh[] {
  const ribs: THREE.Mesh[] = [];
  const ribCount = 8;

  for (let i = 0; i < ribCount; i++) {
    const angle = (i / ribCount) * Math.PI * 2;
    const ribGroup = new THREE.Group();

    // Each rib is composed of segments following the dome curve
    const segmentCount = 20;
    for (let s = 0; s < segmentCount; s++) {
      const t = s / segmentCount;
      const phi = t * (Math.PI / 2);
      const radius = 13.9;

      const x = Math.cos(angle) * radius * Math.cos(phi);
      const z = Math.sin(angle) * radius * Math.cos(phi);
      const y = radius * Math.sin(phi);

      const segGeo = new THREE.BoxGeometry(0.3, 0.8, 0.3);
      const segMat = new THREE.MeshStandardMaterial({
        color: 0xc4a265,
        roughness: 0.4,
        metalness: 0.3,
      });
      const seg = new THREE.Mesh(segGeo, segMat);
      seg.position.set(x, y, z);
      seg.lookAt(0, y + 0.1, 0);
      ribGroup.add(seg);
    }

    scene.add(ribGroup);
    // Store first child for animation reference
    const firstSeg = ribGroup.children[0] as THREE.Mesh;
    ribs.push(firstSeg);
  }

  return ribs;
}

function createHumanFigure(scene: THREE.Scene): THREE.Group {
  const figure = new THREE.Group();

  // Body — cylinder
  const bodyGeo = new THREE.CylinderGeometry(0.25, 0.3, 1.4, 8);
  const bodyMat = new THREE.MeshStandardMaterial({
    color: 0x2a1a0a,
    roughness: 0.9,
    metalness: 0.0,
  });
  const body = new THREE.Mesh(bodyGeo, bodyMat);
  body.position.y = 0.9;
  figure.add(body);

  // Head — sphere
  const headGeo = new THREE.SphereGeometry(0.2, 16, 16);
  const headMat = new THREE.MeshStandardMaterial({
    color: 0x2a1a0a,
    roughness: 0.9,
    metalness: 0.0,
  });
  const head = new THREE.Mesh(headGeo, headMat);
  head.position.y = 1.8;
  figure.add(head);

  // Looking up pose — slight tilt
  figure.position.set(0, 0, 0);
  scene.add(figure);
  return figure;
}

function createParticles(scene: THREE.Scene): THREE.Points {
  const count = 500;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const sizes = new Float32Array(count);

  const goldColor = new THREE.Color(0xffd700);
  const warmColor = new THREE.Color(0xc4a265);

  for (let i = 0; i < count; i++) {
    // Distribute within the dome volume
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI * 0.45;
    const r = 3 + Math.random() * 10;

    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.cos(phi) + 1;
    positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);

    const color = Math.random() > 0.5 ? goldColor : warmColor;
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;

    sizes[i] = 0.02 + Math.random() * 0.06;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  geo.setAttribute("size", new THREE.BufferAttribute(sizes, 1));

  const mat = new THREE.PointsMaterial({
    size: 0.08,
    vertexColors: true,
    transparent: true,
    opacity: 0.7,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });

  const points = new THREE.Points(geo, mat);
  scene.add(points);
  return points;
}

function createLighting(scene: THREE.Scene): THREE.PointLight[] {
  // Golden ambient
  const ambient = new THREE.AmbientLight(0xffd700, 0.3);
  scene.add(ambient);

  // Warm hemisphere light
  const hemi = new THREE.HemisphereLight(0xffd700, 0xc4a265, 0.4);
  scene.add(hemi);

  // Oculus light from above — the divine light
  const oculusLight = new THREE.PointLight(0xfff5e0, 2, 30);
  oculusLight.position.set(0, 13, 0);
  scene.add(oculusLight);

  // Ring of warm point lights around the drum
  const pointLights: THREE.PointLight[] = [];
  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2;
    const light = new THREE.PointLight(0xffa500, 0.6, 15);
    light.position.set(Math.cos(angle) * 12, 2, Math.sin(angle) * 12);
    scene.add(light);
    pointLights.push(light);
  }

  return pointLights;
}

export function createRenaissanceDome(
  scene: THREE.Scene
): { animate: (time: number) => void } {
  // Set scene fog for atmosphere
  scene.fog = new THREE.FogExp2(0x1a0f00, 0.012);
  scene.background = new THREE.Color(0x0a0500);

  createMarbleFloor(scene);
  createOctagonalDome(scene);
  const ribs = createRibs(scene);
  const figure = createHumanFigure(scene);
  const particles = createParticles(scene);
  const pointLights = createLighting(scene);

  const objects: RenaissanceObjects = {
    particles,
    ribs,
    figure,
    pointLights,
  };

  return {
    animate: (time: number) => {
      // Rotate particles slowly
      objects.particles.rotation.y = time * 0.02;

      // Gentle vertical drift for particles
      const posAttr = objects.particles.geometry.getAttribute("position");
      const positions = posAttr.array as Float32Array;
      for (let i = 0; i < positions.length; i += 3) {
        positions[i + 1] += Math.sin(time * 0.5 + i) * 0.001;
      }
      posAttr.needsUpdate = true;

      // Flicker the warm lights gently
      objects.pointLights.forEach((light, idx) => {
        light.intensity = 0.5 + Math.sin(time * 0.8 + idx * 0.7) * 0.15;
      });

      // Subtle figure breathing
      const scale = 1 + Math.sin(time * 0.6) * 0.01;
      objects.figure.scale.set(scale, scale, scale);
    },
  };
}
