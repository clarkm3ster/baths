import * as THREE from "three";

/**
 * World 3: Personal Dome
 *
 * A glass/steel geodesic dome with warm natural light,
 * glowing data panels in domain colors, a coordinator desk,
 * plants, water feature, connected data lines.
 * The feeling: connection, coordination, warmth, technology
 * serving humans, hope.
 */

interface PersonalDomeObjects {
  geodesicFrame: THREE.LineSegments;
  dataPanels: THREE.Mesh[];
  connectionLines: THREE.Line[];
  particles: THREE.Points;
  waterPlane: THREE.Mesh;
  plants: THREE.Group[];
  panelLights: THREE.PointLight[];
}

interface DomainPanel {
  label: string;
  color: number;
  angle: number;
  height: number;
}

const DOMAINS: DomainPanel[] = [
  { label: "Health", color: 0x1a6b3c, angle: 0, height: 2 },
  { label: "Justice", color: 0x8b1a1a, angle: Math.PI / 3, height: 2.5 },
  { label: "Housing", color: 0x1a3d8b, angle: (2 * Math.PI) / 3, height: 1.8 },
  { label: "Income", color: 0x6b5a1a, angle: Math.PI, height: 2.2 },
  { label: "Education", color: 0x5a1a6b, angle: (4 * Math.PI) / 3, height: 2.8 },
  { label: "Child Welfare", color: 0x1a6b6b, angle: (5 * Math.PI) / 3, height: 2.0 },
];

function createPanelTexture(label: string, color: number): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 384;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Could not get 2d context");

  // Translucent dark background
  ctx.fillStyle = "rgba(10, 10, 20, 0.85)";
  ctx.fillRect(0, 0, 256, 384);

  // Colored border
  const hexColor = `#${color.toString(16).padStart(6, "0")}`;
  ctx.strokeStyle = hexColor;
  ctx.lineWidth = 3;
  ctx.strokeRect(4, 4, 248, 376);

  // Header bar
  ctx.fillStyle = hexColor;
  ctx.fillRect(4, 4, 248, 48);

  // Label
  ctx.fillStyle = "#FFFFFF";
  ctx.font = "bold 22px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(label, 128, 34);

  // Simulated data lines
  ctx.strokeStyle = `${hexColor}88`;
  ctx.lineWidth = 1;
  for (let i = 0; i < 8; i++) {
    const y = 70 + i * 36;
    ctx.beginPath();
    ctx.moveTo(20, y);
    // Data chart line
    let cx = 20;
    for (let p = 0; p < 10; p++) {
      cx += 22;
      const cy = y + (Math.random() - 0.5) * 20;
      ctx.lineTo(cx, cy);
    }
    ctx.stroke();
  }

  // Status indicator dot
  ctx.fillStyle = hexColor;
  ctx.beginPath();
  ctx.arc(230, 28, 8, 0, Math.PI * 2);
  ctx.fill();

  // Pulsing ring
  ctx.strokeStyle = `${hexColor}66`;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(230, 28, 12, 0, Math.PI * 2);
  ctx.stroke();

  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  return texture;
}

function createGeodesicDome(scene: THREE.Scene): THREE.LineSegments {
  // Wireframe geodesic dome using icosahedron
  const icoGeo = new THREE.IcosahedronGeometry(10, 2);
  const edgesGeo = new THREE.EdgesGeometry(icoGeo);
  const frameMat = new THREE.LineBasicMaterial({
    color: 0x88aacc,
    transparent: true,
    opacity: 0.6,
  });
  const frame = new THREE.LineSegments(edgesGeo, frameMat);
  scene.add(frame);

  // Transparent glass panels
  const panelMat = new THREE.MeshPhysicalMaterial({
    color: 0xaaccee,
    transparent: true,
    opacity: 0.08,
    roughness: 0.1,
    metalness: 0.2,
    side: THREE.BackSide,
    envMapIntensity: 0.5,
  });
  const panelMesh = new THREE.Mesh(icoGeo.clone(), panelMat);
  scene.add(panelMesh);

  // Steel nodes at vertices
  const posAttr = icoGeo.getAttribute("position");
  const nodePositions = new Set<string>();
  for (let i = 0; i < posAttr.count; i++) {
    const x = posAttr.getX(i);
    const y = posAttr.getY(i);
    const z = posAttr.getZ(i);
    // Only top hemisphere
    if (y < -1) continue;
    const key = `${x.toFixed(2)},${y.toFixed(2)},${z.toFixed(2)}`;
    if (nodePositions.has(key)) continue;
    nodePositions.add(key);

    const nodeGeo = new THREE.SphereGeometry(0.08, 8, 8);
    const nodeMat = new THREE.MeshStandardMaterial({
      color: 0xccddee,
      metalness: 0.7,
      roughness: 0.3,
    });
    const node = new THREE.Mesh(nodeGeo, nodeMat);
    node.position.set(x, y, z);
    scene.add(node);
  }

  icoGeo.dispose();
  return frame;
}

