import * as THREE from "three";

/**
 * World 2: Broken Capitol
 *
 * A cracked government dome with harsh fluorescent lighting,
 * a plastic chair, scattered papers, a take-a-number sign.
 * The feeling: abandonment, bureaucratic neglect, the human
 * reduced to a number.
 */

interface BrokenCapitolObjects {
  flickerLights: THREE.PointLight[];
  papers: THREE.Mesh[];
  signLight: THREE.PointLight;
  crackLight: THREE.DirectionalLight;
}

function createCanvasTexture(
  text: string,
  width: number,
  height: number,
  options?: {
    fontSize?: number;
    fontFamily?: string;
    color?: string;
    bgColor?: string;
    bold?: boolean;
  }
): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Could not get 2d context");

  const bgColor = options?.bgColor ?? "#E8E4D8";
  const color = options?.color ?? "#333333";
  const fontSize = options?.fontSize ?? 48;
  const fontFamily = options?.fontFamily ?? "monospace";
  const bold = options?.bold ?? false;

  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, width, height);

  // Aging / stain effects
  ctx.fillStyle = "rgba(180, 170, 140, 0.3)";
  for (let i = 0; i < 5; i++) {
    const sx = Math.random() * width;
    const sy = Math.random() * height;
    ctx.beginPath();
    ctx.arc(sx, sy, 20 + Math.random() * 40, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.fillStyle = color;
  ctx.font = `${bold ? "bold " : ""}${fontSize}px ${fontFamily}`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  // Word-wrap text
  const words = text.split(" ");
  const lines: string[] = [];
  let currentLine = "";
  const maxWidth = width * 0.8;

  for (const word of words) {
    const testLine = currentLine ? `${currentLine} ${word}` : word;
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && currentLine) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) lines.push(currentLine);

  const lineHeight = fontSize * 1.3;
  const startY = height / 2 - ((lines.length - 1) * lineHeight) / 2;
  lines.forEach((line, idx) => {
    ctx.fillText(line, width / 2, startY + idx * lineHeight);
  });

  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  return texture;
}

function createBrokenDome(scene: THREE.Scene): THREE.Group {
  const domeGroup = new THREE.Group();

  // Main dome shell with missing segments (cracks)
  const radius = 12;
  const widthSegs = 16;
  const heightSegs = 16;

  // Create dome in sections, omitting some for cracks
  for (let wi = 0; wi < widthSegs; wi++) {
    for (let hi = 0; hi < heightSegs / 2; hi++) {
      // Skip segments to create cracks
      const skip =
        (wi === 3 && hi >= 2 && hi <= 5) ||
        (wi === 4 && hi >= 1 && hi <= 4) ||
        (wi === 10 && hi >= 3 && hi <= 6) ||
        (wi === 11 && hi >= 2 && hi <= 3) ||
        (wi === 7 && hi >= 5 && hi <= 7);

      if (skip) continue;

      const phiStart = (wi / widthSegs) * Math.PI * 2;
      const phiLen = (1 / widthSegs) * Math.PI * 2;
      const thetaStart = (hi / heightSegs) * Math.PI;
      const thetaLen = (1 / heightSegs) * Math.PI;

      const segGeo = new THREE.SphereGeometry(
        radius,
        2,
        2,
        phiStart,
        phiLen,
        thetaStart,
        thetaLen
      );

      // Offset some vertices for damage
      const positions = segGeo.getAttribute("position");
      const posArray = positions.array as Float32Array;
      const adjacentToCrack =
        (wi === 2 && hi >= 2 && hi <= 5) ||
        (wi === 5 && hi >= 1 && hi <= 4) ||
        (wi === 9 && hi >= 3 && hi <= 6) ||
        (wi === 12 && hi >= 2 && hi <= 3);

      if (adjacentToCrack) {
        for (let v = 0; v < posArray.length; v += 3) {
          posArray[v] += (Math.random() - 0.5) * 0.15;
          posArray[v + 1] += (Math.random() - 0.5) * 0.15;
          posArray[v + 2] += (Math.random() - 0.5) * 0.15;
        }
        positions.needsUpdate = true;
      }

      const segMat = new THREE.MeshStandardMaterial({
        color: 0x8a8a8a,
        roughness: 0.85,
        metalness: 0.05,
        side: THREE.BackSide,
      });

      const seg = new THREE.Mesh(segGeo, segMat);
      domeGroup.add(seg);
    }
  }

  // Drum / walls — dingy concrete
  const drumGeo = new THREE.CylinderGeometry(12, 12, 5, 16, 1, true);
  const drumMat = new THREE.MeshStandardMaterial({
    color: 0x7a7a72,
    roughness: 0.9,
    metalness: 0.02,
    side: THREE.BackSide,
  });
  const drum = new THREE.Mesh(drumGeo, drumMat);
  drum.position.y = -2.5;
  domeGroup.add(drum);

  scene.add(domeGroup);
  return domeGroup;
}

