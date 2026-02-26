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

import CmkDualList from '@/components/CmkDualList/CmkDualList.vue'
import {
  type DualListElement,
  type SearchableListWidthVariants
} from '@/components/CmkDualList/index.ts'

defineProps<{ screenshotMode: boolean }>()

const selectedData = ref<DualListElement[]>([{ name: 'host_admin', title: 'Host Administrator' }])
const a11yDataCmkDualList = [
  {
    keys: ['Tab'],
    description:
      'Moves keyboard focus sequentially between the searchable lists and the action buttons.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus in reverse order between the searchable lists and the action buttons.'
  },
  {
    keys: ['Enter', 'Space'],
    description:
      'Triggers the selected action button (e.g., adding or removing items between lists).'
  }
]

const codeExampleCmkDualList = `<script setup lang="ts">
import { ref } from 'vue'
${'import'} CmkDualList from '@/components/CmkDualList/CmkDualList.vue'
${'import'} { type DualListElement } from '@/components/CmkDualList/index.ts'

const availableRoles = ref<DualListElement[]>([
  { name: 'admin', title: 'Admin' },
  { name: 'editor', title: 'Editor' },
  { name: 'viewer', title: 'Viewer' }
])


const selectedRoles = ref<DualListElement[]>([availableRoles.value[2]!])
<${'/'}script>

<template>
  <CmkDualList
    v-model:data="selectedRoles"
    :elements="availableRoles"
    title="Assign User Roles"
    :validators="[]"
    :backendValidation="[]"
    width="medium"
  />
</template>`

const panelConfig = {
  title: {
    type: 'string',
    title: 'Group Title',
    initialState: 'Assign User Roles'
  },
  width: {
    type: 'list',
    title: 'Width',
    options: [
      { title: 'XSmall', name: 'xsmall' },
      { title: 'Small', name: 'small' },
      { title: 'Medium', name: 'medium' },
      { title: 'Large', name: 'large' }
    ] satisfies Options<SearchableListWidthVariants>[],
    initialState: 'medium' as const
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkDualList</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkDualList
        v-model:data="selectedData"
        :elements="[
          { name: 'host_admin', title: 'Host Administrator' },
          { name: 'network_admin', title: 'Network Administrator' },
          { name: 'db_admin', title: 'Database Administrator' },
          { name: 'security_auditor', title: 'Security Auditor' },
          { name: 'guest', title: 'Guest User' }
        ]"
        :title="propState.title"
        :validators="[]"
        :backend-validation="[]"
        :width="propState.width"
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkDualList" />

    <DemoDetailPageAccessibility :data="a11yDataCmkDualList" />
  </DemoDetailPageLayout>
</template>
