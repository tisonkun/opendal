// Temporary diagnostics for Docusaurus 3.10.1; not intended for the final PR.
const path = require("node:path");
const { performance } = require("node:perf_hooks");

function log(message) {
  console.log(`[PROFILE ${new Date().toISOString()}] ${message}`);
}

const crates = require("crates-llms-txt");
const fromLocal = crates.fromLocal;
crates.fromLocal = function (...args) {
  const started = performance.now();
  log(`crates-llms-txt.fromLocal started: ${JSON.stringify(args)}`);
  try {
    const result = fromLocal.apply(this, args);
    log(`crates-llms-txt.fromLocal result: ${JSON.stringify(result ? {
      libName: result.libName,
      version: result.version,
      sessions: result.sessions?.length,
      fullSessions: result.fullSessions?.length,
    } : null)}`);
    return result;
  } finally {
    log(`crates-llms-txt.fromLocal finished: ${((performance.now() - started) / 1000).toFixed(3)} s`);
  }
};

const core = path.dirname(require.resolve("@docusaurus/core/package.json"));
const siteModule = require(path.join(core, "lib/server/site.js"));
const loadSite = siteModule.loadSite;
siteModule.loadSite = async function (...args) {
  const site = await loadSite.apply(this, args);
  for (const plugin of site.props.plugins) {
    if (!plugin.postBuild) continue;
    const postBuild = plugin.postBuild;
    plugin.postBuild = async function (...hookArgs) {
      const started = performance.now();
      log(`${plugin.name}.postBuild started`);
      try {
        return await postBuild.apply(this, hookArgs);
      } finally {
        log(`${plugin.name}.postBuild finished: ${((performance.now() - started) / 1000).toFixed(3)} s`);
      }
    };
  }
  return site;
};
