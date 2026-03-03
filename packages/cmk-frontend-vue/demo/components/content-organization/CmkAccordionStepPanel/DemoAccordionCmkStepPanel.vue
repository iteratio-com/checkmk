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
  DemoDetailPageLayout
} from '@demo/_demo/components/detail-page'
import { ref } from 'vue'

import CmkAccordionStepPanel from '@/components/CmkAccordionStepPanel/CmkAccordionStepPanel.vue'
import CmkAccordionStepPanelItem from '@/components/CmkAccordionStepPanel/CmkAccordionStepPanelItem.vue'
import CmkIndent from '@/components/CmkIndent.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkAccordionStepPanel = [
  {
    keys: ['Tab'],
    description: 'Moves keyboard focus to the step panel.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the step panel from the next focusable element in reverse order.'
  },
  {
    keys: ['Enter', 'Space'],
    description: 'Toggles the expansion state of the focused accordion item.'
  }
]

const codeExampleCmkAccordionStepPanel = `<script setup lang="ts">
import { ref } from 'vue'
${'import'} CmkAccordionStepPanel from '@/components/CmkAccordionStepPanel/CmkAccordionStepPanel.vue'
${'import'} CmkAccordionStepPanelItem from '@/components/CmkAccordionStepPanel/CmkAccordionStepPanelItem.vue'

const openSteps = ref(['step-2'])
<${'/'}script>

<template>
  <CmkAccordionStepPanel v-model="openSteps">

    <CmkAccordionStepPanelItem
      :step="1"
      title="Download Agent"
      info="2-3 min"
      :accomplished="true"
    >
      <p>Select your operating system and download the appropriate agent package.</p>
    </CmkAccordionStepPanelItem>

    <CmkAccordionStepPanelItem
      :step="2"
      title="Install Package"
      info="5 min"
      :accomplished="false"
    >
      <p>Run the installer on your target machine. Ensure you have root/admin privileges.</p>
    </CmkAccordionStepPanelItem>
  </CmkAccordionStepPanel>
</template>`

const openSteps = ref<string[]>(['step-2'])
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkAccordionStepPanel</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkAccordionStepPanel v-model="openSteps">
        <CmkAccordionStepPanelItem
          :step="1"
          title="Download Agent"
          info="2-3 min"
          :accomplished="true"
        >
          <CmkIndent>
            Select your operating system and download the appropriate agent package.
          </CmkIndent>
        </CmkAccordionStepPanelItem>

        <CmkAccordionStepPanelItem
          :step="2"
          title="Install Package"
          info="5 min"
          :accomplished="false"
        >
          <CmkIndent>
            Run the installer on your target machine. Ensure you have root/admin privileges.
          </CmkIndent>
        </CmkAccordionStepPanelItem>

        <CmkAccordionStepPanelItem
          :step="3"
          title="Verify Connection"
          info="&infin;"
          :accomplished="false"
        >
          <CmkIndent> Check the connection status in the monitoring dashboard. </CmkIndent>
        </CmkAccordionStepPanelItem>
      </CmkAccordionStepPanel>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkAccordionStepPanel" />

    <DemoDetailPageAccessibility :data="a11yDataCmkAccordionStepPanel" />
  </DemoDetailPageLayout>
</template>
