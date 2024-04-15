import 'react';

type AmbiguousObject = Record<string, unknown>;

declare module '*.svg' {
    const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
    export default content;
}

declare global {
    type RenderAppFunc = (data: AmbiguousObject) => void;

    interface Window {
        renderApp: RenderAppFunc;
    }
}
