<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts"></script>

<template>
  <div class="demo-detail-page-component__component-container">
    <div class="demo-detail-page-component__preview-panel">
      <slot></slot>
    </div>
    <div class="demo-detail-page-component__properties-panel">
      <slot name="properties"></slot>
    </div>
  </div>
</template>

<style scoped>
.demo-detail-page-component__component-container {
  display: flex;
  gap: var(--dimension-10);
  padding: var(--dimension-10);
  border: 1px solid var(--demo-elements-border-color);
  border-radius: var(--dimension-4);
  margin-top: var(--dimension-8);
}

.demo-detail-page-component__preview-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--dimension-10);
}

.demo-detail-page-component__properties-panel {
  flex-shrink: 0;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: var(--dimension-4);
}
</style>
