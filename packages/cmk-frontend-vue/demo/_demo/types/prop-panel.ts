/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { Suggestion } from '@/components/CmkSuggestions'

export interface BoolPropDef {
  type: 'boolean'
  title: string
  initialState: boolean
}

export interface StringPropDef {
  type: 'string'
  title: string
  initialState: string
}

export interface ListPropDef {
  type: 'list'
  title: string
  options: Suggestion[]
  initialState: string
}

export type PropDef = BoolPropDef | StringPropDef | ListPropDef

export type PanelConfig = Record<string, PropDef>

export type PanelState = Record<string, boolean | string | null>

type InferStateFromDef<T extends PropDef> = T extends BoolPropDef
  ? boolean
  : T extends StringPropDef
    ? string
    : T extends ListPropDef
      ? string | null
      : never

export type InferPanelState<T extends PanelConfig> = {
  [K in keyof T]: InferStateFromDef<T[K]>
}

export function createPanelState<T extends PanelConfig>(config: T): InferPanelState<T> {
  return Object.fromEntries(
    Object.entries(config).map(([key, def]) => [key, def.initialState])
  ) as InferPanelState<T>
}
