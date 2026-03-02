<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import CmkHeading from '@/components/typography/CmkHeading.vue'

export interface AccessibilityItem {
  key: string
  description: string
}

defineProps<{
  data: AccessibilityItem[]
}>()
</script>

<template>
  <div class="demo-accessibility-table__table">
    <div class="demo-accessibility-table__table-header">
      <CmkHeading type="h4">Key</CmkHeading>
      <CmkHeading type="h4">Description</CmkHeading>
    </div>
    <template v-if="data.length > 0">
      <div v-for="item in data" :key="item.key" class="demo-accessibility-table__table-row">
        <div class="demo-accessibility-table__table-cell">
          <span class="demo-accessibility-table__key-pill">{{ item.key }}</span>
        </div>
        <div class="demo-accessibility-table__table-cell">
          {{ item.description }}
        </div>
      </div>
    </template>
    <div v-else class="demo-accessibility-table__empty-message">
      No keyboard accessibility available for this component
    </div>
  </div>
</template>

<style scoped>
.demo-accessibility-table__table {
  border: 1px solid var(--demo-elements-border-color);
  background: var(--demo-detail-section-bg-color);
  border-radius: 8px;
  overflow: hidden;
  width: 100%;
  margin-bottom: var(--spacing);
}

.demo-accessibility-table__table-header {
  display: flex;
  background: var(--demo-elements-background-color);
  border-bottom: 1px solid var(--demo-elements-border-color);
}

.demo-accessibility-table__table-header > * {
  flex: 1;
  padding: 12px 16px;
  text-align: left;
}

.demo-accessibility-table__table-row {
  display: flex;
  border-top: 1px solid var(--demo-elements-border-color);
}

.demo-accessibility-table__table-cell {
  flex: 1;
  padding: 12px 16px;
  display: flex;
  align-items: center;
}

.demo-accessibility-table__key-pill {
  background: var(--demo-detail-table-pill-bg-color);
  border-radius: 4px;
  padding: 4px 8px;
  color: var(--demo-cta-banner-title-color);
  display: inline-block;
}

.demo-accessibility-table__empty-message {
  padding: 12px 16px;
  color: var(--demo-elements-text-color);
  text-align: center;
  font-style: italic;
}
</style>
