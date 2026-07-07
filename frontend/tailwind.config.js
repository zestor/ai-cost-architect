export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: '#28251D',
        muted: '#7A7974',
        faint: '#BAB9B4',
        surface: '#F7F6F2',
        surface2: '#F9F8F5',
        card: '#FBFBF9',
        border: '#D4D1CA',
        accent: '#01696F',
        accent2: '#0C4E54',
        warn: '#964219',
        err: '#A12C7B',
        ok: '#437A22'
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif']
      }
    }
  },
  plugins: []
};
