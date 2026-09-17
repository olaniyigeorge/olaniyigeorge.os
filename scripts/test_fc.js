const fc = require('C:/nvm4w/nodejs/node_modules/firecrawl/dist/index.cjs');
console.log('loaded:', typeof fc);
console.log('keys:', Object.keys(fc).slice(0, 20).join(', '));
const m = fc.Murk || fc.default;
if (m) console.log('Murk/client:', typeof m, m.name || 'n/a');
