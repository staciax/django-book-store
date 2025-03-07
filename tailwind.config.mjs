import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
// import aspectRatio from '@tailwindcss/aspect-ratio';

// /** @type {import('tailwindcss').Config} */
export default {
  content: [
    // (BASE_DIR/templates)
    './templates/**/*.html',
    // (BASE_DIR/<any_app_name>/templates)
    './**/templates/**/*.html',
    // (BASE_DIR/routes)
    './routes/**/*.html',
    // (BASE_DIR/<any_app_name>/routes)
    './**/routes/**/*.html',
  ],
  theme: {
    container: {
      screens: {
        xl: '1200px',
        '2xl': '1200px',
      },
    },
    extend: {
      colors: {
        primary: '#5D87FF',
        'light-primary': '#ECF2FF',
        'dark-primary': '#2A3547',
        secondary: '#1895f5',
        'light-secondary': '#DFE5EF',
        tertiary: '#4570EA',
        'light-tertiary': '#d8d8d8',
        promptpay: '#113566',
      },
      fontFamily: {
        prompt: ['Prompt', 'sans-serif'],
      },
    },
  },
  plugins: [forms, typography],
};
