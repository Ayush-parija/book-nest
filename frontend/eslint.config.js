import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

// ESLint configuration for the React and Vite project
export default defineConfig([
  // Ignore generated build files
  globalIgnores(['dist']),
  {
    // Apply these rules to JavaScript and JSX files
    files: ['**/*.{js,jsx}'],

    // Enable recommended ESLint and React configurations
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],

    // Configure language settings
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])