<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import {
  DemoDetailPageAccessibility,
  DemoDetailPageCodeExample,
  DemoDetailPageComponent,
  DemoDetailPageHeader,
  DemoDetailPageLayout,
  DemoPropertiesPanel,
  type Options,
  type PanelConfig,
  createPanelState
} from '@demo/_demo/components/detail-page'
import { ref } from 'vue'

import CmkInput from '@/components/user-input/CmkInput.vue'
import type { inputSizes } from '@/components/user-input/sizes'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkInput = [
  {
    keys: ['Tab'],
    description: 'Moves keyboard focus to the input field.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the input field from the next focusable element in reverse order.'
  },
  {
    keys: ['ArrowLeft', 'ArrowRight'],
    description: 'Moves the cursor one character to the left or right within the input content.'
  },
  {
    keys: ['End'],
    description: 'Moves the cursor to the end of the input content.'
  }
]

const codeExampleCmkInput = `<script setup lang="ts">
import { ref } from 'vue'
${'import'} CmkInput from '@/components/user-input/CmkInput.vue'

const username = ref('')
<${'/'}script>

<template>
  <CmkInput
    v-model="username"
    type="text"
    field-size="MEDIUM"
  />
</template>`

type InputType = 'text' | 'number' | 'date' | 'time' | 'password'

const panelConfig = {
  modelValue: {
    type: 'string',
    title: 'Value',
    initialState: 'Checkmk Admin'
  },
  type: {
    type: 'list',
    title: 'Type',
    options: [
      { title: 'Text', name: 'text' },
      { title: 'Number', name: 'number' },
      { title: 'Password', name: 'password' },
      { title: 'Date', name: 'date' },
      { title: 'Time', name: 'time' }
    ] satisfies Options<InputType>[],
    initialState: 'text' as InputType
  },
  fieldSize: {
    type: 'list',
    title: 'Size',
    help: 'This Only affects text inputs and controls the width of the input field.',
    options: [
      { title: 'SMALL', name: 'SMALL' },
      { title: 'MEDIUM', name: 'MEDIUM' },
      { title: 'LARGE', name: 'LARGE' },
      { title: 'FILL', name: 'FILL' }
    ] satisfies Options<keyof typeof inputSizes>[],
    initialState: 'SMALL' as const
  },
  unit: {
    type: 'string',
    title: 'Unit',
    initialState: ''
  },
  inline: {
    type: 'boolean',
    title: 'Inline',
    initialState: false
  },
  externalErrors: {
    type: 'string',
    title: 'External Error',
    initialState: ''
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkInput</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkInput
        v-model="propState.modelValue"
        :type="propState.type"
        :field-size="propState.fieldSize"
        :unit="propState.unit"
        :inline="propState.inline"
        :external-errors="propState.externalErrors ? [propState.externalErrors] : []"
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkInput" />

    <DemoDetailPageAccessibility :data="a11yDataCmkInput" />
  </DemoDetailPageLayout>
</template>
