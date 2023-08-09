/** @type {import('tailwindcss').Config} */

import plugin from 'tailwindcss/plugin';

module.exports = {
  content: ['./src/**/*.html', './src/**/*.js', './src/**/*.jsx'],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#DDD6CB',
          secondary: '#F1EEEA',
          accent: '#75716B',
        },
      },
    },
  },
  plugins: [
    plugin(function ({ addUtilities, theme }) {
      addUtilities({
        '.button-1': {
          backgroundColor: theme('colors.brand.primary'),
          padding: '0.5rem 1rem',
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.semibold'),
          border: '1px solid ',
          borderColor: theme('colors.gray.300'),
          '&:hover': {
            backgroundColor: theme('colors.brand.secondary'),
          },
        },
        // breakpoint
        '.button-2': {
          backgroundColor: theme('colors.brand.accent'),
          padding: '0.5rem 1rem',
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.semibold'),
          border: '1px solid ',
          borderColor: theme('colors.gray.300'),
          color: theme('colors.gray.50'),
        },
        'input[type="text"]': {
          borderColor: theme('colors.gray.300') + ' !important',
          backgroundColor: theme('colors.white') + '!important',
        },
        select: {
          borderColor: theme('colors.gray.300') + ' !important',
          backgroundColor: theme('colors.white') + '!important',
        },
      });
    }),
    require('@tailwindcss/forms'),
    require('flowbite/plugin'),
  ],
};
