import dispose from './patch/dispose.js';
export type WatOptions = {
    /**
     * - Initialization options for the libwabt module
     */
    init?: Object;
    /**
     * - Import object for the WebAssembly module
     */
    import?: Object;
    /**
     * - Features for the WebAssembly module
     */
    features?: Object;
    /**
     * - Binary options for the WebAssembly module
     */
    binary?: Object;
    /**
     * - Name of the WebAssembly module
     */
    name?: string;
};
export default _default;
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
declare function _default(options?: WatOptions): (template: TemplateStringsArray, ...values: any[]) => Promise<WebAssembly.Instance & WebAssembly.WebAssemblyInstantiatedSource & {
    [dispose]: () => void;
}>;