function createFloor(scene: THREE.Scene): void {
  // Dirty linoleum floor
  const floorGeo = new THREE.PlaneGeometry(24, 24);
  const floorMat = new THREE.MeshStandardMaterial({
    color: 0x9a9580,
    roughness: 0.95,
    metalness: 0.0,
  });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -5;
  floor.receiveShadow = true;
  scene.add(floor);

  // Scuff marks
  for (let i = 0; i < 8; i++) {
    const markGeo = new THREE.PlaneGeometry(
      0.5 + Math.random() * 2,
      0.1 + Math.random() * 0.3
    );
    const markMat = new THREE.MeshStandardMaterial({
      color: 0x6a6555,
      roughness: 1.0,
      transparent: true,
      opacity: 0.4,
    });
    const mark = new THREE.Mesh(markGeo, markMat);
    mark.rotation.x = -Math.PI / 2;
    mark.rotation.z = Math.random() * Math.PI;
    mark.position.set(
      (Math.random() - 0.5) * 10,
      -4.99,
      (Math.random() - 0.5) * 10
    );
    scene.add(mark);
  }
}

function createPlasticChair(scene: THREE.Scene): THREE.Group {
  const chair = new THREE.Group();
  const plasticColor = 0xb0a890;
  const legColor = 0x888888;

  // Seat
  const seatGeo = new THREE.BoxGeometry(0.5, 0.04, 0.45);
  const seatMat = new THREE.MeshStandardMaterial({
    color: plasticColor,
    roughness: 0.8,
  });
  const seat = new THREE.Mesh(seatGeo, seatMat);
  seat.position.y = 0.45;
  chair.add(seat);

  // Back
  const backGeo = new THREE.BoxGeometry(0.5, 0.5, 0.04);
  const backMat = new THREE.MeshStandardMaterial({
    color: plasticColor,
    roughness: 0.8,
  });
  const back = new THREE.Mesh(backGeo, backMat);
  back.position.set(0, 0.72, -0.2);
  back.rotation.x = -0.05;
  chair.add(back);

  // Legs — 4 metal tubes
  const legPositions: [number, number][] = [
    [-0.2, -0.18],
    [0.2, -0.18],
    [-0.2, 0.18],
    [0.2, 0.18],
  ];
  for (const [lx, lz] of legPositions) {
    const legGeo = new THREE.CylinderGeometry(0.015, 0.015, 0.45, 6);
    const legMat = new THREE.MeshStandardMaterial({
      color: legColor,
      roughness: 0.4,
      metalness: 0.5,
    });
    const leg = new THREE.Mesh(legGeo, legMat);
    leg.position.set(lx, 0.225, lz);
    chair.add(leg);
  }

  chair.position.set(0, -5, 0);
  scene.add(chair);
  return chair;
}

function createTakeANumberSign(scene: THREE.Scene): THREE.PointLight {
  const texture = createCanvasTexture(
    "PLEASE TAKE A NUMBER",
    512,
    256,
    {
      fontSize: 52,
      fontFamily: "monospace",
      color: "#880000",
      bgColor: "#E8E0C8",
      bold: true,
    }
  );

  const signGeo = new THREE.PlaneGeometry(2.0, 1.0);
  const signMat = new THREE.MeshStandardMaterial({
    map: texture,
    roughness: 0.7,
  });
  const sign = new THREE.Mesh(signGeo, signMat);
  sign.position.set(0, 0.5, -10);
  scene.add(sign);

  // Number dispenser below sign
  const dispenserGeo = new THREE.BoxGeometry(0.4, 0.5, 0.15);
  const dispenserMat = new THREE.MeshStandardMaterial({
    color: 0xcc3333,
    roughness: 0.6,
  });
  const dispenser = new THREE.Mesh(dispenserGeo, dispenserMat);
  dispenser.position.set(0, -0.2, -9.95);
  scene.add(dispenser);

  // Current number display
  const numTexture = createCanvasTexture("247", 128, 128, {
    fontSize: 64,
    color: "#FF0000",
    bgColor: "#111111",
    bold: true,
  });
  const numGeo = new THREE.PlaneGeometry(0.3, 0.3);
  const numMat = new THREE.MeshStandardMaterial({
    map: numTexture,
    emissive: 0xff0000,
    emissiveIntensity: 0.3,
    emissiveMap: numTexture,
  });
  const numDisplay = new THREE.Mesh(numGeo, numMat);
  numDisplay.position.set(0.8, 0.5, -9.9);
  scene.add(numDisplay);

  // "NOW SERVING" text
  const servingTexture = createCanvasTexture("NOW SERVING: 84", 256, 128, {
    fontSize: 36,
    color: "#FF3333",
    bgColor: "#0A0A0A",
    bold: true,
  });
  const servingGeo = new THREE.PlaneGeometry(1.5, 0.5);
  const servingMat = new THREE.MeshStandardMaterial({
    map: servingTexture,
    emissive: 0xff0000,
    emissiveIntensity: 0.2,
    emissiveMap: servingTexture,
  });
  const servingDisplay = new THREE.Mesh(servingGeo, servingMat);
  servingDisplay.position.set(-2.5, 1.5, -9.9);
  scene.add(servingDisplay);

  // Sickly light above sign
  const signLight = new THREE.PointLight(0xffffff, 1.0, 8);
  signLight.position.set(0, 2, -9);
  scene.add(signLight);

  return signLight;
}

