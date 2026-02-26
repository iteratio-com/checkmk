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

import CmkLoading from '@/components/CmkLoading.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkLoading = `<script setup lang="ts">
${'import'} CmkLoading from '@/components/CmkLoading.vue'
<${'/'}script>

<template>
  <CmkLoading height="8px" />
</template>`

const panelConfig = {
  height: {
    type: 'string',
    title: 'Dot Height',
    help: 'Adjust the height of the loading dots using any valid CSS unit (e.g., px, em, rem). 8px is default and recommended for most use cases.',
    initialState: '8px'
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkLoading</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <div
        style="
          min-height: 80px;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 100%;
        "
      >
        <CmkLoading :height="propState.height" />
      </div>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkLoading" />

    <DemoDetailPageAccessibility :data="[]" />
  </DemoDetailPageLayout>
</template>
