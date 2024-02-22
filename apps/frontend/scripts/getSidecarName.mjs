const execa = await import('execa');
import fs from 'fs';
import path from 'path';

const filepath = process.argv[2];

if (!filepath) {
  console.error('Please provide a filepath argument');
  process.exit(1);
}

if (!fs.existsSync(filepath)) {
  console.error('File does not exist');
  process.exit(1);
}

const filename = path.basename(filepath);


async function main() {
  const { stdout: rustInfo } = await execa.execa('rustc', ['-vV']);
  const targetTripleMatch = /host: (\S+)/g.exec(rustInfo);
  const targetTriple = targetTripleMatch ? targetTripleMatch[1] : null;

  if (!targetTriple) {
    console.error('Failed to determine platform target triple');
    return;
  }

  console.log(
    process.platform === 'win32' ?
    `${filename}-${targetTriple}.exe`:
    `${filename}-${targetTriple}`
  )
  
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});