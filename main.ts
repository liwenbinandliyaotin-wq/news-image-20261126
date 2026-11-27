// News image 26 Nov 2026 — entrypoint. Node 22, standard library only.
//
// The finished picture (entry.png, 1024x1024) lives next to this file. This
// program checks it is really a PNG of the size the bounty allows, then
// places an exact copy at <output>/entry.png, where <output> comes from
// MAKEFUN_OUTPUT_DIR and defaults to /output. Copying bytes instead of
// redrawing keeps every run identical, so the judge always sees the same
// image.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//   # then compare: cmp entry.png out/entry.png

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// PNG signature: 8 bytes every PNG file starts with.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

// Bounty limits for the picture.
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

const here = dirname(fileURLToPath(import.meta.url));
const picture = join(here, 'entry.png');
const bytes = readFileSync(picture);

if (bytes.length === 0) {
  throw new Error('entry.png is empty, nothing to copy');
}
if (!bytes.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png does not start with the PNG signature');
}
if (bytes.length > MAX_BYTES) {
  throw new Error(
    `entry.png is ${bytes.length} bytes, over the ${MAX_BYTES} byte limit`,
  );
}

// The IHDR chunk holds the width and height as big-endian uint32s at
// offsets 16 and 20. Confirm the chunk really is IHDR, then confirm the
// picture fits the 1024x1024 cap.
const chunkType = bytes.subarray(12, 16).toString('ascii');
if (chunkType !== 'IHDR') {
  throw new Error(`first PNG chunk is ${chunkType}, expected IHDR`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over the ${MAX_SIDE} cap`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
copyFileSync(picture, target);

const written = statSync(target).size;
console.log(`copied ${written} bytes (${width}x${height}) to ${target}`);
