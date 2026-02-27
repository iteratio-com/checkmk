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

import CmkHtml from '@/components/CmkHtml.vue'

import DemoCmkHtmlDev from './DemoCmkHtmlDev.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkHtml: never[] = []

const codeExampleCmkHtml = `<script setup lang="ts">
import CmkHtml from '@/components/CmkHtml.vue'
<${'/'}script>

<template>
  <CmkHtml html="<h1>Heading</h1> <b>bold</b> and <a href='https://checkmk.com'>link</a>" />
</template>`

const panelConfig = {
  html: {
    type: 'string',
    title: 'html',
    initialState: "<h1>Heading</h1> <b>bold</b> and <a href='https://checkmk.com'>link</a>"
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkHtml</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkHtml :html="propState.html" />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkHtml" />

    <DemoDetailPageAccessibility :data="a11yDataCmkHtml" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkHtmlDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
