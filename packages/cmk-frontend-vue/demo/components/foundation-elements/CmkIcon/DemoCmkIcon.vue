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

import type { CmkIconVariants, IconSizeNames, SimpleIcons } from '@/components/CmkIcon'
import CmkIcon from '@/components/CmkIcon'

import DemoCmkIconDev from './DemoCmkIconDev.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkIcon = `<script setup lang="ts">
${'import'} CmkIcon from '@/components/CmkIcon'
<${'/'}script>

<template>
  <CmkIcon
    name="main-help"
    size="large"
    variant="inline"
    title="Get Help"
  />
</template>`

const panelConfig = {
  name: { type: 'string', title: 'Icon Name', initialState: 'main-help' },
  variant: {
    type: 'list',
    title: 'Variant',
    options: [
      { title: 'Plain', name: 'plain' },
      { title: 'Inline (with margin)', name: 'inline' }
    ],
    initialState: 'plain'
  },
  size: {
    type: 'list',
    title: 'Size',
    options: [
      { title: 'XX-Small', name: 'xxsmall' },
      { title: 'X-Small', name: 'xsmall' },
      { title: 'Small', name: 'small' },
      { title: 'Medium', name: 'medium' },
      { title: 'Large', name: 'large' },
      { title: 'X-Large', name: 'xlarge' },
      { title: 'XX-Large', name: 'xxlarge' },
      { title: 'XXX-Large', name: 'xxxlarge' }
    ],
    initialState: 'xxlarge'
  },
  colored: { type: 'boolean', title: 'Colored', initialState: false },
  title: { type: 'string', title: 'Title (Tooltip/Alt)', initialState: 'Help Icon' },
  rotate: { type: 'number', title: 'Rotation (Degrees)', initialState: 0 }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkIcon</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkIcon
        :name="propState.name as SimpleIcons"
        :variant="propState.variant as CmkIconVariants['variant']"
        :size="propState.size as IconSizeNames"
        :colored="propState.colored"
        :title="propState.title"
        :rotate="propState.rotate"
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkIcon" />

    <DemoDetailPageAccessibility :data="[]" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkIconDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
