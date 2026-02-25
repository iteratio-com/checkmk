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
  DemoDetailPageDeveloperPlayground,
  DemoDetailPageHeader,
  DemoDetailPageLayout,
  DemoPropertiesPanel,
  type PanelConfig,
  createPanelState
} from '@demo/_demo/components/detail-page'
import { ref } from 'vue'

import CmkCode from '@/components/CmkCode.vue'

import DemoCmkCodeDev from './DemoCmkCodeDev.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkCode = [
  {
    keys: ['Tab'],
    description:
      'Moves focus sequentially to the scrollable code container, the "Show more/less" toggle button (if visible), and the Copy button. While the focus outline is hidden from view, its underlying functionality remains intact.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus in reverse through the focusable elements.'
  },
  {
    keys: ['Enter', 'Space'],
    description:
      'Activates the "Show more/less" toggle or triggers the code copy action when the respective button is focused.'
  }
]

const codeExampleCmkCode = `<script setup lang="ts">
${'import'} CmkCode from '@/components/CmkCode.vue'

const mySnippet = \`const greet = () => {
  console.log("Hello Checkmk!");
};
greet();\`
<${'/'}script>

<template>
  <CmkCode
    title="Greeting Function"
    :code_txt="mySnippet"
  />
</template>`

const panelConfig = {
  title: {
    type: 'string',
    title: 'Title',
    initialState: 'Example Code Snippet'
  },
  code_txt: {
    type: 'string',
    title: 'Code Text',
    initialState: codeExampleCmkCode
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkCode</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkCode :title="propState.title" :code_txt="propState.code_txt" />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkCode" />

    <DemoDetailPageAccessibility :data="a11yDataCmkCode" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkCodeDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
