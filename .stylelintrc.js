/** @type {import('stylelint').Config} */
export default {
  extends: 'stylelint-config-standard',
  rules: {
    'selector-class-pattern': null
  },
  plugins: ['./packages/cmk-frontend-vue/scripts/stylelint-vue-bem-naming-convention.js'],
  overrides: [
    {
      files: ['*.css', '**/*.css'],
      rules: {
        'selector-class-pattern': [
          '^$',
          {
            message: 'Expected no selectors in css files, only variable definitions.'
          }
        ]
      }
    },
    {
      files: ['*.scss', '**/*.scss'],
      rules: {
        // css-tree@3.1.0 does not define <cursor-predefined>, crashing the rule.
        // The fix is tracked in @csstools/css-syntax-patches-for-csstree but
        // cursor-predefined is not yet included. Re-enable when it is.
        // See: stylelint/stylelint#8100, stylelint/stylelint#8850
        'declaration-property-value-no-unknown': null
      }
    },
    // https://github.com/ota-meshi/stylelint-config-standard-vue/blob/main/lib/index.js
    // https://github.com/ota-meshi/stylelint-config-standard-vue/blob/main/lib/vue-specific-rules.js
    {
      files: ['*.vue', '**/*.vue'],
      customSyntax: 'postcss-html',
      extends: ['stylelint-config-standard'],
      rules: {
        // Allow only valid native CSS nesting patterns:
        // & followed by: . : # [ space > + ~
        // This prevents SCSS concatenation like &--modifier, &__element
        'selector-nested-pattern': [
          '^(&(\\.|:|#|\\[|\\s|>|\\+|~)|[^&])',
          {
            message:
              'Expected "%s" to match CSS nesting pattern. Only native CSS nesting allowed. Use &:hover, & .child, &#id instead of SCSS patterns like &--modifier'
          }
        ],
        'keyframes-name-pattern': ['^([a-z][a-z0-9]*)((-|_|--|__)[a-z0-9]+)*$'],
        // https://github.com/ota-meshi/stylelint-config-recommended-vue/blob/main/lib/vue-specific-rules.js
        // css-tree@3.1.0 does not define <cursor-predefined>, crashing the rule.
        // Re-enable when @csstools/css-syntax-patches-for-csstree includes cursor-predefined.
        // See: stylelint/stylelint#8100, stylelint/stylelint#8850
        'declaration-property-value-no-unknown': null,
        'selector-pseudo-class-no-unknown': [true, { ignorePseudoClasses: ['slotted'] }],
        'value-keyword-case': [
          'lower',
          {
            ignoreFunctions: ['v-bind']
          }
        ],
        'checkmk/vue-bem-naming-convention': true,
        // renaming the error message to make it more clear what happens:
        'no-empty-source': [true, { message: 'No empty <style> section allowed in vue files.' }]
      }
    }
  ]
}
