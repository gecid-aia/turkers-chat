module.exports = {
  extends: ['airbnb-base', 'prettier'],
  plugins: ['prettier'],
  rules: {
    'prettier/prettier': 'error',
    'arrow-body-style': ['error', 'as-needed'],
    'no-param-reassign': 'off',
    'no-console': ['error', { allow: ['error'] }],
    'no-underscore-dangle': 'off',
    'import/prefer-default-export': 'off'
  },
  env: {
    es6: true,
    jest: true,
    browser: true,
  },
};
