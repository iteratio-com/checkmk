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

import CmkAlertBox, { type Sizes, type Variants } from '@/components/CmkAlertBox.vue'

import DemoCmkAlertBoxDev from './DemoCmkAlertBoxDev.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkAlertBox = `<script setup lang="ts">
import { ref } from 'vue'

${'import'} CmkAlertBox from '@/components/CmkAlertBox.vue'

const isAlertOpen = ref(true)
<${'/'}script>

<template>
  <CmkAlertBox
    v-model:open="isAlertOpen"
    variant="info"
    size="medium"
    heading="Alert Heading"
  >
    This is an important alert message that requires your attention.
  </CmkAlertBox>
</template>`

const panelConfig = {
  open: { type: 'boolean', title: 'Open', initialState: true },
  variant: {
    type: 'list',
    title: 'Variant',
    options: [
      { title: 'Info', name: 'info' },
      { title: 'Success', name: 'success' },
      { title: 'Warning', name: 'warning' },
      { title: 'Error', name: 'error' },
      { title: 'Loading', name: 'loading' }
    ] satisfies Options<NonNullable<Variants>>[],
    initialState: 'info' as const
  },
  size: {
    type: 'list',
    title: 'Size',
    options: [
      { title: 'Medium', name: 'medium' },
      { title: 'Small', name: 'small' }
    ] satisfies Options<NonNullable<Sizes>>[],
    initialState: 'medium' as const
  },
  heading: { type: 'string', title: 'Heading', initialState: 'Alert Heading' },
  dismissable: { type: 'boolean', title: 'Dismissable', initialState: false },
  autoDismiss: { type: 'boolean', title: 'Auto Dismiss (6s)', initialState: false }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkAlertBox</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkAlertBox
        v-model:open="propState.open"
        :variant="propState.variant"
        :size="propState.size"
        :heading="propState.heading"
        :auto-dismiss="propState.autoDismiss"
        :dismissible="propState.dismissable"
      >
        This is a demonstration of the alert box content. You can put any long text or HTML elements
        in here to showcase wrapping and layout.
      </CmkAlertBox>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkAlertBox" />

    <DemoDetailPageAccessibility :data="[]" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkAlertBoxDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
