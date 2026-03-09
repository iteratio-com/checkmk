/**
 * Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import type { Suggestion } from '@/components/CmkSuggestions'

export type Options<T> = { title: string; name: NonNullable<T> }

export interface BoolPropDef {
  type: 'boolean'
  title: string
  initialState: boolean
  help?: string
}

export interface StringPropDef {
  type: 'string'
  title: string
  initialState: string
  help?: string
}

export interface ListPropDef<T extends string = string> {
  type: 'list'
  title: string
  options: Suggestion[]
  initialState: T
  help?: string
}

export interface NumberPropDef {
  type: 'number'
  title: string
  initialState: number
  help?: string
}

export interface MultilineStringPropDef {
  type: 'multiline-string'
  title: string
  initialState: string
  help?: string
}

export type PropDef =
  | BoolPropDef
  | StringPropDef
  | NumberPropDef
  | ListPropDef<string>
  | MultilineStringPropDef

export type PanelConfig = Record<string, PropDef>

export type PanelState = Record<string, boolean | string | number>

type InferStateFromDef<T extends PropDef> = T extends BoolPropDef
  ? boolean
  : T extends StringPropDef
    ? string
    : T extends NumberPropDef
      ? number
      : T extends ListPropDef<infer U>
        ? NonNullable<U>
        : T extends MultilineStringPropDef
          ? string
          : never

export type InferPanelState<T extends PanelConfig> = {
  [K in keyof T]: InferStateFromDef<T[K]>
}

export function createPanelState<T extends PanelConfig>(config: T): InferPanelState<T> {
  return Object.fromEntries(
    Object.entries(config).map(([key, def]) => [key, def.initialState])
  ) as InferPanelState<T>
}