function createDataPanels(scene: THREE.Scene): { panels: THREE.Mesh[]; lights: THREE.PointLight[] } {
  const panels: THREE.Mesh[] = [];
  const lights: THREE.PointLight[] = [];
  const panelRadius = 7;

  for (const domain of DOMAINS) {
    const texture = createPanelTexture(domain.label, domain.color);

    const panelGeo = new THREE.PlaneGeometry(1.8, 2.7);
    const panelMat = new THREE.MeshStandardMaterial({
      map: texture,
      emissive: domain.color,
      emissiveIntensity: 0.15,
      emissiveMap: texture,
      transparent: true,
      opacity: 0.92,
      side: THREE.DoubleSide,
    });

    const panel = new THREE.Mesh(panelGeo, panelMat);
    const x = Math.cos(domain.angle) * panelRadius;
    const z = Math.sin(domain.angle) * panelRadius;
    panel.position.set(x, domain.height, z);
    panel.lookAt(0, domain.height, 0);

    scene.add(panel);
    panels.push(panel);

    // Colored glow light behind each panel
    const light = new THREE.PointLight(domain.color, 0.4, 6);
    light.position.set(
      Math.cos(domain.angle) * (panelRadius + 0.5),
      domain.height,
      Math.sin(domain.angle) * (panelRadius + 0.5)
    );
    scene.add(light);
    lights.push(light);
  }

  return { panels, lights };
}

function createConnectionLines(
  scene: THREE.Scene,
  panels: THREE.Mesh[]
): THREE.Line[] {
  const lines: THREE.Line[] = [];

  // Connect each panel to its neighbors and to center
  for (let i = 0; i < panels.length; i++) {
    const next = (i + 1) % panels.length;
    const points = [
      panels[i].position.clone(),
      new THREE.Vector3(0, 1.5, 0), // through center hub
      panels[next].position.clone(),
    ];

    const curve = new THREE.QuadraticBezierCurve3(points[0], points[1], points[2]);
    const curvePoints = curve.getPoints(30);
    const lineGeo = new THREE.BufferGeometry().setFromPoints(curvePoints);
    const lineMat = new THREE.LineBasicMaterial({
      color: 0xc4a265,
      transparent: true,
      opacity: 0.3,
    });
    const line = new THREE.Line(lineGeo, lineMat);
    scene.add(line);
    lines.push(line);
  }

  // Central hub node
  const hubGeo = new THREE.OctahedronGeometry(0.3, 0);
  const hubMat = new THREE.MeshStandardMaterial({
    color: 0xc4a265,
    emissive: 0xc4a265,
    emissiveIntensity: 0.4,
    metalness: 0.6,
    roughness: 0.2,
  });
  const hub = new THREE.Mesh(hubGeo, hubMat);
  hub.position.set(0, 1.5, 0);
  scene.add(hub);

  return lines;
}

function createCoordinatorDesk(scene: THREE.Scene): void {
  const desk = new THREE.Group();

  // Desktop surface
  const topGeo = new THREE.BoxGeometry(1.8, 0.06, 0.9);
  const topMat = new THREE.MeshStandardMaterial({
    color: 0xd4a574,
    roughness: 0.5,
    metalness: 0.1,
  });
  const top = new THREE.Mesh(topGeo, topMat);
  top.position.y = 0.75;
  desk.add(top);

  // Legs
  const legPositions: [number, number][] = [
    [-0.8, -0.35],
    [0.8, -0.35],
    [-0.8, 0.35],
    [0.8, 0.35],
  ];
  for (const [lx, lz] of legPositions) {
    const legGeo = new THREE.BoxGeometry(0.05, 0.75, 0.05);
    const legMat = new THREE.MeshStandardMaterial({
      color: 0x333333,
      metalness: 0.6,
      roughness: 0.3,
    });
    const leg = new THREE.Mesh(legGeo, legMat);
    leg.position.set(lx, 0.375, lz);
    desk.add(leg);
  }

  // Monitor on desk
  const monitorGeo = new THREE.BoxGeometry(0.8, 0.5, 0.03);
  const monitorMat = new THREE.MeshStandardMaterial({
    color: 0x222222,
    emissive: 0x1a3d8b,
    emissiveIntensity: 0.2,
  });
  const monitor = new THREE.Mesh(monitorGeo, monitorMat);
  monitor.position.set(0, 1.1, -0.2);
  desk.add(monitor);

  // Monitor stand
  const standGeo = new THREE.CylinderGeometry(0.03, 0.05, 0.25, 8);
  const standMat = new THREE.MeshStandardMaterial({
    color: 0x333333,
    metalness: 0.7,
    roughness: 0.2,
  });
  const stand = new THREE.Mesh(standGeo, standMat);
  stand.position.set(0, 0.9, -0.2);
  desk.add(stand);

  // Chair behind desk
  const chairSeatGeo = new THREE.BoxGeometry(0.5, 0.05, 0.45);
  const chairMat = new THREE.MeshStandardMaterial({
    color: 0x2a2a2a,
    roughness: 0.7,
  });
  const chairSeat = new THREE.Mesh(chairSeatGeo, chairMat);
  chairSeat.position.set(0, 0.45, 0.7);
  desk.add(chairSeat);

  const chairBackGeo = new THREE.BoxGeometry(0.5, 0.6, 0.04);
  const chairBack = new THREE.Mesh(chairBackGeo, chairMat);
  chairBack.position.set(0, 0.78, 0.92);
  desk.add(chairBack);

  desk.position.set(2, 0, 1);
  desk.rotation.y = -Math.PI / 4;
  scene.add(desk);
}

