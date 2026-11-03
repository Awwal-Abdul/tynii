# libwabt.js

Both [libwabt.js](./libwabt.js) and [libwabt.wasm](./libwabt.wasm) are forked directly from https://github.com/WebAssembly/wabt/tree/main#readme

This utility simply borrows those files and re-package these in a compressed base64 version of the original WASM binary.

This allows developers to use directly the WABT JS module without needing to land files around or building via Emscripten by hand.

[LICENCE](./LICENSE) and all credits remains intact, the [index.js](./index.js) entry point is just a wrapper that decode at runtime the WASM binary once before bootstrapping the module.