function createScatteredPapers(scene: THREE.Scene): THREE.Mesh[] {
  const papers: THREE.Mesh[] = [];

  for (let i = 0; i < 15; i++) {
    const w = 0.15 + Math.random() * 0.15;
    const h = 0.2 + Math.random() * 0.1;
    const paperGeo = new THREE.PlaneGeometry(w, h);
    const shade = 0.85 + Math.random() * 0.1;
    const paperMat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(shade, shade * 0.98, shade * 0.92),
      roughness: 0.9,
      side: THREE.DoubleSide,
    });
    const paper = new THREE.Mesh(paperGeo, paperMat);

    paper.position.set(
      (Math.random() - 0.5) * 8,
      -4.98 + Math.random() * 0.02,
      (Math.random() - 0.5) * 8
    );
    paper.rotation.x = -Math.PI / 2 + (Math.random() - 0.5) * 0.3;
    paper.rotation.z = Math.random() * Math.PI * 2;

    scene.add(paper);
    papers.push(paper);
  }

  return papers;
}

function createExposedPipes(scene: THREE.Scene): void {
  // Pipes running along the upper walls
  const pipeConfigs: { start: THREE.Vector3; end: THREE.Vector3; radius: number }[] = [
    {
      start: new THREE.Vector3(-10, 3, -8),
      end: new THREE.Vector3(10, 3.5, -8),
      radius: 0.08,
    },
    {
      start: new THREE.Vector3(-10, 2, -9),
      end: new THREE.Vector3(8, 2.3, -9),
      radius: 0.05,
    },
    {
      start: new THREE.Vector3(9, -2, -9),
      end: new THREE.Vector3(9, 4, -9),
      radius: 0.06,
    },
    {
      start: new THREE.Vector3(-9, -3, -8),
      end: new THREE.Vector3(-9, 3, -8),
      radius: 0.07,
    },
    {
      start: new THREE.Vector3(-8, 1.5, -9.5),
      end: new THREE.Vector3(6, 1.5, -9.5),
      radius: 0.04,
    },
  ];

  for (const cfg of pipeConfigs) {
    const dir = new THREE.Vector3().subVectors(cfg.end, cfg.start);
    const len = dir.length();
    const pipeGeo = new THREE.CylinderGeometry(cfg.radius, cfg.radius, len, 8);
    const pipeMat = new THREE.MeshStandardMaterial({
      color: 0x666660,
      roughness: 0.6,
      metalness: 0.4,
    });
    const pipe = new THREE.Mesh(pipeGeo, pipeMat);

    const mid = new THREE.Vector3().addVectors(cfg.start, cfg.end).multiplyScalar(0.5);
    pipe.position.copy(mid);

    // Orient along direction
    const axis = new THREE.Vector3(0, 1, 0);
    const normalized = dir.clone().normalize();
    const quat = new THREE.Quaternion().setFromUnitVectors(axis, normalized);
    pipe.quaternion.copy(quat);

    scene.add(pipe);
  }

  // Dangling wires
  for (let i = 0; i < 4; i++) {
    const wireGeo = new THREE.CylinderGeometry(0.01, 0.01, 1.5 + Math.random(), 4);
    const wireMat = new THREE.MeshStandardMaterial({
      color: i % 2 === 0 ? 0x444444 : 0x664422,
      roughness: 0.9,
    });
    const wire = new THREE.Mesh(wireGeo, wireMat);
    wire.position.set(
      (Math.random() - 0.5) * 6,
      3 + Math.random() * 2,
      -8 + Math.random() * 2
    );
    wire.rotation.z = (Math.random() - 0.5) * 0.5;
    wire.rotation.x = (Math.random() - 0.5) * 0.3;
    scene.add(wire);
  }
}

