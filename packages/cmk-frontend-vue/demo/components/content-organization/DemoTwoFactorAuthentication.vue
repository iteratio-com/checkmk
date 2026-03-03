<!--
Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
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
  type PanelConfig,
  createPanelState
} from '@demo/_demo/components/detail-page'
import type { TwoFactorAuth as TwoFactorAuthType } from 'cmk-shared-typing/typescript/two_factor_auth'
import { computed, ref } from 'vue'

import TwoFactorAuth from '@/two-factor-auth/TwoFactorAuthApp.vue'

defineProps<{ screenshotMode: boolean }>()

const a11yDataTwoFactorAuth = [
  {
    keys: ['Tab'],
    description: 'Moves keyboard focus to the different elements.'
  },
  {
    keys: [['Shift', 'Tab']],
    description: 'Moves focus to the previous element in reverse order.'
  },
  {
    keys: ['Enter'],
    description: 'Submits the form when focused within the input fields.'
  }
]

const codeExampleTwoFactorAuth = `<script setup lang="ts">
import type { TwoFactorAuth as TwoFactorAuthType } from 'cmk-shared-typing/typescript/two_factor_auth'
${'import'} TwoFactorAuth from '@/two-factor-auth/TwoFactorAuthApp.vue'

const methods: TwoFactorAuthType = {
  totp_credentials: true,
  webauthn_credentials: true,
  backup_codes: false
}
<${'/'}script>

<template>
  <TwoFactorAuth :available-methods="methods" />
</template>`

const panelConfig = {
  totp: { type: 'boolean', title: 'Enable TOTP', initialState: true },
  webauthn: { type: 'boolean', title: 'Enable WebAuthn', initialState: true },
  backup: { type: 'boolean', title: 'Enable Backup Codes', initialState: true }
} satisfies PanelConfig

const propState = ref(createPanelState(panelConfig))

const dynamicAvailableMethods = computed<TwoFactorAuthType>(() => ({
  totp_credentials: propState.value.totp,
  webauthn_credentials: propState.value.webauthn,
  backup_codes: propState.value.backup
}))
</script>

<template>
  <DemoDetailPageLayout>
    <DemoDetailPageHeader>TwoFactorAuthApp</DemoDetailPageHeader>

    <DemoDetailPageComponent>
      <TwoFactorAuth
        :key="JSON.stringify(dynamicAvailableMethods)"
        :available-methods="dynamicAvailableMethods"
      />

      <template #properties>
        <DemoPropertiesPanel v-model="propState" :config="panelConfig" />
      </template>
    </DemoDetailPageComponent>

    <DemoDetailPageCodeExample :code="codeExampleTwoFactorAuth" />

    <DemoDetailPageAccessibility :data="a11yDataTwoFactorAuth" />
  </DemoDetailPageLayout>
</template>
