const globals = require('globals');
const { configs: eslintConfigs } = require('@eslint/js');
const eslintPluginPrettierRecommended = require('eslint-config-prettier');

module.exports = [
  eslintConfigs.recommended,
  eslintPluginPrettierRecommended,
  {
    files: ['**/*.js'],
    rules: {
      ...eslintPluginPrettierRecommended.rules,
      semi: ['error', 'always'],
      quotes: ['error', 'single'],
    },
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.browser,
        ...globals.es2021,
        ...globals.commonjs,
      },
    },
    ignores: ['**/node_modules', '**/dist', '**/.git', '**/.venv'],
  },
];