function createLighting(scene: THREE.Scene): THREE.PointLight[] {
  // Harsh, cold ambient
  const ambient = new THREE.AmbientLight(0xd0d0e0, 0.2);
  scene.add(ambient);

  // Fluorescent-style point lights
  const lights: THREE.PointLight[] = [];
  const lightPositions: [number, number, number][] = [
    [-4, 5, -3],
    [4, 5, -3],
    [0, 5, 3],
    [-3, 5, 5],
    [3, 5, -7],
  ];

  for (const [lx, ly, lz] of lightPositions) {
    const light = new THREE.PointLight(0xf0f0ff, 1.2, 15);
    light.position.set(lx, ly, lz);
    scene.add(light);
    lights.push(light);

    // Visible fluorescent tube housing
    const housingGeo = new THREE.BoxGeometry(1.2, 0.05, 0.15);
    const housingMat = new THREE.MeshStandardMaterial({
      color: 0xf0f0ff,
      emissive: 0xf0f0ff,
      emissiveIntensity: 0.5,
      roughness: 0.3,
    });
    const housing = new THREE.Mesh(housingGeo, housingMat);
    housing.position.set(lx, ly + 0.1, lz);
    scene.add(housing);
  }

  // Cold blue light leaking through dome crack
  const crackLight = new THREE.DirectionalLight(0x4488ff, 0.8);
  crackLight.position.set(3, 15, -2);
  crackLight.target.position.set(2, -5, -1);
  scene.add(crackLight);
  scene.add(crackLight.target);

  return lights;
}

function createAdditionalChairs(scene: THREE.Scene): void {
  // Row of empty chairs — bureaucratic waiting room
  for (let i = 0; i < 6; i++) {
    const chairGroup = new THREE.Group();
    const plasticColor = i % 2 === 0 ? 0xa09878 : 0x98a088;

    const seatGeo = new THREE.BoxGeometry(0.5, 0.04, 0.45);
    const seatMat = new THREE.MeshStandardMaterial({
      color: plasticColor,
      roughness: 0.8,
    });
    const seatMesh = new THREE.Mesh(seatGeo, seatMat);
    seatMesh.position.y = 0.45;
    chairGroup.add(seatMesh);

    const backGeo = new THREE.BoxGeometry(0.5, 0.4, 0.04);
    const backMat = new THREE.MeshStandardMaterial({
      color: plasticColor,
      roughness: 0.8,
    });
    const backMesh = new THREE.Mesh(backGeo, backMat);
    backMesh.position.set(0, 0.67, -0.2);
    chairGroup.add(backMesh);

    for (const [lx, lz] of [
      [-0.2, -0.18],
      [0.2, -0.18],
      [-0.2, 0.18],
      [0.2, 0.18],
    ] as [number, number][]) {
      const legGeo = new THREE.CylinderGeometry(0.015, 0.015, 0.45, 6);
      const legMat = new THREE.MeshStandardMaterial({
        color: 0x888888,
        metalness: 0.5,
        roughness: 0.4,
      });
      const leg = new THREE.Mesh(legGeo, legMat);
      leg.position.set(lx, 0.225, lz);
      chairGroup.add(leg);
    }

    chairGroup.position.set(-3.5 + i * 1.2, -5, -6);
    chairGroup.rotation.y = Math.PI;
    scene.add(chairGroup);
  }
}

export function createBrokenCapitol(
  scene: THREE.Scene
): { animate: (time: number) => void } {
  // Cold institutional fog
  scene.fog = new THREE.FogExp2(0x1a1a22, 0.02);
  scene.background = new THREE.Color(0x0a0a10);

  createBrokenDome(scene);
  createFloor(scene);
  createPlasticChair(scene);
  createAdditionalChairs(scene);
  const signLight = createTakeANumberSign(scene);
  const papers = createScatteredPapers(scene);
  createExposedPipes(scene);
  const flickerLights = createLighting(scene);

  const crackLight = new THREE.DirectionalLight(0x4488ff, 0.5);
  crackLight.position.set(3, 15, -2);
  scene.add(crackLight);

  const objects: BrokenCapitolObjects = {
    flickerLights,
    papers,
    signLight,
    crackLight,
  };

  return {
    animate: (time: number) => {
      // Fluorescent flicker effect
      objects.flickerLights.forEach((light, idx) => {
        const flicker = Math.sin(time * 15 + idx * 3.7) > 0.9 ? 0.3 : 1.0;
        const hum = 1.0 + Math.sin(time * 8 + idx * 2.1) * 0.1;
        light.intensity = 1.2 * flicker * hum;
      });

      // Sign light buzz
      objects.signLight.intensity =
        1.0 + Math.sin(time * 12) * 0.15 + (Math.random() > 0.97 ? -0.5 : 0);

      // Subtle paper drift (as if from HVAC)
      objects.papers.forEach((paper, idx) => {
        paper.rotation.z += Math.sin(time * 0.3 + idx) * 0.0003;
      });

      // Crack light pulses cold
      objects.crackLight.intensity = 0.5 + Math.sin(time * 0.4) * 0.2;
    },
  };
}
