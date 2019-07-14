module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended',
    // 'plugin:prettier/recommended',
    'prettier',
    'prettier/vue'
  ],
  plugins: [
    'prettier'
  ],
  // add your custom rules here
  rules: {
    'nuxt/no-cjs-in-config': 'off',
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'vue/html-indent': ['error', 4, {
      'attribute': 1
    }],
    "vue/script-indent": ["error", 4, {
      "baseIndent": 1
    }],
    "vue/max-attributes-per-line": [1, {
        "singleline": 3,
      }],
    'vue/no-unused-vars': 'off',
    'vue/require-valid-default-prop': 'off',
  },
  "overrides": [
    {
      "files": ["*.vue", "*.js"],
      "rules": {
        "indent": "off"
      }
    }
  ]
}
