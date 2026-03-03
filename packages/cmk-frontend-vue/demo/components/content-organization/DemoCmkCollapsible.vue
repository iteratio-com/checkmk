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

import CmkCollapsible, { CmkCollapsibleTitle } from '@/components/CmkCollapsible'
import CmkIndent from '@/components/CmkIndent.vue'

import DemoCmkCollapsibleDev from './DemoCmkCollapsibleDev.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkCollapsible = [
  {
    keys: ['Tab'],
    description:
      'Moves keyboard focus to title. While the focus outline is hidden from view, its underlying functionality remains intact.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the title from the next focusable element in reverse order.'
  },
  {
    keys: ['Enter', 'Space'],
    description:
      'When the title button is focused, pressing Enter or Space opens the collapsible content.'
  }
]

const codeExampleCmkCollapsible = `<script setup lang="ts">
import { ref } from 'vue'
${'import'} CmkCollapsible, { CmkCollapsibleTitle } from '@/components/CmkCollapsible'
${'import'} CmkIndent from '@/components/CmkIndent.vue'

const isOpen = ref(false)
<${'/'}script>

<template>
  <CmkCollapsibleTitle
    title="Collapsible Section"
    side-title="Details"
    help_text="Click to expand"
    :open="isOpen"
    @toggle-open="isOpen = !isOpen"
  />

  <CmkCollapsible :open="isOpen">
    <CmkIndent>
      This content is hidden inside the collapsible wrapper. It animates height smoothly when toggled.
    </CmkIndent>
  </CmkCollapsible>
</template>`

const panelConfig = {
  open: { type: 'boolean', title: 'Open', initialState: false },
  title: { type: 'string', title: 'Title Text', initialState: 'Collapsible Section' },
  sideTitle: { type: 'string', title: 'Side Title', initialState: 'Details' },
  helpText: { type: 'string', title: 'Help Text', initialState: 'Click to expand' }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkCollapsible</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkCollapsibleTitle
        :title="propState.title"
        :side-title="propState.sideTitle"
        :help_text="propState.helpText"
        :open="propState.open"
        @toggle-open="propState.open = !propState.open"
      />

      <CmkCollapsible :open="propState.open">
        <CmkIndent>
          This content is hidden inside the collapsible wrapper. It animates height smoothly when
          toggled.
        </CmkIndent>
      </CmkCollapsible>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkCollapsible" />

    <DemoDetailPageAccessibility :data="a11yDataCmkCollapsible" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkCollapsibleDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
