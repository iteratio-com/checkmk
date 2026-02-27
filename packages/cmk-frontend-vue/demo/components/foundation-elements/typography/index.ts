/**
 * Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { type Folder, Page } from '@demo/_demo/types/page'

import DemoCmkHeading from './DemoCmkHeading.vue'
import DemoCmkParagraph from './DemoCmkParagraph.vue'
import DemoI18n from './DemoI18n.vue'

export const pages: Array<Folder | Page> = [
  new Page('CmkHeading', DemoCmkHeading),
  new Page('CmkParagraph', DemoCmkParagraph),
  new Page('i18n', DemoI18n)
]
