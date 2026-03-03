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

import CmkCatalogPanel from '@/components/CmkCatalogPanel.vue'

import DemoCmkCatalogPanelDev from './DemoCmkCatalogPanelDev.vue'

type CatalogPanelVariant = 'default' | 'padded'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkCatalogPanel = [
  {
    keys: ['Tab'],
    description:
      'Moves keyboard focus to header. While the focus outline is hidden from view, its underlying functionality remains intact.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the header from the next focusable element in reverse order.'
  },
  {
    keys: ['Enter', 'Space'],
    description:
      'When the header button is focused, pressing Enter or Space toggles the visibility of the panel content.'
  }
]

const codeExampleCmkCatalogPanel = `<script setup lang="ts">
${'import'} CmkCatalogPanel from '@/components/CmkCatalogPanel.vue'
<${'/'}script>

<template>
  <CmkCatalogPanel title="Catalog Panel" variant="default" :open="true">
    This is the collapsible content inside the panel.
  </CmkCatalogPanel>
</template>`

const panelConfig = {
  title: { type: 'string', title: 'Panel Title', initialState: 'Catalog Panel' },
  variant: {
    type: 'list',
    title: 'Variant',
    options: [
      { title: 'Default', name: 'default' },
      { title: 'Padded', name: 'padded' }
    ] satisfies Options<CatalogPanelVariant>[],
    initialState: 'default' as const
  },
  open: { type: 'boolean', title: 'Open', initialState: true }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkCatalogPanel</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkCatalogPanel
        :key="String(propState.open)"
        :title="propState.title"
        :variant="propState.variant ?? 'default'"
        :open="propState.open"
      >
        This is the collapsible content inside the panel.
      </CmkCatalogPanel>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkCatalogPanel" />

    <DemoDetailPageAccessibility :data="a11yDataCmkCatalogPanel" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkCatalogPanelDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
