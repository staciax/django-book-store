import globals from 'globals';
import pluginJs from '@eslint/js';
import eslintConfigPrettier from 'eslint-config-prettier';

/** @type {import('eslint').Linter.Config[]} */
const eslintConfig = [
  {
    ignores: [
      '**/node_modules/**/*',
      '**/dist/*',
      '**/.venv/**/*',
      '**/static/admin/*',
      '**/static/store/*',
      '**/static/django-browser-reload/*',
      '**/.*/**/*',
    ],
  },
  pluginJs.configs.recommended,
  eslintConfigPrettier,
  {
    files: ['**/store/static/**/*.js'],
    languageOptions: {
      globals: globals.browser,
    },
  },
];

export default eslintConfig;
