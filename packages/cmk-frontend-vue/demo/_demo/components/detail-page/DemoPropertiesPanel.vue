<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import type { ListPropDef, PanelConfig, PanelState } from '@demo/_demo/types/prop-panel.ts'

import CmkDropdown from '@/components/CmkDropdown'
import CmkHelpText from '@/components/CmkHelpText.vue'
import CmkLabel from '@/components/CmkLabel.vue'
import CmkSpace from '@/components/CmkSpace.vue'
import CmkSwitch from '@/components/CmkSwitch.vue'
import CmkHeading from '@/components/typography/CmkHeading.vue'
import CmkInput from '@/components/user-input/CmkInput.vue'

defineProps<{ config: PanelConfig }>()

const state = defineModel<PanelState>({ required: true })
</script>

<template>
  <div class="demo-properties-panel__properties-panel">
    <CmkHeading type="h4">Properties</CmkHeading>
    <CmkSpace size="small" />

    <div
      v-for="[key, def] in Object.entries(config)"
      :key="key"
      class="demo-properties-panel__prop-control"
    >
      <div class="demo-properties-panel__label-container">
        <CmkLabel :for="`ctrl-${key}`">{{ def.title }}</CmkLabel>
        <CmkSpace v-if="def.help" size="small" />
        <CmkHelpText v-if="def.help" :help="def.help" />
      </div>
      <CmkSwitch
        v-if="def.type === 'boolean'"
        :id="`ctrl-${key}`"
        :data="state[key] as boolean"
        @update:data="state[key] = $event"
      />
      <CmkInput
        v-else-if="def.type === 'string'"
        :id="`ctrl-${key}`"
        :model-value="state[key] as string"
        @update:model-value="state[key] = $event ?? ''"
      />
      <CmkDropdown
        v-else-if="def.type === 'list'"
        :component-id="`ctrl-${key}`"
        :label="def.title"
        :options="{ type: 'fixed', suggestions: (def as ListPropDef).options }"
        :selected-option="state[key] as string"
        @update:selected-option="$event !== null && (state[key] = $event)"
      />
    </div>
  </div>
</template>

<style scoped>
.demo-properties-panel__properties-panel {
  border: 1px solid var(--demo-elements-border-color);
  border-radius: 4px;
  padding: 16px;
}

.demo-properties-panel__prop-control {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 12px;
}
</style>
