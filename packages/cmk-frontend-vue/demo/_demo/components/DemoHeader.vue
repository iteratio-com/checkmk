<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->

<script setup lang="ts">
import { ref } from 'vue'

import iconUrl from '../assets/images/checkmk_logo.svg'
import DemoGlobalTheme from './DemoGlobalTheme.vue'

const selectedTheme = ref<'facelift' | 'modern-dark'>('facelift')
</script>

<template>
  <div class="demo-header">
    <div class="demo-header__item">
      <div class="demo-header__group">
        <img :src="iconUrl" alt="Checkmk logo" width="117" />
        <span class="demo-header__app-title">| Vue Demo App</span>
      </div>
    </div>
    <div class="demo-header__item">
      <DemoGlobalTheme v-model:theme="selectedTheme" />
    </div>
  </div>
</template>

<style scoped>
.demo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.demo-header__item {
  display: flex;
  align-items: center;
}

.demo-header__group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.demo-header__app-title {
  color: var(--color-corporate-green-50);
  font-size: 20px;
  font-weight: 400;
  display: flex;
  align-items: center;
}
</style>
