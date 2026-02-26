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

import CmkList from '@/components/CmkList/CmkList.vue'

import DemoCmkListDev from './DemoCmkListDev.vue'

defineProps<{ screenshotMode: boolean }>()

const listData = ref({
  titles: ['Primary Server', 'Backup Database', 'Cache Node']
})

const tryDelete = (_index: number) => {
  return true
}

const tryAdd = () => {
  listData.value.titles.push(`New Node ${listData.value.titles.length + 1}`)
  return true
}

const a11yDataCmkList = [
  {
    keys: ['Tab'],
    description:
      'Moves keyboard focus to end of list. While the focus outline is hidden from view, its underlying functionality remains intact.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus in reverse order through the list elements.'
  },
  {
    keys: ['Enter', 'Space'],
    description: 'Deletes the focused item from the list.'
  }
]

const codeExampleCmkList = `<script setup lang="ts">
import { ref } from 'vue'
${'import'} CmkList from '@/components/CmkList/CmkList.vue'

const itemsData = ref({
  names: ['Alice', 'Bob', 'Charlie'],
  roles: ['Admin', 'Editor', 'Viewer']
})

const handleAdd = () => {
  itemsData.value.names.push('New User')
  itemsData.value.roles.push('Viewer')
  return true
}

const handleDelete = (index: number) => {
  return true
}
<${'/'}script>

<template>
  <CmkList
    :items-props="itemsData"
    orientation="vertical"
    :try-delete="handleDelete"
    :add="{ show: true, tryAdd: handleAdd, label: 'Add User' }"
  >
    <template #item-props="{ names, roles }">
      <div>
        <strong>{{ names }}</strong> - <span>{{ roles }}</span>
      </div>
    </template>
  </CmkList>
</template>`

type ListOrientation = 'vertical' | 'horizontal'

const panelConfig = {
  orientation: {
    type: 'list',
    title: 'Orientation',
    options: [
      { title: 'Vertical', name: 'vertical' },
      { title: 'Horizontal', name: 'horizontal' }
    ] satisfies Options<ListOrientation>[],
    initialState: 'vertical' as const
  },
  showAdd: {
    type: 'boolean',
    title: 'Show Add Button',
    initialState: true
  },
  enableDrag: {
    type: 'boolean',
    title: 'Enable Drag & Drop',
    initialState: false
  }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkList</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkList
        :items-props="listData"
        :orientation="propState.orientation"
        :try-delete="tryDelete"
        :add="{ show: propState.showAdd, tryAdd, label: 'Add Item' }"
        :drag-callbacks="propState.enableDrag ? { onReorder: () => {} } : null"
      >
        <template #item-props="{ index, titles }">
          {{ titles }} <small style="opacity: 0.6">(ID: {{ index }})</small>
        </template>
      </CmkList>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkList" />

    <DemoDetailPageAccessibility :data="a11yDataCmkList" />

    <DemoDetailPageDeveloperPlayground>
      <DemoCmkListDev :screenshot-mode="screenshotMode" />
    </DemoDetailPageDeveloperPlayground>
  </DemoDetailPageLayout>
</template>
