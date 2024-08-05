import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "spike",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    baseUrl: "spikedoanz.github.io",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "created",
    theme: {
      typography: {
        header: "JetBrains Mono",
        body: "JetBrains Mono",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#dce0e8",     // background
          lightgray: "#ccd0da", // dashed lines
          gray: "#eff1f5",
          darkgray: "#7c7f93",  // regular text
          dark: "#4c4f69",      // bold text
          secondary: "#f38ba8", // hyperlinks and site header
          tertiary: "#9ca0b0",  // cursor highlight
          highlight: "rgba(0, 0, 0, 0)",
        },
        // darkMode: { // catpuccin mocha
        //   light: "#11111b",
        //   lightgray: "#6c7086",
        //   gray: "#1e1e2e",
        //   darkgray: "#b1b1b1",
        //   dark: "#cdd6f4",
        //   secondary: "#f38ba8",
        //   tertiary: "#45475a",
        //   highlight: "rgba(0, 0, 0, 0)",
        // },
        darkMode: { // rosepine dawn 
          light: "#faf4ed",
          lightgray: "#cecacd",
          gray: "#575279",
          darkgray: "#575279",
          dark: "#575279",
          secondary: "#b4637a",
          tertiary: "#dfdad9",
          highlight: "rgba(0, 0, 0, 0)",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.TableOfContents(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "filesystem"], // you can add 'git' here for last modified from Git but this makes the build slower
      }),
      Plugin.SyntaxHighlighting(),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Latex({ renderEngine: "katex" }),
      Plugin.Description(),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources({ fontOrigin: "googleFonts" }),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
