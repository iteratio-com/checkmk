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
  type Options,
  type PanelConfig,
  createPanelState
} from '@demo/_demo/components/detail-page'
import { ref } from 'vue'

import CmkKeyboardKey, {
  type CmkKeyboardKeyProps,
  type Sizes
} from '@/components/CmkKeyboardKey.vue'

import DemoCmkKeyboardKeyDev from './DemoCmkKeyboardKeyDev.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkKeyboardKey = `<script setup lang="ts">
${'import'} CmkKeyboardKey from '@/components/CmkKeyboardKey.vue'
<${'/'}script>

<template>
  <CmkKeyboardKey keyboard-key="enter" size="large" />
</template>`

const panelConfig = {
  keyboardKey: {
    type: 'list',
    title: 'Key Content',
    options: [
      { title: 'Arrow Left', name: 'arrow-left' },
      { title: 'Arrow Right', name: 'arrow-right' },
      { title: 'Arrow Up', name: 'arrow-up' },
      { title: 'Arrow Down', name: 'arrow-down' },
      { title: 'Enter', name: 'enter' },
      { title: 'Backspace', name: 'backspace' },
      { title: 'Ctrl', name: 'Ctrl' },
      { title: 'Shift', name: 'Shift' },
      { title: 'A', name: 'A' }
    ] satisfies Options<CmkKeyboardKeyProps['keyboardKey']>[],
    help: 'Custom keys can be added by passing any string value. For example, passing "Ctrl,Shift,A" will render a key with the text inside.',
    initialState: 'enter' as const
  },
  size: {
    type: 'list',
    title: 'Size',
    options: [
      { title: 'Small', name: 'small' },
      { title: 'Medium', name: 'medium' },
      { title: 'Large', name: 'large' }
    ] satisfies Options<Sizes>[],
    initialState: 'medium' as const
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkKeyboardKey</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkKeyboardKey :keyboard-key="propState.keyboardKey" :size="propState.size" />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkKeyboardKey" />

    <DemoDetailPageAccessibility :data="[]" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkKeyboardKeyDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
