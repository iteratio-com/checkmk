<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
import AccessibilityTable, {
  type AccessibilityItem
} from '@demo/_demo/components/detail-page/DemoAccessibilityTable.vue'

import CmkHeading from '@/components/typography/CmkHeading.vue'

defineProps<{
  data?: AccessibilityItem[]
}>()
</script>

<template>
  <div v-if="data?.length" class="demo-detail-page-accessibility-table__section">
    <CmkHeading type="h2">Accessibility</CmkHeading>
    <AccessibilityTable :data="data" />
  </div>
</template>

<style scoped>
.demo-detail-page-accessibility-table__section {
  display: flex;
  flex-direction: column;
  gap: var(--dimension-6);
}
</style>
