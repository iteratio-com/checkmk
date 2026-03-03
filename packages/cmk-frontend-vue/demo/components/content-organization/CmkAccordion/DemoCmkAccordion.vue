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

import CmkAccordion from '@/components/CmkAccordion/CmkAccordion.vue'
import CmkAccordionItem from '@/components/CmkAccordion/CmkAccordionItem.vue'
import CmkAccordionItemStateIndicator from '@/components/CmkAccordion/CmkAccordionItemStateIndicator.vue'
import CmkIcon from '@/components/CmkIcon'
import type { HeadingType } from '@/components/typography/CmkHeading.vue'

import DemoCmkAccordionDev from './DemoCmkAccordionDev.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkAccordion = [
  {
    keys: ['Tab'],
    description: 'Moves keyboard focus to the accordion header.'
  },
  {
    keys: [['Shift', 'Tab']],
    description:
      'Moves focus to the accordion header from the next focusable element in reverse order.'
  },
  {
    keys: ['Enter', 'Space'],
    description: 'Toggles the expansion state of the focused accordion item.'
  }
]

const codeExampleCmkAccordion = `<script setup lang="ts">
import { ref } from 'vue'
${'import'} CmkAccordion from '@/components/CmkAccordion/CmkAccordion.vue'
${'import'} CmkAccordionItem from '@/components/CmkAccordion/CmkAccordionItem.vue'
${'import'} CmkAccordionItemStateIndicator from '@/components/CmkAccordion/CmkAccordionItemStateIndicator.vue'
${'import'} CmkIcon from '@/components/CmkIcon'

const openedItems = ref(['item-1'])
<${'/'}script>

<template>
  <CmkAccordion v-model="openedItems" :min-open="1" :max-open="1">

    <CmkAccordionItem value="item-1">
      <template #header>
        <div style="display: flex; align-items: center; gap: 8px;">
          <CmkIcon name="users" />
          <span>Personal Information</span>
          <CmkAccordionItemStateIndicator value="item-1" />
        </div>
      </template>
      <template #content>
        <p>Manage your personal details, email address, and profile settings.</p>
      </template>
    </CmkAccordionItem>

    <CmkAccordionItem value="item-2">
      <template #header>
        <div style="display: flex; align-items: center; gap: 8px;">
          <CmkIcon name="passwords" />
          <span>Security Settings</span>
        </div>
      </template>
      <template #content>
        <p>Update your password, enable 2FA, and manage security keys.</p>
      </template>
    </CmkAccordionItem>

    <CmkAccordionItem value="item-3">
      <template #header>
        <div style="display: flex; align-items: center; gap: 8px;">
          <CmkIcon name="notifications" />
          <span>Notifications</span>
        </div>
      </template>
      <template #content>
        <p>Configure email digests and real-time alert preferences.</p>
      </template>
    </CmkAccordionItem>

  </CmkAccordion>
</template>`

const panelConfig = {
  minOpen: {
    type: 'number',
    title: 'minOpen',
    help: '0 allows all items to be collapsed, while 1 or more ensures that at least that many items are always expanded.',
    initialState: 1
  },
  maxOpen: {
    type: 'number',
    title: 'maxOpen',
    help: '0 allows unlimited items to be expanded, while 1 restricts to only one item at a time.',
    initialState: 1
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
const openedItems = ref(['item-1'])

const itemPanelConfig = {
  headerAs: {
    type: 'list',
    title: 'headerAs',
    options: [
      { title: 'h1', name: 'h1' },
      { title: 'h2', name: 'h2' },
      { title: 'h3', name: 'h3' },
      { title: 'h4', name: 'h4' }
    ] satisfies Options<NonNullable<HeadingType>>[],
    initialState: 'h3' as NonNullable<HeadingType>,
    help: 'HTML element used to render the accordion item header.'
  },
  disabled: {
    type: 'boolean',
    title: 'disabled',
    initialState: false,
    help: 'Disables all items in the accordion.'
  }
} satisfies PanelConfig

const itemPropState = ref(createPanelState(itemPanelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkAccordion</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkAccordion
        v-model="openedItems"
        :min-open="propState.minOpen"
        :max-open="propState.maxOpen"
      >
        <CmkAccordionItem
          value="item-1"
          :header-as="itemPropState.headerAs"
          :disabled="itemPropState.disabled"
        >
          <template #header>
            <div style="display: flex; align-items: center; gap: 8px">
              <CmkIcon name="users" />
              <span>Personal Information</span>
              <CmkAccordionItemStateIndicator value="item-1" />
            </div>
          </template>
          <template #content>
            <p>Manage your personal details, email address, and profile settings.</p>
          </template>
        </CmkAccordionItem>

        <CmkAccordionItem
          value="item-2"
          :header-as="itemPropState.headerAs"
          :disabled="itemPropState.disabled"
        >
          <template #header>
            <div style="display: flex; align-items: center; gap: 8px">
              <CmkIcon name="passwords" />
              <span>Security Settings</span>
            </div>
          </template>
          <template #content>
            <p>Update your password, enable 2FA, and manage security keys.</p>
          </template>
        </CmkAccordionItem>

        <CmkAccordionItem
          value="item-3"
          :header-as="itemPropState.headerAs"
          :disabled="itemPropState.disabled"
        >
          <template #header>
            <div style="display: flex; align-items: center; gap: 8px">
              <CmkIcon name="notifications" />
              <span>Notifications</span>
            </div>
          </template>
          <template #content>
            <p>Configure email digests and real-time alert preferences.</p>
          </template>
        </CmkAccordionItem>
      </CmkAccordion>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
        <DemoPropertiesPanel v-model="itemPropState" :config="itemPanelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkAccordion" />

    <DemoDetailPageAccessibility :data="a11yDataCmkAccordion" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkAccordionDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