function createPlants(scene: THREE.Scene): THREE.Group[] {
  const plants: THREE.Group[] = [];

  const plantPositions: [number, number, number][] = [
    [-3, 0, 4],
    [4, 0, -3],
    [-5, 0, -2],
    [1, 0, -5],
    [-2, 0, 5],
  ];

  for (const [px, py, pz] of plantPositions) {
    const plant = new THREE.Group();

    // Pot
    const potGeo = new THREE.CylinderGeometry(0.25, 0.2, 0.4, 8);
    const potMat = new THREE.MeshStandardMaterial({
      color: 0x8b5e3c,
      roughness: 0.8,
    });
    const pot = new THREE.Mesh(potGeo, potMat);
    pot.position.y = 0.2;
    plant.add(pot);

    // Soil
    const soilGeo = new THREE.CylinderGeometry(0.23, 0.23, 0.05, 8);
    const soilMat = new THREE.MeshStandardMaterial({
      color: 0x3a2a1a,
      roughness: 1.0,
    });
    const soil = new THREE.Mesh(soilGeo, soilMat);
    soil.position.y = 0.42;
    plant.add(soil);

    // Foliage — layered cones and spheres
    const foliageCount = 2 + Math.floor(Math.random() * 3);
    for (let f = 0; f < foliageCount; f++) {
      const isSphere = Math.random() > 0.5;
      const green = 0.3 + Math.random() * 0.3;
      const foliageColor = new THREE.Color(0.05, green, 0.1);

      let foliageMesh: THREE.Mesh;
      if (isSphere) {
        const fGeo = new THREE.SphereGeometry(0.15 + Math.random() * 0.15, 8, 8);
        const fMat = new THREE.MeshStandardMaterial({
          color: foliageColor,
          roughness: 0.8,
        });
        foliageMesh = new THREE.Mesh(fGeo, fMat);
      } else {
        const fGeo = new THREE.ConeGeometry(0.12 + Math.random() * 0.1, 0.4 + Math.random() * 0.3, 6);
        const fMat = new THREE.MeshStandardMaterial({
          color: foliageColor,
          roughness: 0.8,
        });
        foliageMesh = new THREE.Mesh(fGeo, fMat);
      }

      foliageMesh.position.set(
        (Math.random() - 0.5) * 0.2,
        0.55 + f * 0.2,
        (Math.random() - 0.5) * 0.2
      );
      plant.add(foliageMesh);
    }

    plant.position.set(px, py, pz);
    scene.add(plant);
    plants.push(plant);
  }

  return plants;
}

function createWaterFeature(scene: THREE.Scene): THREE.Mesh {
  // Circular basin
  const basinGeo = new THREE.RingGeometry(0.8, 1.2, 32);
  const basinMat = new THREE.MeshStandardMaterial({
    color: 0x555555,
    roughness: 0.3,
    metalness: 0.5,
    side: THREE.DoubleSide,
  });
  const basin = new THREE.Mesh(basinGeo, basinMat);
  basin.rotation.x = -Math.PI / 2;
  basin.position.set(-3, 0.05, 0);
  scene.add(basin);

  // Basin rim
  const rimGeo = new THREE.TorusGeometry(1.0, 0.05, 8, 32);
  const rimMat = new THREE.MeshStandardMaterial({
    color: 0x666666,
    metalness: 0.6,
    roughness: 0.3,
  });
  const rim = new THREE.Mesh(rimGeo, rimMat);
  rim.rotation.x = -Math.PI / 2;
  rim.position.set(-3, 0.1, 0);
  scene.add(rim);

  // Water surface
  const waterGeo = new THREE.CircleGeometry(0.95, 32);
  const waterMat = new THREE.MeshPhysicalMaterial({
    color: 0x3388aa,
    transparent: true,
    opacity: 0.5,
    roughness: 0.1,
    metalness: 0.2,
    side: THREE.DoubleSide,
  });
  const water = new THREE.Mesh(waterGeo, waterMat);
  water.rotation.x = -Math.PI / 2;
  water.position.set(-3, 0.08, 0);
  scene.add(water);

  return water;
}

