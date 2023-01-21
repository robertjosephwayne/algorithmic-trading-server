module.exports = {
    parser: '@typescript-eslint/parser',
    extends: ['plugin:@typescript-eslint/recommended', 'prettier/@typescript-eslint', 'plugin:prettier/recommended'],
    parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
    },
    env: {
        es6: true,
        node: true,
    },
    rules: {
        "camelcase": "error",
        "spaced-comment": "error",
        "quotes": ["error", "single"],
        "no-duplicate-imports": "error",
        'no-multiple-empty-lines': 'error',
        'prefer-const': 'error',
    },
};