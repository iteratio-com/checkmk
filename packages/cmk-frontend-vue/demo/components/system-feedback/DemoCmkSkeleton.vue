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

import CmkSkeleton, { type SkeletonType } from '@/components/CmkSkeleton.vue'

import DemoCmkSkeletonDev from './DemoCmkSkeletonDev.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkSkeleton = `<script setup lang="ts">
${'import'} CmkSkeleton from '@/components/CmkSkeleton.vue'
<${'/'}script>

<template>
  <div class="user-card-loading">
    <CmkSkeleton type="icon-xlarge" />
    <div class="user-card-text">
      <CmkSkeleton type="h3" width="60%" />
      <CmkSkeleton type="info-text" width="40%" />
    </div>
  </div>
</template>`

const panelConfig = {
  type: {
    type: 'list',
    title: 'Skeleton Type',
    options: [
      { title: 'Box', name: 'box' },
      { title: 'H1', name: 'h1' },
      { title: 'H2', name: 'h2' },
      { title: 'H3', name: 'h3' },
      { title: 'Text', name: 'text' },
      { title: 'Info Text', name: 'info-text' },
      { title: 'Icon: X-Small', name: 'icon-xsmall' },
      { title: 'Icon: Small', name: 'icon-small' },
      { title: 'Icon: Medium', name: 'icon-medium' },
      { title: 'Icon: Large', name: 'icon-large' },
      { title: 'Icon: X-Large', name: 'icon-xlarge' },
      { title: 'Icon: XX-Large', name: 'icon-xxlarge' },
      { title: 'Icon: XXX-Large', name: 'icon-xxxlarge' }
    ] satisfies Options<NonNullable<SkeletonType>>[],
    initialState: 'text' as const
  },
  width: {
    type: 'string',
    title: 'Custom Width',
    help: 'Optionally set a custom width for the skeleton using any valid CSS unit(% or px).',
    initialState: '100%'
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkSkeleton</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkSkeleton :type="propState.type" :width="propState.width" />
      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkSkeleton" />

    <DemoDetailPageAccessibility :data="[]" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkSkeletonDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
