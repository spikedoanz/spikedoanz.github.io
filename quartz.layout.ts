import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [
    Component.PageTitle(),
  ],
  footer: Component.MobileOnly(Component.Spacer()),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.MobileOnly(Component.Darkmode()),
    Component.MobileOnly(Component.Spacer()),
  ],
  left: [
    Component.MobileOnly(Component.Spacer()),
  ],
  right: [
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.PageTitle(),
  ],
  left: [
    Component.MobileOnly(Component.Spacer()),
  ],
  right: [
    Component.Darkmode(),
  ],
}
