export let version = '1.0';

export default class {
  constructor(customVersion) {
    console.log(`Framework v${customVersion || version} initialized`);
  }
}
