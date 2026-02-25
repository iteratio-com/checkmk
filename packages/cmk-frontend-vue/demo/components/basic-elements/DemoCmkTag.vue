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

import CmkTag, { type Colors, type Sizes, type Variants } from '@/components/CmkTag.vue'

import DemoCmkTagDev from './DemoCmkTagDev.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkTag = `<script setup lang="ts">
${'import'} CmkTag from '@/components/CmkTag.vue'
<${'/'}script>

<template>
  <CmkTag
    content="Critical Issue"
    color="default"
    variant="outline"
    size="medium"
  />
</template>`

const panelConfig = {
  content: {
    type: 'string',
    title: 'Content',
    initialState: 'Status Tag'
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
  },
  color: {
    type: 'list',
    title: 'Color',
    options: [
      { title: 'Default', name: 'default' },
      { title: 'Success', name: 'success' },
      { title: 'Warning', name: 'warning' },
      { title: 'Danger', name: 'danger' }
    ] satisfies Options<Colors>[],
    initialState: 'default' as const
  },
  variant: {
    type: 'list',
    title: 'Variant',
    options: [
      { title: 'Outline', name: 'outline' },
      { title: 'Fill', name: 'fill' }
    ] satisfies Options<Variants>[],
    initialState: 'outline' as const
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkTag</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkTag
        :content="propState.content"
        :size="propState.size"
        :color="propState.color"
        :variant="propState.variant"
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkTag" />

    <DemoDetailPageAccessibility :data="[]" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkTagDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
