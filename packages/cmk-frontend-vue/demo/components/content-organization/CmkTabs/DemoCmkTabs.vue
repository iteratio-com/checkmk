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
  DemoDetailPageLayout
} from '@demo/_demo/components/detail-page'
import { ref } from 'vue'

import CmkIcon from '@/components/CmkIcon'
import CmkTabs, { CmkTab, CmkTabContent } from '@/components/CmkTabs'
import CmkHeading from '@/components/typography/CmkHeading.vue'
import CmkParagraph from '@/components/typography/CmkParagraph.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkTabs = [
  {
    keys: ['Tab'],
    description: 'Moves keyboard focus to the Tab.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the Tab from the next focusable element in reverse order.'
  },
  {
    keys: ['ArrowLeft', 'ArrowRight'],
    description: 'Move focus between tabs.'
  },
  {
    keys: ['Home', 'End'],
    description: 'Move to the first and last tabs respectively.'
  }
]

const codeExampleCmkTabs = `<script setup lang="ts">
import { ref } from 'vue'
${'import'} CmkTabs, { CmkTab, CmkTabContent } from '@/components/CmkTabs'
${'import'} CmkIcon from '@/components/CmkIcon'

const activeTab = ref('tab-1')
<${'/'}script>

<template>
  <CmkTabs v-model="activeTab">

    <template #tabs>
      <CmkTab id="tab-1">
        <CmkIcon name="search" /> Search
      </CmkTab>
      <CmkTab id="tab-2">
        <CmkIcon name="info-circle" /> Information
      </CmkTab>
      <CmkTab id="tab-3" :disabled="true">
        <CmkIcon name="close" /> Disabled
      </CmkTab>
    </template>

    <template #tab-contents>
      <CmkTabContent id="tab-1">
        <p>Use the search bar to find hosts and services.</p>
      </CmkTabContent>
      <CmkTabContent id="tab-2">
        <p>Detailed system information and status reports.</p>
      </CmkTabContent>
      <CmkTabContent id="tab-3">
        <p>This content is not accessible.</p>
      </CmkTabContent>
    </template>

  </CmkTabs>
</template>`

const activeTab = ref('tab-1')
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkTabs</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkTabs v-model="activeTab">
        <template #tabs>
          <CmkTab id="tab-1"><CmkIcon name="search" /> Search</CmkTab>
          <CmkTab id="tab-2"><CmkIcon name="info-circle" /> Information</CmkTab>
          <CmkTab id="tab-3" :disabled="true"><CmkIcon name="close" /> Disabled</CmkTab>
        </template>

        <template #tab-contents>
          <CmkTabContent id="tab-1">
            <CmkHeading type="h3">Search</CmkHeading>
            <CmkParagraph>Use the search bar to find hosts and services.</CmkParagraph>
          </CmkTabContent>
          <CmkTabContent id="tab-2">
            <CmkHeading type="h3">Information</CmkHeading>
            <CmkParagraph>Detailed system information and status reports.</CmkParagraph>
          </CmkTabContent>
          <CmkTabContent id="tab-3">
            <CmkHeading type="h3">Disabled</CmkHeading>
            <CmkParagraph>This content is not accessible.</CmkParagraph>
          </CmkTabContent>
        </template>
      </CmkTabs>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkTabs" />

    <DemoDetailPageAccessibility :data="a11yDataCmkTabs" />
  </DemoDetailPageLayout>
</template>
