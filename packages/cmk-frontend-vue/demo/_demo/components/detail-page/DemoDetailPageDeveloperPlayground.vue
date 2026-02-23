<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import { computed, ref } from 'vue'

import CmkAccordion from '@/components/CmkAccordion/CmkAccordion.vue'
import CmkAccordionItem from '@/components/CmkAccordion/CmkAccordionItem.vue'
import CmkIcon from '@/components/CmkIcon'
import CmkSpace from '@/components/CmkSpace.vue'

const openedItems = ref<string[]>([])
const isDeveloperOpen = computed(() => openedItems.value.includes('developer-playground'))
</script>

<template>
  <div class="demo-detail-page-developer-playground__section">
    <CmkAccordion v-model="openedItems" :max-open="1" :min-open="0">
      <CmkAccordionItem value="developer-playground">
        <template #header>
          <CmkIcon name="tree-closed" size="xsmall" :rotate="isDeveloperOpen ? 90 : 0" />
          <CmkSpace size="small" />
          <span> Developer Playground </span>
        </template>

        <template #content>
          <slot></slot>
        </template>
      </CmkAccordionItem>
    </CmkAccordion>
  </div>
</template>

<style scoped>
.demo-detail-page-developer-playground__section {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-6);
}
</style>
