<!--
Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<template>
  <div class="demo-detail-page-layout">
    <slot />
  </div>
</template>

<style scoped>
.demo-detail-page-layout {
  display: flex;
  flex-direction: column;
  padding: var(--dimension-6);
  gap: 24px;
}
</style>
