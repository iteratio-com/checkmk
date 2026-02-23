<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import AccessibilityTable from '@demo/_demo/components/DemoAccessibilityTable.vue'
import PropertiesPanel from '@demo/_demo/components/DemoPropertiesPanel.vue'
import { type PanelConfig, createPanelState } from '@demo/_demo/types/prop-panel.ts'
import { computed, ref } from 'vue'

import CmkCode from '@/components/CmkCode.vue'
import CmkDropdown from '@/components/CmkDropdown'
import type { ButtonVariants } from '@/components/CmkDropdown/CmkDropdownButton.vue'
import type { Suggestions } from '@/components/CmkSuggestions'
import CmkHeading from '@/components/typography/CmkHeading.vue'

defineProps<{ screenshotMode: boolean }>()
const selectedValue = ref<string | null>(null)

const a11yDataCmkDropdown = [
  {
    key: 'Enter',
    description: 'Selects the currently highlighted suggestion and triggers the update.'
  },
  {
    key: 'Tab',
    description:
      'Selects the currently highlighted suggestion (functions identically to the Enter key in this component).'
  },
  {
    key: 'Escape',
    description:
      'Closes the suggestions dropdown or removes focus from the filter input without making a selection.'
  },
  {
    key: 'ArrowDown',
    description:
      'Moves the active highlight to the next selectable suggestion in the list, scrolling it into view if necessary.'
  },
  {
    key: 'ArrowUp',
    description:
      'Moves the active highlight to the previous selectable suggestion in the list, scrolling it into view if necessary.'
  }
]

const codeExampleCmkDropdown = `<script setup lang="ts">
import { ref } from 'vue'

import CmkDropdown from '@/components/CmkDropdown'
import type { Suggestions } from '@/components/CmkSuggestions'

const selected = ref<string | null>(null)
const options: Suggestions = {
  type: 'fixed',
  suggestions: [
    { name: '1', title: 'one' },
    { name: '2', title: 'two' }
  ]
}
<${'/'}script>

<template>
  <CmkDropdown
    v-model:selected-option="selected"
    :options="options"
    input-hint="some input hint"
    no-results-hint="no results hint"
    label="some label"
    required
  />
</template>`

const panelConfig = {
  optionsType: {
    type: 'list',
    title: 'Options Type',
    options: [
      { title: 'Fixed', name: 'fixed' },
      { title: 'Filtered', name: 'filtered' },
      { title: 'Callback Filtered', name: null }
    ],
    initialState: 'fixed'
  },
  width: {
    type: 'list',
    title: 'Width',
    options: [
      { title: 'Default', name: 'default' },
      { title: 'Wide', name: 'wide' },
      { title: 'Fill', name: 'fill' }
    ],
    initialState: 'wide'
  },
  disabled: { type: 'boolean', title: 'Disabled', initialState: false },
  required: { type: 'boolean', title: 'Required', initialState: false },
  formValidation: { type: 'boolean', title: 'Form Validation Error', initialState: false },
  inputHint: { type: 'string', title: 'Input Hint', initialState: 'Please select an option...' },
  noResultsHint: { type: 'string', title: 'No Results Hint', initialState: 'No matches found' }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))

const dynamicOptions = computed<Suggestions>(() => {
  const baseSuggestions = [
    { name: '1', title: 'Option One' },
    { name: '2', title: 'Option Two' },
    { name: '3', title: 'Option Three' }
  ]

  return propState.value.optionsType === 'filtered'
    ? { type: 'filtered', suggestions: baseSuggestions }
    : { type: 'fixed', suggestions: baseSuggestions }
})
</script>

<template>
  <h1>CmkDropDown</h1>

  <CmkDropdown
    v-model:selected-option="selectedValue"
    :options="dynamicOptions"
    :input-hint="propState.inputHint"
    :no-results-hint="propState.noResultsHint"
    :width="propState.width as ButtonVariants['width']"
    :disabled="propState.disabled"
    :required="propState.required"
    label="demo dropdown"
    :form-validation="propState.formValidation"
  />

  <PropertiesPanel v-model="propState" :config="panelConfig" />
  <CmkHeading level="2">Code Example</CmkHeading>
  <CmkCode :code_txt="codeExampleCmkDropdown" width="fill"> </CmkCode>
  <AccessibilityTable :data="a11yDataCmkDropdown" />
</template>
