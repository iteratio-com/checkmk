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
  type Options,
  type PanelConfig,
  createPanelState
} from '@demo/_demo/components/detail-page'
import { ref } from 'vue'

import CmkMultitoneIcon from '@/components/CmkIcon/CmkMultitoneIcon.vue'
import type {
  CmkMultitoneIconColor,
  CmkMultitoneIconNames,
  IconSizeNames
} from '@/components/CmkIcon/types.ts'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkMultitoneIcon = `<script setup lang="ts">
${'import'} CmkMultitoneIcon from '@/components/CmkIcon/CmkMultitoneIcon.vue'
<${'/'}script>

<template>
  <CmkMultitoneIcon
    name="services"
    primary-color="success"
    secondary-color="warning"
    size="large"
    title="Service Status"
  />
</template>`

const toneOptions = [
  { name: 'success', title: 'Success (Green)' },
  { name: 'danger', title: 'Danger (Red)' },
  { name: 'warning', title: 'Warning (Yellow)' },
  { name: 'info', title: 'Info (Blue)' },
  { name: 'hosts', title: 'Hosts (Cyan)' },
  { name: 'services', title: 'Services (Orange)' },
  { name: 'specialAgents', title: 'Special Agents (Purple)' },
  { name: 'users', title: 'Users (Pink)' },
  { name: 'customization', title: 'Customization (Brown)' },
  { name: 'others', title: 'Others (Grey)' }
] satisfies Options<CmkMultitoneIconColor>[]

const panelConfig = {
  name: {
    type: 'list',
    title: 'Icon Name',
    options: [
      { title: 'Services', name: 'services' },
      { title: 'Monitoring', name: 'monitoring' },
      { title: 'Setup', name: 'setup' },
      { title: 'User', name: 'user' },
      { title: 'Success', name: 'success' },
      { title: 'Error', name: 'error' },
      { title: 'Warning', name: 'warning' },
      { title: 'Aggregation (two-color)', name: 'aggr' }
    ] satisfies Options<CmkMultitoneIconNames>[],
    initialState: 'services' as CmkMultitoneIconNames
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
    ] satisfies Options<IconSizeNames>[],
    initialState: 'xxlarge' as const
  },
  primaryColor: {
    type: 'list',
    title: 'Primary Color',
    options: toneOptions,
    initialState: 'success' as const
  },
  secondaryColor: {
    type: 'list',
    title: 'Secondary Color',
    options: toneOptions,
    initialState: 'warning' as const
  },
  rotate: {
    type: 'number',
    title: 'Rotation',
    initialState: 0,
    help: 'Enter a rotation value in degrees (e.g., 45, 90, 180) to rotate the icon.'
  },
  title: {
    type: 'string',
    title: 'Title Attribute',
    initialState: 'Demo Multitone Icon'
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkMultitoneIcon</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkMultitoneIcon
        :name="propState.name"
        :primary-color="propState.primaryColor"
        :secondary-color="propState.secondaryColor"
        :size="propState.size"
        :rotate="propState.rotate"
        :title="propState.title"
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkMultitoneIcon" />

    <DemoDetailPageAccessibility :data="[]" />
  </DemoDetailPageLayout>
</template>
