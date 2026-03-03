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

import type { SimpleIcons } from '@/components/CmkIcon'
import CmkLinkCard from '@/components/CmkLinkCard'
import type { CmkLinkCardVariants } from '@/components/CmkLinkCard/CmkLinkCard.vue'

import DemoCmkLinkCardDev from './DemoCmkLinkCardDev.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkLinkCard = [
  {
    keys: ['Tab'],
    description:
      'Moves keyboard focus to the card. The card is focusable and acts as a standard hyperlink.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the card from the next focusable element in reverse order.'
  },
  {
    keys: ['Enter'],
    description: 'Activates the link card, following the URL or triggering the callback.'
  }
]

const codeExampleCmkLinkCard = `<script setup lang="ts">
${'import'} CmkLinkCard from '@/components/CmkLinkCard'
<${'/'}script>

<template>
  <CmkLinkCard
    title="Checkmk Documentation"
    subtitle="Learn how to configure and use Checkmk."
    icon-name="about-checkmk"
    url="https://docs.checkmk.com"
    variant="standard"
    :open-in-new-tab="true"
  />
</template>`

const panelConfig = {
  variant: {
    type: 'list',
    title: 'Variant',
    options: [
      { title: 'Standard', name: 'standard' },
      { title: 'Borderless', name: 'borderless' }
    ],
    initialState: 'standard'
  },
  title: { type: 'string', title: 'Title', initialState: 'Checkmk Community' },
  subtitle: {
    type: 'string',
    title: 'Subtitle',
    initialState: 'Join the discussion with other users.'
  },
  iconName: {
    type: 'list',
    title: 'Icon',
    options: [
      { title: 'None', name: 'none' },
      { title: 'Checkmk Logo', name: 'checkmk-logo-min' },
      { title: 'Help', name: 'main-help' },
      { title: 'Info', name: 'about-checkmk' }
    ],
    initialState: 'checkmk-logo-min'
  },
  openInNewTab: { type: 'boolean', title: 'Open in New Tab', initialState: true },
  disabled: { type: 'boolean', title: 'Disabled', initialState: false }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkLinkCard</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <div
        style="
          width: 100%;
          max-width: 500px;
          display: flex;
          flex-direction: column;
          gap: var(--dimension-4);
        "
      >
        <CmkLinkCard
          :title="propState.title"
          :subtitle="propState.subtitle"
          :icon-name="propState.iconName as SimpleIcons"
          :url="propState.disabled ? undefined : 'https://forum.checkmk.com'"
          :variant="propState.variant as CmkLinkCardVariants['variant']"
          :open-in-new-tab="propState.openInNewTab"
          :disabled="propState.disabled"
        />
      </div>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkLinkCard" />

    <DemoDetailPageAccessibility :data="a11yDataCmkLinkCard" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkLinkCardDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
