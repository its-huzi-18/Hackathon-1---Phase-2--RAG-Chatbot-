// Type declarations for Docusaurus module aliases used at build time.
// These aliases (for example `@theme/Layout`) are provided by Docusaurus
// at runtime. TypeScript doesn't know about them by default, so we declare
// them as generic React components/values to satisfy the type checker.

declare module '@theme/*' {
  import type {ComponentType, PropsWithChildren} from 'react';
  const Component: ComponentType<PropsWithChildren<any>>;
  export default Component;
}

declare module '@site/*' {
  const value: any;
  export default value;
}

declare module '@generated/*' {
  const value: any;
  export default value;
}

declare module '@docusaurus/*' {
  const value: any;
  export default value;
}
