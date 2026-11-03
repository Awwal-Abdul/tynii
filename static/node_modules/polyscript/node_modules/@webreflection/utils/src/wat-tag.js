// @ts-check

import dispose from './patch/dispose.js';
import libwabt from './libwabt/index.js';
import plain from './plain-tag.js';
import dedent from './dedent.js';

const { assign } = Object;

/**
 * @typedef {Object} WatOptions
 * @property {Object} [init] - Initialization options for the libwabt module
 * @property {Object} [import] - Import object for the WebAssembly module
 * @property {Object} [features] - Features for the WebAssembly module
 * @property {Object} [binary] - Binary options for the WebAssembly module
 * @property {string} [name] - Name of the WebAssembly module
 */

/**
 * @param {WatOptions} [options] - Options for the Wat module
 * @returns
 */
export default (options = {}) => {
  const lib = libwabt(options.init ?? {});
  /**
   * @param {TemplateStringsArray} template - Template string
   * @param {...any} values - Values to interpolate into the template
   * @returns
   */
  return async (template, ...values) => {
    const importObject = options.import ?? {};
    const features = options.features ?? {};
    const wabt = await lib;
    // @ts-ignore
    const module = wabt.parseWat(
      options.name ?? 'test.wast',
      dedent(plain(template, ...values)).trim(),
      features
    );
    module.validate(features);
    return assign(
      // @ts-ignore
      await WebAssembly.instantiate(module.toBinary(options.binary ?? {}).buffer, importObject),
      {
        [dispose]() {
          module.destroy();
        }
      }
    );
  };
};
