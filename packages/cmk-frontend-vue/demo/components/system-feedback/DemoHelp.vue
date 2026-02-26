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
  type PanelConfig,
  createPanelState
} from '@demo/_demo/components/detail-page'
import { ref } from 'vue'

import CmkHelpText from '@/components/CmkHelpText.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkHelpText = [
  {
    keys: ['Tab'],
    description:
      'Moves keyboard focus to the button or link element (if not disabled). While the focus outline is hidden from view, its underlying functionality remains intact.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the button from the next focusable element in reverse order.'
  },
  {
    keys: ['Enter', 'Space'],
    description: 'Opens the help text.'
  },
  {
    keys: ['Escape'],
    description: 'Closes the tooltip if it is currently open.'
  }
]

const codeExampleCmkHelpText = `<script setup lang="ts">
${'import'} CmkHelpText from '@/components/CmkHelpText.vue'
<${'/'}script>

<template>
    <CmkHelpText help="Enter the fully qualified domain name (FQDN) of the server." />
</template>`

const panelConfig = {
  help: {
    type: 'string',
    title: 'Help',
    initialState: 'This is a short, precise contextual help text.'
  },
  ariaLabel: {
    type: 'string',
    title: 'Custom Aria Label',
    initialState: 'Help regarding this setting'
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkHelpText</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <span> Example Configuration Field </span>
      <CmkHelpText :help="propState.help" :aria-label="propState.ariaLabel" />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkHelpText" />

    <DemoDetailPageAccessibility :data="a11yDataCmkHelpText" />
  </DemoDetailPageLayout>
</template>
