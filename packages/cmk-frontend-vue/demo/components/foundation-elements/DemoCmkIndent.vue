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

import CmkIndent from '@/components/CmkIndent.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkIndent = `<script setup lang="ts">
${'import'} CmkIndent from '@/components/CmkIndent.vue'
<${'/'}script>

<template>
  <p>Top Level Content</p>
  <CmkIndent>
    <p>First Level Indentation</p>
    <CmkIndent error>
      <p>Second Level Indentation</p>
    </CmkIndent>
  </CmkIndent>
</template>`

const panelConfig = {
  indent: { type: 'boolean', title: 'Enable Indent', initialState: true },
  error: { type: 'boolean', title: 'Error State', initialState: false }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkIndent</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <p>Top Level Content</p>

      <CmkIndent :indent="propState.indent" :error="propState.error">
        <p>First Level Indentation</p>

        <CmkIndent :indent="propState.indent" :error="propState.error">
          <p>Second Level Indentation</p>
        </CmkIndent>
      </CmkIndent>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkIndent" />

    <DemoDetailPageAccessibility :data="[]" />
  </DemoDetailPageLayout>
</template>
