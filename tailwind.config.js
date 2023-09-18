/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './node_modules/flowbite/**/*.js'
    ],
    theme: {
        extend: {
            colors: {
                // primary: '#2E3192',
                primary: '#04047B',
                secondary: '#FFA500',
                sidebarfont: '#e6efff',
                sidebaricons: '#7a9dff',
            },
        },
    },
    plugins: [
        require('flowbite/plugin')
    ],
  }