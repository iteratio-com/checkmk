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

import CmkButton from '@/components/CmkButton.vue'
import type { SimpleIcons } from '@/components/CmkIcon'
import CmkPopupDialog from '@/components/CmkPopupDialog.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkPopupDialog = [
  {
    keys: ['Tab'],
    description:
      'Moves keyboard focus to the button or link element (if not disabled). While the focus outline is hidden from view, its underlying functionality remains intact.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the button from the next focusable element in reverse order.'
  },
  {
    keys: ['Enter', 'Space'],
    description: 'Opens the Popup Dialog when the trigger element is focused.'
  },
  {
    keys: ['Escape'],
    description: 'Closes the dialog.'
  }
]

const codeExampleCmkPopupDialog = `<script setup lang="ts">
import { ref } from 'vue'

${'import'} CmkButton from '@/components/CmkButton.vue'
${'import'} CmkPopupDialog from '@/components/CmkPopupDialog.vue'

const isOpen = ref(false)
<${'/'}script>

<template>
  <CmkButton @click="isOpen = true">
    Open Dialog
  </CmkButton>

  <CmkPopupDialog
    :open="isOpen"
    title="System Notification"
    text="This is a detailed message explaining the context of the dialog."
    icon="alert-crit"
    ok-button-text="OK Button Text"
    @close="isOpen = false"
  />
</template>`

const panelConfig = {
  open: { type: 'boolean', title: 'Open', initialState: false },
  title: { type: 'string', title: 'Title', initialState: 'System Notification' },
  text: {
    type: 'string',
    title: 'Text Content',
    initialState: 'This is a detailed message explaining the context of the dialog.'
  },
  icon: {
    type: 'list',
    title: 'Icon',
    options: [
      { title: 'None', name: 'none' },
      { title: 'Info Circle', name: 'info-circle' },
      { title: 'Alert Critical', name: 'alert-crit' },
      { title: 'Checkmark', name: 'check' }
    ] satisfies Options<SimpleIcons | 'none'>[],
    initialState: 'alert-crit' as SimpleIcons | 'none'
  },
  okButtonText: { type: 'string', title: 'OK Button Text', initialState: 'Close' },
  stayOpenOverlayClick: { type: 'boolean', title: 'Prevent Overlay Close', initialState: false }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkPopupDialog</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkButton @click="propState.open = true"> Open Dialog </CmkButton>

      <CmkPopupDialog
        :open="propState.open"
        :title="propState.title"
        :text="propState.text"
        :icon="propState.icon === 'none' ? undefined : (propState.icon as SimpleIcons)"
        :ok-button-text="propState.okButtonText || undefined"
        :stay-open-overlay-click="propState.stayOpenOverlayClick"
        @close="propState.open = false"
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkPopupDialog" />

    <DemoDetailPageAccessibility :data="a11yDataCmkPopupDialog" />
  </DemoDetailPageLayout>
</template>
