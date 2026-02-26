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

import CmkInlineValidation from '@/components/user-input/CmkInlineValidation.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkInlineValidation = `<script setup lang="ts">
import { ref } from 'vue'

${'import'} CmkInlineValidation from '@/components/user-input/CmkInlineValidation.vue'

const formErrors = ref<string[]>([
  'This is an inline validation error message.',
  'A secondary validation condition also failed.'
])
<${'/'}script>

<template>
  <CmkInlineValidation :validation="formErrors" />
</template>`

const panelConfig = {
  validation: {
    type: 'boolean',
    title: 'validation',
    initialState: true
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkInlineValidation</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkInlineValidation
        :validation="
          propState.validation
            ? [
                'This is an inline validation error message.',
                'A secondary validation condition also failed.'
              ]
            : undefined
        "
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkInlineValidation" />

    <DemoDetailPageAccessibility :data="[]" />
  </DemoDetailPageLayout>
</template>