function createParticles(scene: THREE.Scene): THREE.Points {
  const count = 300;
  const positions = new Float32Array(count * 3);

  for (let i = 0; i < count; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI * 0.4;
    const r = 2 + Math.random() * 7;

    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = 1 + r * Math.cos(phi);
    positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));

  const mat = new THREE.PointsMaterial({
    size: 0.04,
    color: 0xfff5e6,
    transparent: true,
    opacity: 0.5,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });

  const points = new THREE.Points(geo, mat);
  scene.add(points);
  return points;
}

function createLighting(scene: THREE.Scene): void {
  // Warm natural light from above
  const dirLight = new THREE.DirectionalLight(0xfff5e6, 1.0);
  dirLight.position.set(5, 12, 3);
  scene.add(dirLight);

  // Soft ambient
  const ambient = new THREE.AmbientLight(0xfff5e6, 0.3);
  scene.add(ambient);

  // Hemisphere — sky and ground
  const hemi = new THREE.HemisphereLight(0xddeeff, 0xc4a265, 0.3);
  scene.add(hemi);

  // Subtle center light
  const centerLight = new THREE.PointLight(0xfff5e6, 0.5, 12);
  centerLight.position.set(0, 3, 0);
  scene.add(centerLight);
}

function createFloor(scene: THREE.Scene): void {
  // Warm wooden floor
  const floorGeo = new THREE.CircleGeometry(9.5, 64);
  const floorMat = new THREE.MeshStandardMaterial({
    color: 0xc8a882,
    roughness: 0.6,
    metalness: 0.05,
  });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.01;
  floor.receiveShadow = true;
  scene.add(floor);
}

export function createPersonalDome(
  scene: THREE.Scene
): { animate: (time: number) => void } {
  // Light, airy atmosphere
  scene.fog = new THREE.FogExp2(0x1a2030, 0.015);
  scene.background = new THREE.Color(0x0d1520);

  createFloor(scene);
  const geodesicFrame = createGeodesicDome(scene);
  const { panels: dataPanels, lights: panelLights } = createDataPanels(scene);
  const connectionLines = createConnectionLines(scene, dataPanels);
  createCoordinatorDesk(scene);
  const plants = createPlants(scene);
  const waterPlane = createWaterFeature(scene);
  const particles = createParticles(scene);
  createLighting(scene);

  const objects: PersonalDomeObjects = {
    geodesicFrame,
    dataPanels,
    connectionLines,
    particles,
    waterPlane,
    plants,
    panelLights,
  };

  return {
    animate: (time: number) => {
      // Slow geodesic rotation
      objects.geodesicFrame.rotation.y = time * 0.01;

      // Data panel pulse — each glows softly
      objects.dataPanels.forEach((panel, idx) => {
        const mat = panel.material as THREE.MeshStandardMaterial;
        mat.emissiveIntensity = 0.12 + Math.sin(time * 0.8 + idx * 1.05) * 0.08;
      });

      // Panel lights breathing
      objects.panelLights.forEach((light, idx) => {
        light.intensity = 0.35 + Math.sin(time * 0.6 + idx * 1.05) * 0.15;
      });

      // Connection line opacity wave
      objects.connectionLines.forEach((line, idx) => {
        const mat = line.material as THREE.LineBasicMaterial;
        mat.opacity = 0.2 + Math.sin(time * 0.5 + idx * 0.9) * 0.15;
      });

      // Particle drift
      objects.particles.rotation.y = time * 0.015;
      const posAttr = objects.particles.geometry.getAttribute("position");
      const positions = posAttr.array as Float32Array;
      for (let i = 0; i < positions.length; i += 3) {
        positions[i + 1] += Math.sin(time * 0.3 + i * 0.1) * 0.0008;
      }
      posAttr.needsUpdate = true;

      // Water ripple
      const waterPos = objects.waterPlane.geometry.getAttribute("position");
      const wArr = waterPos.array as Float32Array;
      for (let i = 0; i < wArr.length; i += 3) {
        const x = wArr[i];
        const z = wArr[i + 2];
        // Subtle vertical displacement for ripple
        wArr[i + 1] = Math.sin(x * 4 + time * 2) * 0.01 + Math.cos(z * 4 + time * 1.5) * 0.01;
      }
      waterPos.needsUpdate = true;

      // Plants gentle sway
      objects.plants.forEach((plant, idx) => {
        plant.rotation.z = Math.sin(time * 0.4 + idx * 1.2) * 0.02;
      });
    },
  };
}
