module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  safelist: [
    'hidden', 'flex', 'active',
    'bg-green-600', 'bg-primary', 'bg-gradient-to-br',
    'ranking-fade-in', 'rankings-transitioning',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#e8a020',
        'background-light': '#f6f1e7',
        'background-dark': '#14100c',
        'surface-dark': '#211b15',
        'tomato': '#e23b2e',
      },
      fontFamily: { 'display': ['Inter', 'sans-serif'] },
      borderRadius: { 'DEFAULT': '0.5rem', 'lg': '1rem', 'xl': '1.5rem', 'full': '9999px' },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
