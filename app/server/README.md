# server


### Tmp

#### Possible tsconfig settings

From [full-stack-app/backend](https://github.com/Leejjon/full-stack-app/blob/main/backend/tsconfig.json)
```json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true // If you disable this, you'll get an error:
    // TypeError: (0 , s.default) is not a function
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules"],
  "target": "es2017",
  "module": "commonjs",
  "lib": ["es2017"]
}
```

[Node 18 base](https://github.com/tsconfig/bases/blob/main/bases/node18.json)
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "display": "Node 18",

  "_version": "18.2.0",

  "compilerOptions": {
    "lib": ["es2023"],
    "module": "node16",
    "target": "es2022",

    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node16"
  }
}
```

[Node recommended base](https://github.com/tsconfig/bases/blob/main/bases/recommended.json)
```json
{
  "compilerOptions": {
    "target": "es2015",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "$schema": "https://json.schemastore.org/tsconfig",
  "display": "Recommended"
}
```
