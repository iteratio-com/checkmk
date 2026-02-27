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
  DemoDetailPageLayout
} from '@demo/_demo/components/detail-page'

import CmkParagraph from '@/components/typography/CmkParagraph.vue'

defineProps<{ screenshotMode: boolean }>()

const codeExampleCmkParagraph = `<script setup lang="ts">
${'import'} CmkParagraph from '@/components/typography/CmkParagraph.vue'
<${'/'}script>

<template>
  <CmkParagraph>
    The quick brown fox jumps over the lazy dog.
  </CmkParagraph>
</template>`
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>CmkParagraph</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <CmkParagraph>The quick brown fox jumps over the lazy dog.</CmkParagraph>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleCmkParagraph" />

    <DemoDetailPageAccessibility :data="[]" />
  </DemoDetailPageLayout>
</template>
