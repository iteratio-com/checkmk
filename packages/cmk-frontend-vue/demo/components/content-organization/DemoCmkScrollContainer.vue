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

import CmkScrollContainer, {
  type ScrollContainerVariants
} from '@/components/CmkScrollContainer.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataCmkScrollContainer = [
  {
    keys: ['Tab'],
    description: 'Moves keyboard focus to container.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the container from the next focusable element in reverse order.'
  },
  {
    keys: ['ArrowUp', 'ArrowDown'],
    description:
      'If the container has overflow and is scrollable, users can scroll using the Arrow Up/Down keys when the container or an element inside it has focus.'
  }
]

const codeExampleCmkScrollContainer = `<script setup lang="ts">
${'import'} CmkScrollContainer from '@/components/CmkScrollContainer.vue'
<${'/'}script>

<template>
  <CmkScrollContainer max-height="200px" type="outer">
    <p>
      Long content that will cause the container to overflow
      and display the custom "outer" style scrollbar.
    </p>
  </CmkScrollContainer>
</template>`

const loremIpsum = `
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam mattis magna a felis semper
feugiat. Integer mollis, velit ornare mollis vehicula, ex enim tempor nibh, ac bibendum elit
velit et quam. Nulla sed eleifend nibh. Quisque volutpat risus eget nisl gravida porttitor.
Proin bibendum, enim quis euismod accumsan, nunc urna condimentum nulla, in fermentum nunc purus
eu nisl. In malesuada, magna vel facilisis rhoncus, sem libero porta odio, ac venenatis tortor
urna vel nulla. Nunc elementum mattis auctor. Donec sagittis at nunc vel rutrum. Maecenas quis
ultrices mi. Duis semper blandit quam ut varius. Nam luctus neque nec magna interdum, sit amet
consectetur velit rhoncus. Suspendisse ultrices neque in nulla ultrices, in tempor velit
commodo. Integer congue dui at metus imperdiet, quis cursus magna blandit.`

const panelConfig = {
  type: {
    type: 'list',
    title: 'Scrollbar Type',
    options: [
      { title: 'Inner', name: 'inner' },
      { title: 'Outer', name: 'outer' }
    ] satisfies Options<ScrollContainerVariants['type']>[],
    initialState: 'inner' as const
  },
  height: { type: 'string', title: 'Fixed Height', initialState: '100%' },
  maxHeight: { type: 'string', title: 'Max Height', initialState: '200px' }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkScrollContainer</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkScrollContainer
        :type="propState.type"
        :height="propState.height"
        :max-height="propState.maxHeight"
        style="
          border: 1px solid var(--color-border);
          border-radius: var(--border-radius);
          padding: var(--dimension-2);
        "
      >
        <p style="white-space: pre-wrap">{{ loremIpsum.repeat(3) }}</p>
      </CmkScrollContainer>

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkScrollContainer" />

    <DemoDetailPageAccessibility :data="a11yDataCmkScrollContainer" />
  </DemoDetailPageLayout>
</template>
